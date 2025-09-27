CREATE TABLE IF NOT EXISTS MCP_SERVERS (
    id SERIAL PRIMARY KEY,
    container_id TEXT,
    server_port TEXT,
    mcp_server_name TEXT,
    mcp_server_description TEXT,
    function_args JSONB,
    function_body TEXT   
);