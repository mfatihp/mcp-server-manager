package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

type MCPServer struct {
	container_id    string
	mcp_server_name string
	server_port     string
}

type RDSItem struct {
	Container_id    string
	Mcp_server_name string
	Server_status   string
	Server_port     string
}

func main() {
	// Load env
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}

	ctx := context.Background()

	pgURL := os.Getenv("PG_URL")
	redisAddr := os.Getenv("REDIS_ADDR")

	// Connect Postgres
	pgPool, err := pgxpool.New(ctx, pgURL)
	if err != nil {
		log.Fatal("Postgres error:", err)
	}
	defer pgPool.Close()

	// Connect Redis
	rdb := redis.NewClient(&redis.Options{Addr: redisAddr})
	defer rdb.Close()

	ticker := time.NewTicker(10 * time.Second)

	for {
		t := <-ticker.C
		fmt.Println("Synced at:", t.Format("2006-01-02 15:04:05"))
		if err := syncUsers(pgPool, rdb, ctx); err != nil {
			log.Fatal("Sync error:", err)
		}
	}

}

func syncUsers(pg *pgxpool.Pool, rdb *redis.Client, ctx context.Context) error {
	// Fetch from Postgres DB
	rows, err := pg.Query(ctx, "SELECT container_id, mcp_server_name, server_port FROM mcp_servers")
	if err != nil {
		return err
	}
	defer rows.Close()

	pgUsers := make(map[string]MCPServer)
	for rows.Next() {
		var server MCPServer
		if err := rows.Scan(&server.container_id, &server.mcp_server_name, &server.server_port); err != nil {
			return err
		}
		pgUsers[server.container_id] = server
	}

	// Fetch from Redis DB
	var cursor uint64
	redisKeys, _, err := rdb.Scan(ctx, cursor, "contId:*", 10).Result()

	if err != nil {
		return err
	}

	redisUsers := make(map[string]MCPServer)

	for _, key := range redisKeys {
		value, err := rdb.Do(ctx, "JSON.GET", key, ".").Text()

		var data RDSItem
		err2 := json.Unmarshal([]byte(value), &data)

		if err != nil || err2 != nil {
			continue
		}

		id := key[len("contId:"):]
		redisUsers[id] = MCPServer{
			container_id:    id,
			mcp_server_name: data.Mcp_server_name,
			server_port:     data.Server_port,
		}
	}

	// Compare + Sync
	for id, pgUser := range pgUsers {
		_, exists := redisUsers[id]
		key := fmt.Sprintf("contID:%s", id)

		if !exists {
			// Insert missing server information
			new_val := RDSItem{
				Container_id:    pgUser.container_id,
				Mcp_server_name: pgUser.mcp_server_name,
				Server_status:   "active",
				Server_port:     pgUser.server_port,
			}

			jsondata, _ := json.Marshal(new_val)

			res, err := rdb.Do(ctx, "JSON.SET", key, "$", jsondata).Result()

			if err != nil || res != nil {
				log.Fatal(err)
			}

			fmt.Println("Added:", pgUser)

		}
	}

	// Remove non-exist records from Redis
	for id := range redisUsers {
		if _, exists := pgUsers[id]; !exists {
			key := fmt.Sprintf("contID:%s", id)
			_, err := rdb.Do(ctx, "JSON.DEL", key, ".").Result()

			if err != nil {
				log.Fatalf("Failed to delete JSON: %v", err)
			}
			fmt.Println("Deleted contID:", id)
		}
	}

	return nil
}
