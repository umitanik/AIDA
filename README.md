# 🧠 AI Dokümantasyon Asistanı

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red) ![Haystack](https://img.shields.io/badge/Haystack-2.0-green)

## 📑 Proje Hakkında

AI Dokümantasyon Asistanı, Python kütüphaneleri hakkında teknik sorularınızı yanıtlayan yapay zeka destekli bir araçtır.
Pandas, NumPy, scikit-learn ve Haystack gibi popüler kütüphanelerin dokümantasyonlarını analiz ederek sorularınıza hızlı
ve doğru yanıtlar üretir.


## ✨ Özellikler

- 🔍 **Akıllı Arama**: Dokümanlar arasında anlam tabanlı arama
- 💡 **Kod Örnekleri**: Sorularınıza uygun kod parçaları oluşturma
- 🌐 **Web Destekli**: Yerel dokümanlarda yeterli bilgi bulunamadığında web araması yapma
- 🤖 **Google Gemini AI**: Güncel AI teknolojisi ile doğru ve anlaşılır yanıtlar
- 🔄 **Gerçek Zamanlı**: Anında yanıt üretimi

## 🚀 Kurulum

### Gereksinimler

```bash
# requirements.txt dosyasını oluşturun
pip install -r requirements.txt
```

### API Anahtarları

`.streamlit/secrets.toml` dosyasında API anahtarlarınızı tanımlayın:

```toml
GOOGLE_API_KEY = "sizin_google_api_anahtariniz"
SERPERDEV_API_KEY = "sizin_serperdev_api_anahtariniz"
```

## 🎮 Kullanım

Uygulamayı başlatmak için:

```bash
streamlit run app.py
```

Uygulama başladığında:

1. Dokümanlar otomatik olarak indirilip işlenecektir
2. Metin kutusuna sorunuzu yazın
3. "Yanıtla" butonuna tıklayın
4. AI destekli yanıtınızı alın!

## 🧩 Mimari

Bu proje aşağıdaki ana bileşenlerden oluşur:

- **Dokümantasyon İndeksleme**: Haystack kullanarak dokümanları işler ve vektör veritabanında saklar
- **Sorgulama İşleme**: Kullanıcı sorularını analiz eder ve ilgili dokümanları çeker
- **Yanıt Üretimi**: Google Gemini AI ile anlaşılır ve doğru yanıtlar üretir

## 🛠️ Teknik Detaylar

- **Frontend**: Streamlit
- **Veritabanı**: Haystack InMemoryDocumentStore
- **Embedding Modeli**: SentenceTransformers (msmarco-distilbert-base-v4)
- **LLM**: Google Gemini 2.0 Flash

---