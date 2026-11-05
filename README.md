# 📊 Automated Web Scraping & Data Analytics Pipeline

An end-to-end **ETL (Extract, Transform, Load) and Data Analytics Pipeline** built with Python, BeautifulSoup4, Pandas, SQLite, Plotly, and Streamlit.

This project automates the extraction of structured catalog data from e-commerce websites, cleans and validates fields, persists data into an embedded SQLite database, and presents actionable insights via an interactive dashboard.

---

## 🌟 Key Features
- **Automated Web Scraper:** Handles multi-page pagination, HTTP headers, timeout handling, and HTML parsing via BeautifulSoup4.
- **Data Cleansing & Transformation:** Cleans raw text, extracts numerical prices, standardizes ratings, and formats data frames using Pandas.
- **Embedded Database Persistence:** Saves and queries structured records using SQLite.
- **Interactive Analytics Dashboard:** Real-time KPI metric cards (Total Items, Average Price, 5-Star Share), Plotly box plots, and rating distribution charts.
- **Filtering & Search:** Real-time client-side search across titles.
- **One-Click Export:** Download clean, structured datasets in CSV format.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Web Scraping:** Requests, BeautifulSoup4, lxml
- **Data Manipulation:** Pandas, Regex
- **Database:** SQLite3
- **Visualization:** Plotly Express & Plotly Graph Objects
- **Dashboard Framework:** Streamlit

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/itztunio/python-data-automation-pipeline.git
cd python-data-automation-pipeline
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline & Dashboard
```bash
streamlit run app.py
```

---

## 📈 Architecture Overview
```
[ Target Website (HTML) ]
          │
          ▼ (Requests + BeautifulSoup4)
[ Raw HTML Extraction & Pagination ]
          │
          ▼ (Pandas Data Cleaning & Regex)
[ Structured DataFrame ]
          │
          ▼ (SQLite3 Engine)
[ Embedded Database Storage ]
          │
          ▼ (Plotly & Streamlit)
[ Interactive Analytics Dashboard & CSV Export ]
```

---

## 👤 Author
- **Ayesha Tunio**
- GitHub: [@itztunio](https://github.com/itztunio)
- LinkedIn: [Ayesha Tunio](https://linkedin.com/in/ayesha-tunio-6b2a88382)
