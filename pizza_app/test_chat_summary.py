import importlib
import sys
import types

import pytest


class DummyLLM:
    def __init__(self, *args, **kwargs):
        pass


class DummyMemory:
    def __init__(self, *args, **kwargs):
        self.moving_summary_buffer = ""

    def load_memory_variables(self, x):
        return {"history": []}

    def save_context(self, inputs, outputs):
        return None


def _install_fake_dependencies(monkeypatch):
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda: None
    monkeypatch.setitem(sys.modules, "dotenv", dotenv)

    langchain_core_prompts = types.ModuleType("langchain_core.prompts")

    class DummyPrompt:
        @classmethod
        def from_messages(cls, messages):
            return cls()

        def __or__(self, other):
            return self

    class DummyMessagesPlaceholder:
        def __init__(self, variable_name):
            self.variable_name = variable_name

    langchain_core_prompts.ChatPromptTemplate = DummyPrompt
    langchain_core_prompts.MessagesPlaceholder = DummyMessagesPlaceholder
    monkeypatch.setitem(sys.modules, "langchain_core.prompts", langchain_core_prompts)

    langchain_core_runnables = types.ModuleType("langchain_core.runnables")

    class DummyRunnablePassthrough:
        @classmethod
        def assign(cls, **kwargs):
            return cls()

        def __or__(self, other):
            return self

    langchain_core_runnables.RunnablePassthrough = DummyRunnablePassthrough
    monkeypatch.setitem(sys.modules, "langchain_core.runnables", langchain_core_runnables)

    langchain_core_output_parsers = types.ModuleType("langchain_core.output_parsers")
    langchain_core_output_parsers.StrOutputParser = lambda: object()
    monkeypatch.setitem(sys.modules, "langchain_core.output_parsers", langchain_core_output_parsers)

    langchain_google_genai = types.ModuleType("langchain_google_genai")
    langchain_google_genai.ChatGoogleGenerativeAI = DummyLLM
    monkeypatch.setitem(sys.modules, "langchain_google_genai", langchain_google_genai)

    langchain_memory = types.ModuleType("langchain.memory")
    langchain_memory.ConversationSummaryBufferMemory = DummyMemory
    monkeypatch.setitem(sys.modules, "langchain.memory", langchain_memory)


@pytest.fixture
def chat_summary_module(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy")
    _install_fake_dependencies(monkeypatch)
    sys.modules.pop("pizza_app.main", None)
    sys.modules.pop("pizza_app.chat_summary", None)
    import pizza_app.chat_summary as chat_summary
    importlib.reload(chat_summary)
    return chat_summary


def test_summary_lines_missing_and_empty(chat_summary_module):
    expected = ["\n[System: ჯერ საუბრის ისტორია არ არის.]"]
    assert chat_summary_module.summary_lines(None) == expected
    assert chat_summary_module.summary_lines("") == expected
    assert chat_summary_module.summary_lines(0) == expected


def test_summary_lines_populated(chat_summary_module):
    summary = "პიცის შეკვეთა: მარგარიტა და სოდა"
    assert chat_summary_module.summary_lines(summary) == [
        "\n--- მიმდინარე საუბრის ისტორია ---",
        summary,
    ]
