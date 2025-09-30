package main

import (
	"fmt"
)

/*
TODO: Postgresql için veri structı oluşturulmalı
*/
type PGItem struct {
	container_id           string
	server_port            string
	mcp_server_name        string
	mcp_server_description string
	function_args          []string
	function_body          string
}

func main() {
	fmt.Println("Hello World")
}

func sync_db(pg_db []string, rds_db []string) {

}

func fetchRedis() {

}

func fetchPostgresql() {

}
