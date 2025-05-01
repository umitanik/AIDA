import streamlit as st
from scripts.indexing import create_document_store, build_indexing_pipeline, index_documents
from scripts.query_processing import build_query_pipeline, process_query
from scripts.utils import log_message

def main():
    st.set_page_config(page_title="AI Documentation Assistant", page_icon="🧠")

    st.title("🧠 AI Documentation Assistant")
    st.write("Pandas, NumPy, Scikit-learn veya Haystack hakkında teknik sorularınızı sorabilirsiniz!")

    # Durum kontrolü
    if "indexed" not in st.session_state:
        st.session_state.indexed = False
    if "document_store" not in st.session_state:
        st.session_state.document_store = None
    if "query_pipeline" not in st.session_state:
        st.session_state.query_pipeline = None

    # Belgeleri indeksleme butonu
    if st.button("📚 Belgeleri İndeksle") and not st.session_state.indexed:
        with st.spinner("Belgeler indiriliyor ve işleniyor..."):
            log_message("Indexleme başlatılıyor...")
            document_store = create_document_store()
            indexing_pipeline = build_indexing_pipeline(document_store)
            index_documents(indexing_pipeline)
            st.session_state.indexed = True
            st.session_state.document_store = document_store
            st.success("✅ İndeksleme tamamlandı!")

    # Eğer indeksleme tamamlandıysa sorgulama alanını göster
    if st.session_state.indexed:
        if st.session_state.query_pipeline is None:
            st.session_state.query_pipeline = build_query_pipeline(st.session_state.document_store)

        query = st.text_input("🔎 Bir soru sorun:")
        if st.button("🧠 Yanıtla") and query.strip():
            with st.spinner("Yanıt üretiliyor..."):
                response = process_query(st.session_state.query_pipeline, query)
                st.write("**🗨️ Yanıt:**")
                st.write(response)

if __name__ == "__main__":
    main()
