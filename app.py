"""
universal_analytics_app.py
Run in your terminal with: streamlit run universal_analytics_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="AutoData Dashboard", layout="wide")
st.title("📊 Universal Data Analytics & Dashboard Studio")

# 2. File Upload Widget (Accepts ANY CSV)
uploaded_file = st.file_uploader("Upload any CSV dataset to analyze:", type=["csv"])

if uploaded_file is not None:
    # 3. Ingest Data with Pandas
    df = pd.read_csv(uploaded_file)
    
    # 4. High-Level KPI Metric Cards
    st.subheader("Key Dataset Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rows", f"{len(df):,}")
    col2.metric("Total Columns", f"{len(df.columns)}")
    col3.metric("Duplicates Found", f"{df.duplicated().sum()}")
    col4.metric("Missing Values", f"{df.isnull().sum().sum()}")
    
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    # 5. Interactive Dashboard Controls
    st.divider()
    st.subheader("Interactive Visual Analytics")
    c1, c2 = st.columns(2)
    
    with c1:
        if categorical_cols:
            selected_cat = st.selectbox("Select Categorical Column:", categorical_cols)
            top_counts = df[selected_cat].value_counts().head(10).reset_index()
            top_counts.columns = [selected_cat, 'Count']
            fig_bar = px.bar(top_counts, x=selected_cat, y='Count', title=f"Top {selected_cat} Distribution", color=selected_cat)
            st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        if numeric_cols:
            selected_num = st.selectbox("Select Numeric Column:", numeric_cols)
            fig_hist = px.histogram(df, x=selected_num, title=f"Distribution of {selected_num}", nbins=20)
            st.plotly_chart(fig_hist, use_container_width=True)

    # 6. Data Preview & Cleaning
    st.divider()
    st.subheader("Dataset Preview")
    st.dataframe(df.head(50), use_container_width=True)
else:
    st.info("👆 Upload a CSV file above to generate instant KPIs and charts.")