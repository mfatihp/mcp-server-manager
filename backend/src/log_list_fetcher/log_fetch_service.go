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
	Container_id    string `json:"container_id"`
	Mcp_server_name string `json:"mcp_server_name"`
	Func_args       string `json:"func_args"`
	Server_status   string `json:"server_status"`
	Server_port     string `json:"server_port"`
}

type MCPServer struct {
	Container_id    string `json:"container_id"`
	Mcp_server_name string `json:"mcp_server_name"`
	Func_args       string `json:"func_args"`
	Server_port     string `json:"server_port"`
}

// Middleware to add CORS headers
func corsMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		// Handle preflight (OPTIONS)
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/log_list", log_fetcher)

	handler := corsMiddleware(mux)

	log.Println("🚀 Server started on :8090")
	if err := http.ListenAndServe(":8090", handler); err != nil {
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
	redisKeys, _, err := rdb.Scan(ctx, cursor, "contID:*", 100).Result()
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

		id := key[len("contID:"):]
		redisUsers[id] = MCPServer{
			Container_id:    id,
			Mcp_server_name: data.Mcp_server_name,
			Func_args:       data.Func_args,
			Server_port:     data.Server_port,
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
