#Gerekli Kütüphaneler
from gradio.helpers import log_message
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder


from scripts.config import DOC_URLS, EMBEDDING_MODEL, SPLIT_LENGTH, SPLIT_OVERLAP, TOP_K


def create_document_store():
    """
    Create an in-memory document store.
    """
    log_message("Creating document store...", title="Document Store")
    document_store = InMemoryDocumentStore()
    return document_store

def build_indexing_pipeline(document_store):
    """
    Build the indexing pipeline.
    """
    log_message("Building indexing pipeline...", title="Pipeline")

    pipeline = Pipeline()
    pipeline.add_component(instance=LinkContentFetcher(), name="fetcher")
    pipeline.add_component(instance=HTMLToDocument(), name="converter")
    pipeline.add_component(instance=DocumentCleaner(), name="cleaner")
    pipeline.add_component(instance=DocumentSplitter(split_length=SPLIT_LENGTH, split_overlap=SPLIT_OVERLAP), name="splitter")
    pipeline.add_component(instance=SentenceTransformersDocumentEmbedder(model=EMBEDDING_MODEL), name="embedder")
    pipeline.add_component(instance=DocumentWriter(document_store), name="writer")

    pipeline.connect("fetcher.streams", "converter.sources")
    pipeline.connect("converter.documents", "cleaner")
    pipeline.connect("cleaner", "splitter")
    pipeline.connect("splitter", "embedder")
    pipeline.connect("embedder", "writer")

    return pipeline

def index_documents(pipeline):
    """
    Index documents from the specified URLs.
    """
    log_message("Indexing documents...", title="Index")
    try:
        pipeline.run({"fetcher": {"urls": DOC_URLS}})
        log_message(f"Successfully indexed {len(DOC_URLS)} documentation pages.", title="Indexing Complete")
    except Exception as e:
        log_message(f"Error during indexing: {str(e)}", title="Indexing Error")
