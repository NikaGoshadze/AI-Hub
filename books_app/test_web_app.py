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

    store = types.SimpleNamespace()
    fake_pinecone_vs = types.ModuleType("langchain_pinecone")
    fake_pinecone_vs.PineconeVectorStore = types.SimpleNamespace(
        from_existing_index=lambda *args, **kwargs: store
    )

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

    app_modules = ("books_app.main", "books_app.web_app")
    previous = {name: sys.modules.pop(name, None) for name in app_modules}
    try:
        yield importlib.import_module("books_app.web_app"), store
    finally:
        for name in app_modules:
            sys.modules.pop(name, None)
            if previous[name] is not None:
                sys.modules[name] = previous[name]


def test_web_success(web_app_module):
    web_app, store = web_app_module
    store.similarity_search = lambda query, k: [
        types.SimpleNamespace(metadata={"title": "Book One", "authors": "Author A"}),
        types.SimpleNamespace(metadata={"title": "Book Two", "authors": "Author B"}),
    ]

    client = web_app.app.test_client()
    response = client.post("/", data={"query": "mystery"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "2 results found." in html
    assert "Title: Book One, Authors: Author A" in html
    assert "Title: Book Two, Authors: Author B" in html


def test_web_no_results(web_app_module):
    web_app, store = web_app_module
    store.similarity_search = lambda query, k: []

    client = web_app.app.test_client()
    response = client.post("/", data={"query": "nothing"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "No results" in html
    assert "No relevant books found in the database." in html


def test_web_backend_error(web_app_module):
    web_app, store = web_app_module

    def raise_error(query, k):
        raise RuntimeError("boom")

    store.similarity_search = raise_error

    client = web_app.app.test_client()
    response = client.post("/", data={"query": "oops"})

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Search unavailable" in html
    assert "Sorry, we couldn’t complete that search right now. Please try again." in html
