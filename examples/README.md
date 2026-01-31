# Examples

This directory contains example applications built with pygentic-ai.

## Available Examples

### [Simple Chat](simple-chat/)

A minimal chat application demonstrating:
- Factory pattern for agent configuration
- AgentManager for handling multiple agents
- Basic chat loop with conversation history
- Environment-based configuration

**Difficulty**: Beginner
**Time**: 5 minutes

```bash
cd simple-chat
export OPENAI_API_KEY="sk-..."
python app.py
```

## More Examples Coming Soon

- **Advanced Workflow**: Multi-agent orchestration with routing
- **Tool Integration**: Custom tools and MCP servers
- **RAG Application**: Document Q&A with retrieval
- **API Server**: FastAPI integration

## Structure

Each example includes:
- `README.md` - Detailed explanation
- `app.py` - Main application code
- `.env.example` - Required environment variables
- Additional files as needed

## Contributing

Have a useful example? Submit a PR! Examples should be:
- Self-contained and runnable
- Well-documented
- Demonstrate a specific use case
- Under 200 lines of code
