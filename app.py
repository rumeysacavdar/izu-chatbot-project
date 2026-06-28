import streamlit as st
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Ayarlar
load_dotenv()
client = OpenAI()
chroma_client = chromadb.PersistentClient(path="data/chroma_db")
collections = chroma_client.list_collections()
collection = chroma_client.get_collection(collections[0].name)

# DİL SÖZLÜĞÜ
translations = {
    "Türkçe": {
        "title": "🎓 İZÜ Akademik Asistanı",
        "placeholder": "Sorunuzu buraya yazın...",
        "welcome": "Merhaba! Size nasıl yardımcı olabilirim?"
    },
    "English": {
        "title": "🎓 IZU Academic Assistant",
        "placeholder": "Type your question here...",
        "welcome": "Hello! How can I help you today?"
    }
}

def ask_question(question, lang):
    embedding = client.embeddings.create(model="text-embedding-3-small", input=question).data[0].embedding
    
    # n_results değerini 40 yaparak geniş bir havuz çekiyoruz
    results = collection.query(query_embeddings=[embedding], n_results=30)
    
    documents = results["documents"][0] if results["documents"] and results["documents"][0] else []
    
    # --- YAZILIMSAL FİLTRELEME BAŞLANGICI ---
    # Kullanıcı yüksek lisans veya doktora sormadıysa, yüksek lisans içeren dökümanları Python seviyesinde eliyoruz
    clean_documents = []
    is_graduate_query = any(word in question.lower() for word in ["yüksek", "tezli", "tezsiz", "doktora", "master", "phd"])
    
    if not is_graduate_query:
        for doc in documents:
            # İçinde yüksek lisans veya tez kelimeleri geçen parçaları veriden tamamen çöpe atıyoruz
            if "tezli" not in doc.lower() and "tezsiz" not in doc.lower() and "yüksek lisans" not in doc.lower():
                clean_documents.append(doc)
    else:
        clean_documents = documents
        
    context = "\n---\n".join(clean_documents)
    # --- YAZILIMSAL FİLTRELEME BİTİŞİ ---

    prompt = f"""
    Sen İstanbul Sabahattin Zaim Üniversitesi (İZÜ) akademik asistanısın.
    Kullanıcının seçtiği dil: {lang}
    
    Talimatlar: 
    1. Cevabını SADECE {lang} dilinde ver.
    2. KESİNLİKLE toplama işlemi yapma, verideki sayıları olduğu gibi listele.
    3. Ders programı sorulursa tablo veya liste şeklinde göster.
    4. Verdiğin HER CEVABIN EN SONUNA: "Olası yanlış cevaplar veya güncel değişiklikler için lütfen İZÜ resmi web sitesini kontrol ediniz." cümlesini ekle.
    
    BİLGİLER: {context}
    SORU: {question}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# Arayüz Yapılandırması
st.set_page_config(page_title="İZÜ Asistan", page_icon="🎓")

# DİL SEÇİCİ - Dünya ikonunu doğrudan selectbox içinde gösteriyoruz
# label_visibility="visible" yaparak "🌐" yazısının görünmesini sağladık
lang_choice = st.selectbox("🌐 Dil / Language", ["Türkçe", "English"])

# Metinleri belirle
t = translations[lang_choice]

st.title(t["title"])

# Mesaj geçmişini başlat/güncelle
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": t["welcome"]}]
else:
    if st.session_state.messages[0]["content"] in [translations["Türkçe"]["welcome"], translations["English"]["welcome"]]:
        st.session_state.messages[0]["content"] = t["welcome"]

# Mesajları ekrana çiz (Streamlit bunu otomatik sağ/sol yapar)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Yeni kullanıcı girdisi
if user_input := st.chat_input(t["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = ask_question(user_input, lang_choice)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})