# Streamable HTTP MCP Server

## Running locally 
Run the following commands
```
cd examples/mcp/streamable-http/mcp-server 
uv init
uv venv
uv add mcp
uv run weather.py
```


## Deploy to Azure Container Apps
Run the following commands
```
az containerapp up \
    -g <RESOURCE_GROUP_NAME> \
    -n streamable-weather-mcp \
    --environment mcp \
    -l <REGION> \
    --source .
```


    