from lab import *
show("RAG poisoning -> simulated MCP tool call", RAG_PROMPT, ask(RAG_SYS, RAG_PROMPT, "RAG"), "TOOL:send_email")