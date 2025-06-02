import streamlit as st
import time
from scripts.indexing import create_document_store, build_indexing_pipeline, index_documents
from scripts.query_processing import build_query_pipeline, process_query
from scripts.utils import log_message, get_indexing_progress

# UI metinleri için çeviri sözlüğü
UI_TEXTS = {
    "en": {
        "title": "🧠 AI Documentation Assistant",
        "subtitle": "Ask technical questions about Python libraries!",
        "settings": "Settings",
        "reindex": "🔄 Re-index Documents",
        "ask": "🔎 Ask a question:",
        "answer": "🧠 Answer",
        "answering": "Generating answer...",
        "response": "**🗨️ Response:**",
        "history": "📜 Question History",
        "question": "Question",
        "indexing": "Documents are being downloaded and processed...",
        "indexing_started": "Indexing started...",
        "indexing_complete": "✅ Indexing completed!",
        "indexing_error": "❌ An error occurred during indexing. Please try again.",
        "status": "Status:",
        "processing": "Processing:",
        "api_error": "⚠️ API keys are missing or invalid. Please check your .streamlit/secrets.toml file.",
        "api_info": "Follow the instructions in the README.md file to set up your API keys.",
        "language": "Language"
    },
    "tr": {
        "title": "🧠 Yapay Zeka Dökümantasyon Asistanı",
        "subtitle": "Yapay zeka hakkında teknik sorularınızı sorabilirsiniz!",
        "settings": "Ayarlar",
        "reindex": "🔄 Belgeleri Yeniden İndeksle",
        "ask": "🔎 Bir soru sorun:",
        "answer": "🧠 Yanıtla",
        "answering": "Yanıt üretiliyor...",
        "response": "**🗨️ Yanıt:**",
        "history": "📜 Soru Geçmişi",
        "question": "Soru",
        "indexing": "Belgeler indiriliyor ve işleniyor...",
        "indexing_started": "Indexleme başlatılıyor...",
        "indexing_complete": "✅ İndeksleme tamamlandı!",
        "indexing_error": "❌ İndeksleme sırasında bir hata oluştu. Lütfen tekrar deneyin.",
        "status": "Durum:",
        "processing": "İşleniyor:",
        "api_error": "⚠️ API anahtarları eksik veya hatalı. Lütfen .streamlit/secrets.toml dosyasını kontrol edin.",
        "api_info": "API anahtarlarını ayarlamak için README.md dosyasındaki talimatları izleyin.",
        "language": "Dil"
    }
}

def main():
    st.set_page_config(page_title="AI Documentation Assistant", page_icon="🧠")

    # Dil seçimi için session state
    if "language" not in st.session_state:
        st.session_state.language = "tr"  # Varsayılan dil Türkçe

    # Sidebar for settings and controls
    with st.sidebar:
        st.header(UI_TEXTS[st.session_state.language]["settings"])

        # Dil seçimi
        selected_lang = st.selectbox(
            UI_TEXTS[st.session_state.language]["language"],
            options=["Türkçe 🇹🇷", "English 🇬🇧"],
            index=0 if st.session_state.language == "tr" else 1
        )

        # Dil değişikliğini işle
        new_lang = "tr" if selected_lang == "Türkçe 🇹🇷" else "en"
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.experimental_rerun()

        # Yeniden indeksleme butonu
        if st.button(UI_TEXTS[st.session_state.language]["reindex"]):
            st.session_state.indexed = False
            st.session_state.document_store = None
            st.session_state.query_pipeline = None
            st.experimental_rerun()

    # Seçilen dile göre metinleri al
    texts = UI_TEXTS[st.session_state.language]

    # Ana başlık ve alt başlık
    st.title(texts["title"])
    st.write(texts["subtitle"])

    # Durum kontrolü
    if "indexed" not in st.session_state:
        st.session_state.indexed = False
    if "document_store" not in st.session_state:
        st.session_state.document_store = None
    if "query_pipeline" not in st.session_state:
        st.session_state.query_pipeline = None
    if "history" not in st.session_state:
        st.session_state.history = []

    if not st.session_state.indexed:
        log_message(texts["indexing_started"])
        document_store = create_document_store()
        indexing_pipeline = build_indexing_pipeline(document_store)

        # İlerleme çubuğu ve durum mesajları
        progress_bar = st.progress(0)
        status_text = st.empty()
        url_text = st.empty()

        with st.spinner(texts["indexing"]):
            # İndeksleme işlemini başlat (bu işlem arka planda log_message çağrıları yapacak)
            indexing_started = True
            success = False

            # İndeksleme işlemini başlat
            try:
                success = index_documents(indexing_pipeline)
            except Exception as e:
                log_message(f"İndeksleme hatası: {str(e)}", level="error")
                success = False

            # İlerleme durumunu göster
            last_progress = 0
            while last_progress < 1.0:
                progress, url, status = get_indexing_progress()
                # Eğer ilerleme değişmişse güncelle
                if progress > last_progress:
                    progress_bar.progress(progress)
                    last_progress = progress

                status_text.text(f"{texts['status']} {status}")
                if url:
                    url_text.text(f"{texts['processing']} {url}")

                # İndeksleme tamamlandıysa döngüden çık
                if success and progress >= 0.99:
                    break

                time.sleep(0.1)

            # Son durumu göster
            progress_bar.progress(1.0)

            if success:
                st.session_state.indexed = True
                st.session_state.document_store = document_store
                st.success(texts["indexing_complete"])
            else:
                st.error(texts["indexing_error"])

    # Eğer indeksleme tamamlandıysa sorgulama alanını göster
    if st.session_state.indexed:
        if st.session_state.query_pipeline is None:
            st.session_state.query_pipeline = build_query_pipeline(st.session_state.document_store)

        # API anahtarları eksikse hata mesajı göster
        if st.session_state.query_pipeline is None:
            st.error(texts["api_error"])
            st.info(texts["api_info"])
        else:
            query = st.text_input(texts["ask"])
            if st.button(texts["answer"]) and query.strip():
                with st.spinner(texts["answering"]):
                    response = process_query(st.session_state.query_pipeline, query)
                    st.write(texts["response"])
                    st.write(response)

                    # Sorgu ve yanıtı geçmişe ekle
                    st.session_state.history.append({"query": query, "response": response})

            # Geçmiş sorguları göster
            if st.session_state.history:
                with st.expander(texts["history"], expanded=False):
                    for i, item in enumerate(reversed(st.session_state.history)):
                        st.markdown(f"**{texts['question']} {len(st.session_state.history) - i}:** {item['query']}")
                        st.markdown(f"**{texts['response'].replace('*', '')} {len(st.session_state.history) - i}:** {item['response']}")
                        if i < len(st.session_state.history) - 1:
                            st.markdown("---")

if __name__ == "__main__":
    main()
