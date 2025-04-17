import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("Advanced Data File Converter & Cleaner.")
st.write("Easily upload CSV or Excel files, clean your data, and convert formats.")

user_files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files = True)

if user_files :
    for file in user_files :
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates files -{file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Files Removed")
            st.dataframe(df.head())

            if st.checkbox(f"Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace = True)
                st.success("Missing values fiiled with mean")
                st.dataframe(df.head())

            colums_selector = st.multiselect(f"Select Colums - {file.name}", df.columns, default = df.columns) 
            df = df[colums_selector]
            st.dataframe(df.head()) 

            if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include="number") .empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            choises = st.radio(f"Convert {file.name} to:", ["cnv", "Excel"], key=file.name)


            #Download Button

            if st.button(f"Download {file.name} as {choises}"):
                output = BytesIO()
                if choises == "csv":
                    df.to_csv(output, index=False)
                    mine = "text/csv"
                    new_name =file.name.replace(ext,"csv")

                else:
                    df.to_excel(output, index=False, engine='openpyxl')
                    mine = "application/vnd.openxmlforms-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("Download Button", file_name=new_name, data=output, mime=mine)
            
            st.success("Processing Complete")
                  

