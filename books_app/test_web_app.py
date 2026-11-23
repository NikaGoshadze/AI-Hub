import importlib
import sys
import types

import pytest


@pytest.fixture()
def web_app_module(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy")
    monkeypatch.setenv("PINECONE_API_KEY", "dummy")
    monkeypatch.delenv("BOOK_SEARCH_LIMIT", raising=False)

    fake_langchain = types.ModuleType("langchain")
    fake_langchain.hub = types.SimpleNamespace(pull=lambda _: types.SimpleNamespace(messages=[types.SimpleNamespace(prompt=types.SimpleNamespace(template=""))]))

    fake_agents = types.ModuleType("langchain.agents")
    fake_agents.AgentExecutor = lambda *args, **kwargs: types.SimpleNamespace(invoke=lambda payload: {"output": payload["input"]})
    fake_agents.create_json_chat_agent = lambda *args, **kwargs: object()

    fake_tools = types.ModuleType("langchain_core.tools")
    fake_tools.Tool = lambda **kwargs: kwargs

    fake_memory = types.ModuleType("langchain.memory")
    fake_memory.ConversationBufferMemory = lambda *args, **kwargs: object()

    fake_genai = types.ModuleType("langchain_google_genai")
    fake_genai.ChatGoogleGenerativeAI = lambda *args, **kwargs: object()

    fake_hf = types.ModuleType("langchain_huggingface")
    fake_hf.HuggingFaceEmbeddings = lambda *args, **kwargs: object()

    fake_pinecone_vs = types.ModuleType("langchain_pinecone")
    fake_pinecone_vs.PineconeVectorStore = types.SimpleNamespace(from_existing_index=lambda *args, **kwargs: object())

    fake_pinecone = types.ModuleType("pinecone")
    fake_pinecone.Pinecone = lambda *args, **kwargs: types.SimpleNamespace(list_indexes=lambda: types.SimpleNamespace(names=lambda: ["langchain-books-pure-v1"]))

    fake_dotenv = types.ModuleType("dotenv")
    fake_dotenv.load_dotenv = lambda: None

    monkeypatch.setitem(sys.modules, "langchain", fake_langchain)
    monkeypatch.setitem(sys.modules, "langchain.agents", fake_agents)
    monkeypatch.setitem(sys.modules, "langchain_core.tools", fake_tools)
    monkeypatch.setitem(sys.modules, "langchain.memory", fake_memory)
    monkeypatch.setitem(sys.modules, "langchain_google_genai", fake_genai)
    monkeypatch.setitem(sys.modules, "langchain_huggingface", fake_hf)
    monkeypatch.setitem(sys.modules, "langchain_pinecone", fake_pinecone_vs)
    monkeypatch.setitem(sys.modules, "pinecone", fake_pinecone)
    monkeypatch.setitem(sys.modules, "dotenv", fake_dotenv)

    sys.modules.pop("books_app.main", None)
    sys.modules.pop("books_app.web_app", None)
    module = importlib.import_module("books_app.web_app")
    yield module


def test_web_success(web_app_module, monkeypatch):
    monkeypatch.setattr(web_app_module, "lookup_book_database", lambda query: ([
        types.SimpleNamespace(title="Book One", authors="Author A"),
        types.SimpleNamespace(title="Book Two", authors="Author B"),
    ], 2))

    client = web_app_module.app.test_client()
    response = client.post("/", data={"query": "mystery"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "2 results found." in html
    assert "Title: Book One, Authors: Author A" in html
    assert "Title: Book Two, Authors: Author B" in html


def test_web_no_results(web_app_module, monkeypatch):
    monkeypatch.setattr(web_app_module, "lookup_book_database", lambda query: ([], 0))

    client = web_app_module.app.test_client()
    response = client.post("/", data={"query": "nothing"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No results" in html
    assert "No relevant books found in the database." in html


def test_web_backend_error(web_app_module, monkeypatch):
    def raise_error(query):
        raise RuntimeError("boom")

    monkeypatch.setattr(web_app_module, "lookup_book_database", raise_error)

    client = web_app_module.app.test_client()
    response = client.post("/", data={"query": "oops"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Search unavailable" in html
    assert "Sorry, we couldn’t complete that search right now. Please try again." in html