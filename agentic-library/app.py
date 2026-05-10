import os
import streamlit as st
import requests
#gemini import
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
load_dotenv()

TOOLS = types.Tool(function_declarations = [
    types.FunctionDeclaration(
        name="search_books",
        description=("Search the open library database for the books by title,"
        "author, or subject."
            "Return the book titles, author, publication year etc."),
        parameters=  {
            "type":"object",
            "properties": {
                "query": {
                    "type":"string",
                    "description": "Search query string (book title, author etc)"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["general","title","author"],
                    "description": "Type of search to perform"
                }
            },
            "required": ["query"]
        }
    )
])

def search_books(query, search_type):
    base = "https://openlibrary.org/search.json"
    params = {
        "limit": 6,
        "fields": "key, title, author_name, cover_i, edition_count, subject"
    }
    if search_type == "title":
        params['title'] = query
    elif search_type == "author":
        params['author'] = query
    try:
        resp = requests.get(base, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        books = []
        for doc in data.get("docs",[]):
            books.append({
                "key": doc.get("key"),
                "title": doc.get("title"),
                "authors": doc.get("author_name"),
                "cover_i": doc.get("cover_i"),
            })
        return {"total_found":len(books), "books": books}
    except (Exception):
        print(Exception) 

st.title("Agentic Library")
st.set_page_config(
    page_title="RAG Chatbot",
    layout="centered",
)
api_key = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-flash-latest"
prompt = st.text_input("Ask about books",
                        placeholder = "crime thrillar books")
if st.button("Ask") and prompt: 
    client = genai.Client(api_key=api_key)
    with st.status("Asking LLM for tool call analysis"):
        
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction= "You are a book discovery assitant use" \
                " available tools to get the books ",
                tools=[TOOLS]
            )
        )
        print(f"Response from gemini {response}")
        candidate = response.candidates[0]
        parts = candidate.content.parts[0]

        st.text(f"{parts.function_call}")
        st.text(f"{parts.function_call.args}")
        query = parts.function_call.args.get("query")
        if parts.function_call.name == 'search_books':
            result = search_books(query,'title')
            st.header(result)