package main

import (
	"context"
	"fmt"
	"log"
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

func main() {
	// Load env
	if err := godotenv.Load(); err != nil {
		log.Fatal(err)
	}

	ctx := context.Background()

	redisAddr := os.Getenv("REDIS_ADDR")

	// Connect Redis
	rdb := redis.NewClient(&redis.Options{Addr: redisAddr})
	defer rdb.Close()

	err := redis_log_receiver(rdb, ctx)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Hello")
	log.Fatal()
}

func redis_log_receiver(rdb *redis.Client, ctx context.Context) error {

}
