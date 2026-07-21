from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(model="granite4.1:3b")
