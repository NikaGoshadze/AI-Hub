import importlib
import sys
import types

import pytest


class _DummyListIndexes:
    def names(self):
        return ["langchain-books-pure-v1"]


class _DummyPinecone:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def list_indexes(self):
        return _DummyListIndexes()


class _DummyPineconeVectorStore:
    @classmethod
    def from_existing_index(cls, index_name, embedding):
        return cls()


class _DummyChatGoogleGenerativeAI:
    def __init__(self, model=None, temperature=None):
        self.model = model
        self.temperature = temperature


class _DummyHuggingFaceEmbeddings:
    def __init__(self, model_name=None, model_kwargs=None):
        self.model_name = model_name
        self.model_kwargs = model_kwargs


class _DummyTool:
    def __init__(self, name=None, func=None, description=None):
        self.name = name
        self.func = func
        self.description = description


class _DummyMemory:
    def __init__(self, memory_key=None, return_messages=None):
        self.memory_key = memory_key
        self.return_messages = return_messages


class _DummyPromptMessage:
    def __init__(self):
        self.prompt = types.SimpleNamespace(template="")


class _DummyPrompt:
    def __init__(self):
        self.messages = [_DummyPromptMessage()]


def _install_fakes(monkeypatch):
    monkeypatch.setitem(sys.modules, "dotenv", types.SimpleNamespace(load_dotenv=lambda: None))
    monkeypatch.setitem(sys.modules, "langchain", types.SimpleNamespace(hub=types.SimpleNamespace(pull=lambda name: _DummyPrompt())))
    monkeypatch.setitem(sys.modules, "langchain.agents", types.SimpleNamespace(AgentExecutor=lambda **kwargs: types.SimpleNamespace(), create_json_chat_agent=lambda llm, tools, prompt: object()))
    monkeypatch.setitem(sys.modules, "langchain_core.tools", types.SimpleNamespace(Tool=_DummyTool))
    monkeypatch.setitem(sys.modules, "langchain.memory", types.SimpleNamespace(ConversationBufferMemory=_DummyMemory))
    monkeypatch.setitem(sys.modules, "langchain_google_genai", types.SimpleNamespace(ChatGoogleGenerativeAI=_DummyChatGoogleGenerativeAI))
    monkeypatch.setitem(sys.modules, "langchain_huggingface", types.SimpleNamespace(HuggingFaceEmbeddings=_DummyHuggingFaceEmbeddings))
    monkeypatch.setitem(sys.modules, "langchain_pinecone", types.SimpleNamespace(PineconeVectorStore=_DummyPineconeVectorStore))
    monkeypatch.setitem(sys.modules, "pinecone", types.SimpleNamespace(Pinecone=_DummyPinecone))


@pytest.fixture()
def app_module(monkeypatch):
    _install_fakes(monkeypatch)
    monkeypatch.setenv("GOOGLE_API_KEY", "test")
    monkeypatch.setenv("PINECONE_API_KEY", "test")
    sys.modules.pop("books_app.main", None)
    sys.modules.pop("books_app.web_app", None)
    module = importlib.import_module("books_app.web_app")
    return module


def test_search_endpoint_success_returns_results_and_count(app_module, monkeypatch):
    monkeypatch.setattr(app_module, "search_book_database", lambda query: [
        {"title": "Book One", "authors": ["Author A"]},
        {"title": "Book Two", "authors": "Author B"},
    ])

    client = app_module.app.test_client()
    response = client.get("/search?query=magic")

    assert response.status_code == 200
    assert response.get_json() == {
        "results": [
            {"title": "Book One", "authors": ["Author A"]},
            {"title": "Book Two", "authors": "Author B"},
        ],
        "count": 2,
    }


def test_search_endpoint_empty_result_returns_empty_payload(app_module, monkeypatch):
    monkeypatch.setattr(app_module, "search_book_database", lambda query: [])

    client = app_module.app.test_client()
    response = client.get("/search?query=missing")

    assert response.status_code == 200
    assert response.get_json() == {"results": [], "count": 0}


def test_search_endpoint_error_returns_friendly_message(app_module, monkeypatch):
    def raise_error(query):
        raise RuntimeError("boom")

    monkeypatch.setattr(app_module, "search_book_database", raise_error)

    client = app_module.app.test_client()
    response = client.get("/search?query=error")

    assert response.status_code == 500
    payload = response.get_json()
    assert payload["results"] == []
    assert payload["count"] == 0
    assert "something went wrong" in payload["error"]
