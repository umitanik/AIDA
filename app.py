"""
Main application file for AI Documentation Assistant.
Sets up the Streamlit interface and integrates indexing and query processing.
"""

import streamlit as st
from scripts.indexing import create_document_store, build_indexing_pipeline, index_documents
from scripts.query_processing import build_query_pipeline, process_query
from scripts.utils import log_message


def main():
    """
    Main function to set up and run the AI Documentation Assistant application.
    """
    # Başlık ve açıklama
    st.title("AI Documentation Assistant")
    st.write("Pandas, NumPy, Scikit-learn veya Haystack hakkında sorularınızı sorabilirsiniz!")

    # DocumentStore ve Indexing
    log_message("Starting application...")
    document_store = create_document_store()
    indexing_pipeline = build_indexing_pipeline(document_store)
    index_documents(indexing_pipeline)

    # Query Pipeline
    query_pipeline = build_query_pipeline(document_store)

    # Kullanıcı arayüzü
    query = st.text_input("Destek almak istediğiniz konu ile ilgili bir soru girin:")

    if st.button("Yanıtla"):

        with st.spinner("Yanıt üretiliyor..."):
            response = process_query(query_pipeline, query)
            st.write("**Yanıt:**")
            st.write(response)
            # clean up streamlit
            st.session_state.query = ""


if __name__ == "__main__":
    main()