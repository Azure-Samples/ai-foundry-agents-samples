# Streamable HTTP MCP Server

## Running the MCP Server locally 
Run the following commands
```
cd examples/mcp/streamable-http/mcp-server 
uv venv
uv sync
uv run weather.py
```

## Run MCP Inspector to test and debug MCP Server
Open a new terminal window and run the following commands
```
npx @modelcontextprotocol/inspector
```

Open a browser and navigate to http://127.0.0.1:6274

In the URL enter: http://localhost:8001/mcp and click Connect. 


## Deploy to Azure Container Apps
Run the following commands
```
az containerapp up \
    --resource-group <RESOURCE_GROUP_NAME> \
    --name streamable-weather-mcp \
    --environment mcp \
    --location <REGION> \
    --source .
```


    