# 🇩🇪 DeutschNest — German Learning Assistant

DeutschNest is a web-based German learning tool built with **Python + Streamlit**, designed to help learners efficiently manage, review, and explore vocabulary, phrases, and sentences.

---

## Features

- **Cloud-based storage**: Uses Supabase for centralized data management (no local database required)
- **Automatic translation & parsing**: SpaCy for lemma/POS/tags, GoogleTranslator for optional translation
- **Semantic similarity & related entries**: Embedding-based suggestions using sentence-transformers
- **Flexible review modes**: Cloze deletion, reverse translation, and dictation
- **Batch import & search**: Add entries via text or CSV, filter by type or tags
- **Export options**: CSV or Anki deck (.apkg) for offline learning
- **Multi-language UI**: English, German, and Chinese supported

---

## Quick Start

1. **Create virtual environment**

```bash
python3 -m venv venv
```

2. **Activate environment**

macOS/Linux: `source venv/bin/activate`

Windows: `venv\Scripts\activate`

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install SpaCy German model**

```bash
python -m spacy download de_core_news_sm
```

5. **Run the app**

```bash
streamlit run app.py
```

Open your browser at http://localhost:8501.

## Usage Overview
- Add entries: Input German content and optional English translation; SpaCy parses lemma, POS, and tags automatically.

- Batch import: Paste text or upload CSV; supports automated parsing and embedding generation.

- Search & manage: Filter by keyword, type, or tags; edit or delete entries.

- Review: Select a mode (cloze, reverse, dictation) and optionally filter by tags. Track review counts and last-reviewed dates.

- Related entries: View top 5 semantically similar items for better context and learning.

- Export: Download all entries as CSV or Anki deck (.apkg).

## Tech Stack
- Python 3.8+, Streamlit

- Supabase for cloud database storage

- SpaCy for linguistic parsing

- GoogleTranslator for automatic translation

- sentence-transformers for embeddings and similarity

- pyttsx3 for text-to-speech dictation

- genanki for Anki deck creation