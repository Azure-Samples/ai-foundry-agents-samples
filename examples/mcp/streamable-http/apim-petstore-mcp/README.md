# MCP Client for Pet Store MCP Server on Azure API Management, using Semantic Kernel

**Read the Blog Post**: https://medium.com/@eitansela/expose-your-rest-api-as-an-mcp-server-in-minutes-with-azure-api-management-1deb51142a04

## Running the MCP Client

Save the file `.env_sample` as `.env` and update the environment variables. 

Run the following commands
```
cd examples/mcp/streamable-http/apim-petstore-mcp 
uv venv
uv sync
uv run pet_store_mcp.py
```

**NOTE**: when running this sample code, you'll get `HTTP/1.1 401 Unauthorized` error, when connecting to the Pet Store MCP Server on APIM. 
This demonstrates that the MCP Server is secure and can be reachable only by providing the Bearer token.
To fix this, uncomment the line setting the headers in the `MCPStreamableHttpPlugin` definition (around line 115). 