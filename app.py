import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scraper import scrape_catalog, get_persisted_data

# Page Setup
st.set_page_config(
    page_title="Automated Data Scraping & Analytics Pipeline",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-title">📊 Automated Data Scraping & Analytics Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">End-to-End ETL Pipeline: Web Scraping (BeautifulSoup) ➔ Cleaning & Transformation (Pandas) ➔ Storage (SQLite) ➔ Visualization (Plotly)</div>', unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920277.png", width=70)
    st.title("Pipeline Controls")
    
    pages_to_scrape = st.slider("Select Pages to Scrape", min_value=1, max_value=10, value=3)
    
    scrape_btn = st.button("🚀 Run Live Scraping Pipeline", use_container_width=True)
    st.markdown("---")
    st.caption("Tech Stack: Python, BeautifulSoup4, Pandas, SQLite, Plotly, Streamlit")

# Data loading logic
if scrape_btn:
    with st.spinner(f"Scraping live catalog across {pages_to_scrape} pages..."):
        df = scrape_catalog(num_pages=pages_to_scrape)
        st.session_state["dataset"] = df
        st.success(f"Pipeline executed successfully! Scraped {len(df)} records into SQLite.")
else:
    if "dataset" not in st.session_state:
        # Load from SQLite cache or perform initial scrape
        persisted = get_persisted_data()
        if not persisted.empty:
            st.session_state["dataset"] = persisted
        else:
            with st.spinner("Initializing default dataset..."):
                st.session_state["dataset"] = scrape_catalog(num_pages=3)

df = st.session_state.get("dataset", pd.DataFrame())

if not df.empty:
    # ----------------- Top KPI Metric Cards ----------------- #
    col1, col2, col3, col4 = st.columns(4)
    
    total_items = len(df)
    avg_price = df["Price_GBP"].mean()
    highest_price = df["Price_GBP"].max()
    five_star_pct = (len(df[df["Rating"] == 5]) / total_items) * 100
    
    col1.metric("📦 Total Items Scraped", f"{total_items}")
    col2.metric("💰 Average Price", f"£{avg_price:.2f}")
    col3.metric("🔝 Max Price", f"£{highest_price:.2f}")
    col4.metric("⭐ 5-Star Rating Share", f"{five_star_pct:.1f}%")
    
    st.markdown("---")
    
    # ----------------- Visualizations ----------------- #
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("📈 Price Distribution by Star Rating")
        fig_box = px.box(
            df,
            x="Rating",
            y="Price_GBP",
            color="Rating",
            points="all",
            labels={"Price_GBP": "Price (£)", "Rating": "Star Rating (1 to 5)"},
            title="Price Distribution across Rating Tiers"
        )
        fig_box.update_layout(showlegend=False, template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)
        
    with row1_col2:
        st.subheader("⭐ Rating Distribution")
        rating_counts = df["Rating"].value_counts().reset_index()
        rating_counts.columns = ["Rating", "Count"]
        rating_counts = rating_counts.sort_values(by="Rating")
        
        fig_bar = px.bar(
            rating_counts,
            x="Rating",
            y="Count",
            color="Rating",
            text="Count",
            labels={"Rating": "Star Rating", "Count": "Number of Books"},
            title="Book Count per Rating Tier"
        )
        fig_bar.update_layout(showlegend=False, template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # ----------------- Interactive Data Table ----------------- #
    st.markdown("---")
    st.subheader("📋 Clean Structured Dataset (Persisted in SQLite)")
    
    search_query = st.text_input("🔍 Search by Title...", "")
    filtered_df = df
    if search_query:
        filtered_df = df[df["Title"].str.contains(search_query, case=False, na=False)]
        
    st.dataframe(filtered_df, use_container_width=True, height=300)
    
    # ----------------- Data Export ----------------- #
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Clean Dataset as CSV",
        data=csv_data,
        file_name="scraped_catalog_clean.csv",
        mime="text/csv"
    )
else:
    st.warning("No data found. Click 'Run Live Scraping Pipeline' in the sidebar.")
