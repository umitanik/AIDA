# Dökümantasyon URL' leri
DOC_URLS = [
    "https://pandas.pydata.org/docs/user_guide/indexing.html",
    "https://pandas.pydata.org/docs/user_guide/visualization.html",
    "https://pandas.pydata.org/docs/user_guide/cookbook.html",
    "https://pandas.pydata.org/docs/user_guide/merging.html",
    "https://numpy.org/doc/stable/reference/random/index.html",
    "https://numpy.org/doc/stable/reference/arrays.indexing.html",
    "https://scikit-learn.org/stable/modules/linear_model.html",
    "https://scikit-learn.org/stable/modules/clustering.html",
    "https://docs.haystack.deepset.ai/docs/pipelines",
    "https://docs.haystack.deepset.ai/docs/retriever",
    "https://haystack.deepset.ai/tutorials/27_first_rag_pipeline",
    "https://haystack.deepset.ai/tutorials/43_building_a_tool_calling_agent",
    "https://haystack.deepset.ai/tutorials/40_building_chat_application_with_function_calling",
]

# Model ayarları
EMBEDDING_MODEL = "sentence-transformers/msmarco-distilbert-base-v4"
#EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
GENERATOR_MODEL = "gemini-2.0-flash"

# Pipeline ayarları
SPLIT_LENGTH = 100
SPLIT_OVERLAP = 10
TOP_K = 3

