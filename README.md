# 🧠 Emotion-Aware Support Chat Application

A full-stack web application that detects emotions in real time
using a fine-tuned DistilBERT model and generates empathetic
responses using GPT-4o-mini.

---

## 📋 Project Overview

This system is designed as an integrated framework providing
three core functionalities:

- **Real-time Emotion Classification** — DistilBERT model
  fine-tuned on the ISEAR dataset classifies user input into
  one of 7 emotion categories
- **Empathetic Dialogue Generation** — GPT-4o-mini generates
  context-aware responses tailored to the detected emotion
- **Emotion Tracking and Visualisation** — User interactions
  are stored over time and displayed as trends on a dashboard

---

## 🏗️ System Architecture

---

## 🤖 Models Used

| Model | Purpose | Dataset | Accuracy |
|---|---|---|---|
| CNN | Baseline emotion classification | ISEAR | ~65% |
| BiLSTM | Sequential emotion classification | ISEAR | ~54% |
| BERT | Transformer emotion classification | ISEAR | ~73% |
| DistilBERT | Final deployed model | ISEAR | ~70% |

The ISEAR (International Survey on Emotion Antecedents
and Reactions) dataset contains
7 emotion classes: joy, sadness, anger, fear, disgust,
shame and guilt.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| ML Model | DistilBERT (HuggingFace Transformers) |
| Response Generation | GPT-4o-mini (OpenAI) |
| Database | SQLite (SQLAlchemy ORM) |
| Model Serving | Google Colab GPU + ngrok |
| Language | Python 3 |

---

## 📁 Project Structure

---

## ⚙️ Setup and Installation

### Prerequisites
- Python 3.10+
- Google Account (for Colab)
- OpenAI API key with credits
- ngrok account (free)

### 1. Clone the Repository

```bash
git clone https://github.com/Gitau01Frank/emotion_app.git
cd emotion_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

### 4. Set Up the DistilBERT Model

The trained DistilBERT model must be saved in Google Drive:

---

## 🚀 Running the Application

The application requires three components running simultaneously:

### Step 1 — Start Colab Notebook

### Step 2 — Start FastAPI Backend

```bash
cd emotion_app/backend
uvicorn main:app --reload --port 8000
```

### Step 3 — Start Streamlit Frontend

```bash
cd emotion_app/frontend
python -m streamlit run app.py
```

### Step 4 — Open in Browser

---

## 📊 Features

### Chat Page
- Real time emotion detection with confidence score
- Probability breakdown for all 7 emotion classes
- Empathetic GPT-4o-mini response tailored to emotion
- Chat history maintained during session
- Colour coded emotion badges

### Dashboard Page
- Total message count metrics
- Emotion distribution pie chart
- Emotion frequency bar chart
- Emotion trend over time line chart
- Recent interactions table

---

## 🎭 Supported Emotions

| Emotion | Emoji | Description |
|---|---|---|
| Joy | 😊 | Happiness and positive feelings |
| Sadness | 😢 | Grief and sorrow |
| Anger | 😠 | Frustration and rage |
| Fear | 😨 | Anxiety and worry |
| Disgust | 🤢 | Repulsion and aversion |
| Shame | 😳 | Embarrassment and humiliation |
| Guilt | 😔 | Remorse and self-blame |

---

## 🗄️ Database Schema

---

## 📈 Model Performance

### DistilBERT (Deployed Model)

| Metric | Validation | Test |
|---|---|---|
| Accuracy | 67.5% | 70.5% |
| Precision | 68.0% | 71.2% |
| Recall | 67.5% | 70.5% |
| F1 Score | 67.4% | 70.4% |

### Per Class Performance (Test Set)

| Emotion | Precision | Recall | F1 |
|---|---|---|---|
| Joy | 0.87 | 0.91 | 0.89 |
| Fear | 0.74 | 0.82 | 0.78 |
| Disgust | 0.77 | 0.69 | 0.73 |
| Sadness | 0.76 | 0.69 | 0.72 |
| Guilt | 0.71 | 0.60 | 0.65 |
| Anger | 0.53 | 0.71 | 0.60 |
| Shame | 0.60 | 0.52 | 0.56 |

---

## ⚠️ Important Notes

- The ngrok URL changes every time you restart Colab
- Always update `COLAB_API_URL` in `.env` before starting
  the backend
- Keep the Colab notebook running while using the app
- The DistilBERT model files are not included in this
  repository due to size — see setup instructions above
- Never commit your `.env` file to GitHub

---

## 🔮 Future Improvements

- Add user authentication for personalised emotion tracking
- Integrate larger emotion dataset for improved accuracy
- Deploy to cloud platform for persistent availability
- Add voice input support
- Implement email or SMS mood reports
- Support for multiple languages

## 📄 License
MIT License

Copyright (c) 2026 Gitau01Frank

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---
