import streamlit as st
import pandas as pd
# streamlit run app.py

st.set_page_config(page_title="CSV Duplicate Remover", page_icon="💦", layout="wide")
st.title("DataSpa - CSV Duplicate Remover")
st.write("Upload a CSV file -> Remove duplicate -> Get clean CSV file")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv","xlsx"])   


if uploaded_file is not None:
    # Read the uploaded file
    file_name = uploaded_file.name
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.stop()

    st.subheader("Original Data")
    st.write(f"Total rows: **{len(df)}** | Total columns: **{len(df.columns)}**")
    st.dataframe(df.head(10))

    # basic stats
    st.subheader("Basic Statistics")
    st.dataframe(df.describe())

    # missing values
    st.subheader("Missing Values")
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if len(missing_values) > 0:
        st.write("Columns with missing values:")
        st.dataframe(missing_values)
    else:
        st.write("No missing values found.")

    # Handle Missing Values
    option = st.radio(
        "Choose how to handle missing values:",
        ("Do nothing", "Drop missing value rows", "Fill Mean", "Fill Median", "Fill Mode")
    )
    cleaned_df = df.copy()

    if option == "Drop missing value rows":
        cleaned_df = cleaned_df.dropna()
        st.info("Dropped rows with missing values.")

    elif option == "Fill Mean":
        numeric_cols = cleaned_df.select_dtypes(include='number').columns
        for col in numeric_cols:
            mean_value = cleaned_df[col].mean()
            cleaned_df[col].fillna(mean_value, inplace=True)
        st.info("Filled missing values with mean for numeric columns.")

    elif option == "Fill Median":
        numeric_cols = cleaned_df.select_dtypes(include='number').columns
        for col in numeric_cols:
            median_value = cleaned_df[col].median()
            cleaned_df[col].fillna(median_value, inplace=True)
        st.info("Filled missing values with median for numeric columns.")

    elif option == "Fill Mode":
        for col in cleaned_df.columns:
            mode_value = cleaned_df[col].mode()[0]
            cleaned_df[col].fillna(mode_value, inplace=True)
        st.info("Filled missing values with mode for all columns.")

    # ---------- NEW: Select Columns for Duplicate Check ----------
    st.subheader("Remove Duplicates")
    columns = cleaned_df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to check for duplicates (if none selected, all columns will be used):",
        options = columns,
        default=[]
    )
    before = len(cleaned_df)

    if selected_columns:
        cleaned_df = cleaned_df.drop_duplicates(subset=selected_columns)
        st.info(f"Removed duplicates based on selected columns: {', '.join(selected_columns)}")
    else:
        cleaned_df = cleaned_df.drop_duplicates()
        st.info("Removed duplicates based on all columns.")
        
    after = len(cleaned_df)
    st.write(f"Duplicates removed: **{before - after}**")
    st.write(f"Final rows: **{after}**")

   # ---------- Final Data ----------
    st.subheader("Final Cleaned Data (First 10 rows)")
    st.dataframe(cleaned_df.head(10))
    
    # Download button
    csv = cleaned_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please! Upload a CSV or Excel to clean.")
