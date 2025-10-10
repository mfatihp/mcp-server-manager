package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

type RDSItem struct {
	Container_id    string
	Mcp_server_name string
	Server_status   string
	Server_port     string
}

type MCPServer struct {
	container_id    string
	mcp_server_name string
	server_port     string
}

func main() {
	http.HandleFunc("/log_list", log_fetcher)

	log.Println("🚀 Server started on :8090")
	if err := http.ListenAndServe(":8090", nil); err != nil {
		log.Fatal(err)
	}
}

func redis_log_fetcher() (map[string]MCPServer, error) {
	// Load env
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}

	ctx := context.Background()
	redisAddr := os.Getenv("REDIS_ADDR")

	// Connect Redis
	rdb := redis.NewClient(&redis.Options{Addr: redisAddr})
	defer rdb.Close()

	// Fetch from Redis DB
	var cursor uint64
	redisKeys, _, err := rdb.Scan(ctx, cursor, "contId:*", 100).Result()
	if err != nil {
		log.Fatal(err)
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

	return redisUsers, nil
}

func log_fetcher(w http.ResponseWriter, req *http.Request) {
	logs, err := redis_log_fetcher()
	if err != nil {
		http.Error(w, "failed to fetch logs: "+err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(logs); err != nil {
		http.Error(w, "failed to encode response", http.StatusInternalServerError)
	}
}
