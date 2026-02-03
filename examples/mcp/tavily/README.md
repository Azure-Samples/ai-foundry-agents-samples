# Azure AI Agent with Tavily MCP Tool Example

### Navigate to the Tavily MCP Tool example folder

```
cd examples/mcp/tavily
```

### Create and activate Python virtual environment
```
python -m venv .venv
```
#### MacOS/Linux
```
source .venv/bin/activate
```
#### Windows
```
venv\Scripts\activate
```
### Install dependencies
```
pip install -U agent-framework --pre
pip install python-dotenv
```

### Rename `.env_sample` file to `.env` 
Update the following Environment Variables:
- `AZURE_AI_PROJECT_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- `TAVILY_MCP_SERVER_URL`

### Run the python program
```
python azure_ai_with_tavily_mcp.py 
```