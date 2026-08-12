import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Duplicate Remover", page_icon="💦", layout="wide")
st.title("DataSpa - CSV Duplicate Remover")
st.write("Upload a CSV file -> Remove duplicate -> Get clean CSV file")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")   

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)

    st.subheader("Original Data")
    st.write(f"Total rows: **{len(df)}**")
    st.dataframe(df.head(10))
    
    # Remove duplicates
    cleaned_df = df.drop_duplicates()

    st.subheader("Cleaned Data")
    st.write(f"After Cleaning Total rows: **{len(cleaned_df)}**")
    st.write(f'Total duplicate rows removed: **{len(df) - len(cleaned_df)}**')
    st.dataframe(cleaned_df.head(10))
    
    # Download button
    csv_bytes = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleaned CSV",
        data=csv_bytes,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please! Upload a CSV to clean.")