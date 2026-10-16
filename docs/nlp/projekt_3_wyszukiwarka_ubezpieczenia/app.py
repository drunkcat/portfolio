from pathlib import Path
import re
import unicodedata

import pandas as pd
import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Wyszukiwarka ubezpieczeń", page_icon="🔎")

PROJECT_DIR = Path(__file__).resolve().parent
PDF_PATH = PROJECT_DIR / "zrodlo_poradnik_ubezpieczenia-mieszkaniowe-1.pdf"
TXT_PATH = PROJECT_DIR / "zrodlo_rf_gov_pl_odszkodowania_po_wichurach.txt"

SOURCE_DESCRIPTIONS = {
    0: "Ubezpieczenia mieszkaniowe. Jak się dobrze ubezpieczyć? (Rzecznik Finansowy, 2026)",
    1: "Odszkodowania po wichurach w pytaniach i odpowiedziach (Rzecznik Finansowy, 2022)",
}

SOURCE_TEXT_TITLES = {
    0: "Ubezpieczenia mieszkaniowe Jak się dobrze ubezpieczyć?",
    1: "Odszkodowania po wichurach w pytaniach i odpowiedziach - Rzecznik Finansowy",
}


def clean_text(text, source_title_code):
    """Porządkuje odstępy i usuwa kilka technicznych elementów źródła."""
    text = unicodedata.normalize("NFC", str(text))
    text = text.replace("\xa0", " ").replace("\xad", "")
    text = re.sub(r"(?im)^Strona źródłowa:.*$", " ", text)
    text = re.sub(r"(?m)^\s*\d+\s*$", " ", text)
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(SOURCE_TEXT_TITLES[source_title_code], " ")
    return text.strip()


def split_into_chunks(text, chunk_size=900, overlap=120):
    """Dzieli tekst w pobliżu granicy słowa i zachowuje niewielki overlap."""
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            space_position = text.rfind(" ", start, end)
            if space_position > start:
                end = space_position

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)
        while start < len(text) and text[start].isspace():
            start += 1

    return chunks


@st.cache_resource(show_spinner="Wczytuję dokumenty i przygotowuję wyszukiwarkę...")
def load_search_index():
    """Wczytuje materiały, dzieli je na fragmenty i buduje prosty indeks TF-IDF."""
    documents = []

    pdf_reader = PdfReader(str(PDF_PATH))
    for page_number, page in enumerate(pdf_reader.pages, start=1):
        documents.append(
            {
                "source_id": "RF-HOME-2026",
                "source_title": 0,
                "page": page_number,
                "text": page.extract_text() or "",
            }
        )

    web_text = TXT_PATH.read_text(encoding="utf-8")
    documents.append(
        {
            "source_id": "RF-STORM-2022",
            "source_title": 1,
            "page": None,
            "text": web_text,
        }
    )

    chunk_records = []
    for document in documents:
        cleaned_text = clean_text(document["text"], document["source_title"])

        for chunk_number, chunk in enumerate(split_into_chunks(cleaned_text), start=1):
            chunk_records.append(
                {
                    "source_id": document["source_id"],
                    "source_title": document["source_title"],
                    "page": document["page"],
                    "chunk_number": chunk_number,
                    "text": chunk,
                }
            )

    chunks = pd.DataFrame(chunk_records)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(chunks["text"])
    return chunks, vectorizer, tfidf_matrix


def search_answers(question, chunks, vectorizer, tfidf_matrix, top_n=3):
    """Zwraca fragmenty o najwyższym podobieństwie do pytania."""
    question_vector = vectorizer.transform([question])
    scores = cosine_similarity(question_vector, tfidf_matrix).flatten()

    results = chunks.copy()
    results["similarity"] = scores
    results = results[results["similarity"] > 0]
    return results.sort_values("similarity", ascending=False).head(top_n)


st.title("Wyszukiwarka informacji o ubezpieczeniu domu")
st.write(
    "Wpisz pytanie o ubezpieczenie domu lub mieszkania. Aplikacja wyszuka "
    "pasujące fragmenty w dwóch materiałach Rzecznika Finansowego."
)
st.info(
    "To prosta wyszukiwarka tekstowa, nie chatbot. Pokazuje fragmenty źródeł, "
    "a nie indywidualną poradę ubezpieczeniową ani prawną."
)

missing_files = [path.name for path in (PDF_PATH, TXT_PATH) if not path.exists()]
if missing_files:
    st.error("Brakuje plików źródłowych: " + ", ".join(missing_files))
    st.stop()

chunks, vectorizer, tfidf_matrix = load_search_index()
st.caption(f"Wyszukiwarka przeszukuje {len(chunks)} fragmentów tekstu.")

with st.form("search_form"):
    question = st.text_input(
        "Twoje pytanie",
        placeholder="Np. Czy powódź zawsze jest objęta polisą mieszkaniową?",
    )
    submitted = st.form_submit_button("Szukaj")

if submitted:
    if not question.strip():
        st.warning("Wpisz pytanie, zanim rozpoczniesz wyszukiwanie.")
    else:
        results = search_answers(question, chunks, vectorizer, tfidf_matrix)

        if results.empty:
            st.warning("Nie znaleziono pasujących fragmentów w dostępnych źródłach.")
        else:
            st.subheader("Najbardziej pasujące fragmenty")

            for result_number, (_, result) in enumerate(results.iterrows(), start=1):
                source_description = SOURCE_DESCRIPTIONS[result["source_title"]]
                st.markdown(f"### Wynik {result_number}")
                if pd.notna(result["page"]):
                    location = f"Strona {int(result['page'])}"
                else:
                    location = "Artykuł internetowy"
                st.caption(
                    f"{source_description} · {location} · "
                    f"podobieństwo: {result['similarity']:.3f}"
                )
                st.write(result["text"])
                st.markdown("---")

st.caption(
    "Wyniki szereguje TF-IDF. Podobieństwo słów nie gwarantuje, że fragment "
    "w pełni odpowiada na pytanie."
)
