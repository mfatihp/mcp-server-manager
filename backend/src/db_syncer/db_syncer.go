package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

type MCPServer struct {
	container_id    string
	mcp_server_name string
}

func main() {
	// Load env
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}

	var ctx = context.Background()

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

	if err := syncUsers(pgPool, rdb, ctx); err != nil {
		log.Fatal("Sync error:", err)
	}
}

func syncUsers(pg *pgxpool.Pool, rdb *redis.Client, ctx context.Context) error {
	// Fetch from Postgres
	rows, err := pg.Query(ctx, "SELECT container_id, mcp_server_name FROM mcp_servers")
	if err != nil {
		return err
	}
	defer rows.Close()

	pgUsers := make(map[string]MCPServer)
	for rows.Next() {
		var server MCPServer
		if err := rows.Scan(&server.container_id, &server.mcp_server_name); err != nil {
			return err
		}
		pgUsers[server.container_id] = server
	}

	// Fetch from Redis
	redisKeys, err := rdb.Keys(ctx, "contID:*").Result()
	if err != nil {
		return err
	}

	redisUsers := make(map[string]MCPServer)
	for _, key := range redisKeys {
		data, err := rdb.HGetAll(ctx, key).Result()
		if err != nil || len(data) == 0 {
			continue
		}

		id := key[len("contID:"):]
		redisUsers[id] = MCPServer{
			container_id:    id,
			mcp_server_name: data["name"],
		}
	}

	// Compare + Sync
	for id, pgUser := range pgUsers {
		redisUser, exists := redisUsers[id]
		key := fmt.Sprintf("contID:%s", id)

		if !exists {
			// Insert missing
			rdb.HSet(ctx, key,
				"container_id", pgUser.container_id,
				"mcp_server_name", pgUser.mcp_server_name,
				"status", "active")

			fmt.Println("Added:", pgUser)

		} else if pgUser.mcp_server_name != redisUser.mcp_server_name {
			// Update if different
			rdb.HSet(ctx, key, "name", pgUser.mcp_server_name)
			fmt.Println("Updated:", pgUser)
		}
	}

	// Remove extras from Redis
	for id := range redisUsers {
		if _, exists := pgUsers[id]; !exists {
			key := fmt.Sprintf("contID:%s", id)
			rdb.Del(ctx, key)
			fmt.Println("Deleted contID:", id)
		}
	}

	return nil
}
