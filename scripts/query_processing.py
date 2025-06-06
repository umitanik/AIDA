import streamlit as st
from haystack.core.pipeline import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.routers import ConditionalRouter
from haystack.components.websearch import SerperDevWebSearch
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.generators.google_ai.chat.gemini import GoogleAIGeminiChatGenerator

from scripts.config import EMBEDDING_MODEL, GENERATOR_MODEL, TOP_K
from scripts.utils import log_message

# Safely get API keys from secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SERPERDEV_API_KEY = st.secrets["SERPERDEV_API_KEY"]
except Exception as e:
    log_message(f"API anahtarları yüklenirken hata oluştu: {str(e)}", level="error")
    GOOGLE_API_KEY = None
    SERPERDEV_API_KEY = None


def build_query_pipeline(document_store):
    """
    Builds the query pipeline to process user queries and generate responses.

    Args:
        document_store (InMemoryDocumentStore): The document store to retrieve from.

    Returns:
        Pipeline: The configured query pipeline or None if API keys are missing.
    """
    log_message("Building query pipeline...")

    # Check if API keys are available
    if GOOGLE_API_KEY is None or SERPERDEV_API_KEY is None:
        log_message("API anahtarları eksik. Query pipeline oluşturulamıyor.", level="error")
        return None

    prompt_template = """
    {% if web_documents %}
        You are an expert AI assistant focused on technical questions about Python libraries such as Pandas, NumPy, TensorFlow, PyTorch, LangChain, and Haystack.

        A user has asked the following question:
        **"{{ query }}"**

        You are given web-retrieved documents that may help. Your goal is:

        - If the user asks a code-related question, provide:
          - A **short but functional Python code snippet**
          - A **step-by-step explanation** of how it works
        - Otherwise, provide a clear, accurate technical answer.
        - Use only the content in the documents.
        - If useful, include source links from the documents.
        - If there is not enough context, respond with `NO_ANSWER`.

        **Web Context:**
        {% for document in web_documents %}
        ---
        **URL:** {{ document.meta.link }}
        {{ document.content }}
        {% endfor %}

        {% else %}
        You are an AI assistant for answering detailed technical questions about libraries like Pandas, NumPy, TensorFlow, PyTorch, LangChain, and Haystack.

        Here is the user's question:
        **"{{ query }}"**

        Below are documents retrieved from the internal documentation.

        **Documents:**
        {% for document in documents %}
        ---
        {{ document.content }}
        {% endfor %}

        **Instructions:**
        - If the question includes code or syntax, return:
          - A working Python example
          - An explanation of how and when to use it
        - Otherwise, answer clearly and directly.
        - Do not guess or invent answers. Say `NO_ANSWER` if unsure.
        {% endif %}
        """
    prompt = [ChatMessage.from_user(prompt_template)]

    log_message("Creating prompt...")

    main_routes = [
        {
            "condition": "{{'NO_ANSWER' in replies[0].text.replace('\n', '')}}",
            "output": "{{query}}",
            "output_name": "go_web",
            "output_type": str,
        },
        {
            "condition": "{{'NO_ANSWER' not in replies[0].text.replace('\n', '')}}",
            "output": "{{replies[0].text}}",
            "output_name": "answer",
            "output_type": str,
        },
    ]

    log_message("starting pipeline...")
    advanced_rag = Pipeline(max_runs_per_component=5)
    advanced_rag.add_component("embedder", SentenceTransformersTextEmbedder(model=EMBEDDING_MODEL))
    advanced_rag.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store, top_k=TOP_K))
    advanced_rag.add_component("prompt_builder", ChatPromptBuilder(template=prompt, required_variables=["query"]))
    advanced_rag.add_component("llm", GoogleAIGeminiChatGenerator(model=GENERATOR_MODEL))
    advanced_rag.add_component("web_search", SerperDevWebSearch())
    advanced_rag.add_component("router", ConditionalRouter(routes=main_routes))

    log_message("connecting components...")
    advanced_rag.connect("embedder", "retriever")
    advanced_rag.connect("retriever", "prompt_builder.documents")
    advanced_rag.connect("prompt_builder", "llm")
    advanced_rag.connect("llm.replies", "router.replies")
    advanced_rag.connect("router.go_web", "web_search.query")
    advanced_rag.connect("web_search.documents", "prompt_builder.web_documents")

    return advanced_rag


def process_query(pipeline, query):
    log_message(f"Processing query: {query}")
    try:
        result = pipeline.run({
            "embedder": {"text": query},
            "prompt_builder": {"query": query},
            "router": {"query": query}
        })

        log_message(f"Pipeline result keys: {list(result.keys())}")
        log_message(f"Router result: {result.get('router', {})}")

        router_result = result.get("router", {})
        if "answer" in router_result:
            return router_result["answer"]
        elif "go_web" in router_result:
            return f"Web taramasına yönlendirildi: {router_result['go_web']}"
        else:
            return "Yanıt üretilemedi. LLM yeterli bilgi bulamadı veya yönlendirme gerçekleşmedi."

    except Exception as e:
        log_message(f"Error processing query: {str(e)}", level="error")
        return f"Hata: {str(e)}"
