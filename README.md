# **AI Documentation Assistant**  |  **Yapay Zeka Dökümantasyon Asistanı**
<!-- Dil seçimi için butonlar (etiket gibi) -->
<p align="center">
  <a href="#en">🇬🇧 EN</a> |
  <a href="#tr">🇹🇷 TR</a>
</p>

# <a name="en"></a>🧠 AI Documentation Assistant (English)

**AI Documentation Assistant** is a Streamlit-based application that lets you ask advanced technical questions about
Python libraries (such as Pandas, Numpy, TensorFlow, PyTorch, LangChain, Haystack, and more). Powered by advanced RAG (
Retrieval-Augmented Generation), it retrieves trustworthy answers from official documentation and web sources.

## 🚀 Features

- **Automated Documentation Indexing:** Fetches, cleans, splits, and embeds documentation pages for fast QA.
- **Hybrid RAG Pipeline:** Answers with code examples and explanations based on context, using both internal docs and
  web search fallback if needed.
- **Web Search Fallback:** If documentation is insufficient, completes the answer using trusted web resources.
- **Code & Explanation Focus:** Responds with concise code samples and step-by-step explanations.
- **Modern UI:** Simple and intuitive interface built on Streamlit.

## 🛠️ Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **API Keys:**
    - Create a `.streamlit/secrets.toml` in your project root.
    - Add required keys:
      ```toml
      GOOGLE_API_KEY = "your-google-api-key"
      SERPERDEV_API_KEY = "your-serperdev-api-key"
      ```
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
4. The application will automatically download and index documentation on first run. Then, you can ask your questions!

## ⚙️ Configuration

- Documentation sources and model configs can be changed in `scripts/config.py`.
- Add new sources to `DOC_URLS` as needed.

## 🤖 Technologies Used

- [Streamlit](https://streamlit.io/)
- [Haystack](https://docs.haystack.deepset.ai/)
- [sentence-transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Serper.dev](https://serper.dev/) (web search)


---

# <a name="tr"></a>🧠 Yapay Zeka Dökümantasyon Asistanı (Türkçe)

**Yapay Zeka Dökümantasyon Asistanı**, Python kütüphaneleri (Pandas, Numpy, TensorFlow, PyTorch, LangChain, Haystack ve
diğerleri) hakkında teknik sorularınıza yanıtlar veren Streamlit tabanlı bir uygulamadır. Gelişmiş RAG (
Retrieval-Augmented Generation) altyapısı ile hem iç hem de web tabanlı dökümantasyonları tarayarak doğru ve güvenilir
cevaplar sunar.

## 🚀 Özellikler

- **Otomatik Dökümantasyon İndeksleme:** Dökümantasyon sayfalarını indirir, temizler, böler ve embed eder.
- **Hibrit RAG Pipeline:** Öncelikle iç dökümantasyonlarla, yetersiz kalırsa web arama ile sonuç üretir.
- **Web Arama Desteği:** Yeterli yanıt yoksa güvenilir web kaynaklarından destek alır.
- **Kod ve Açıklama Odaklı:** Kod örnekleri ve adım adım açıklamalarla yanıt verir.
- **Modern UI:** Kullanıcı dostu ve sade Streamlit arayüzü.

## 🛠️ Hızlı Başlangıç

1. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
2. **API Anahtarları:**
    - Proje kökünde `.streamlit/secrets.toml` oluşturun.
    - Şu anahtarları ekleyin:
      ```toml
      GOOGLE_API_KEY = "google-api-anahtarınız"
      SERPERDEV_API_KEY = "serperdev-api-anahtarınız"
      ```
3. **Uygulamayı başlatın:**
   ```bash
   streamlit run app.py
   ```
4. Uygulama ilk başlatıldığında dökümantasyonları indirir ve indeksler. Sonrasında sorularınızı sorabilirsiniz!

## ⚙️ Yapılandırma

- Dökümantasyon kaynaklarını ve model ayarlarını `scripts/config.py` dosyasından güncelleyebilirsiniz.
- `DOC_URLS` sabitine yeni kaynaklar ekleyebilirsiniz.

## 🤖 Kullanılan Teknolojiler

- [Streamlit](https://streamlit.io/)
- [Haystack](https://docs.haystack.deepset.ai/)
- [sentence-transformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Serper.dev](https://serper.dev/) (web arama)

---
