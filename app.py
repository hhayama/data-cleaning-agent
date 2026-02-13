"""Streamlit interface for the Data Cleaning Agent."""

import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from data_cleaning_agent import LightweightDataCleaningAgent

load_dotenv()

st.set_page_config(page_title="Data Cleaning Agent", page_icon="🧹", layout="wide")
st.title("🧹 Data Cleaning Agent")

if 'output_visible' not in st.session_state:
    st.session_state.output_visible = False

def show_output():
    st.session_state.output_visible = True

# Add Streamlit UI elements
colheader1, colheader2 = st.columns(2)

with colheader1:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
with colheader2:
    user_instructions = st.text_area("Enter custom cleaning instructions. Leave blank for default cleaning steps.", label_visibility="visible")

if uploaded_file:
    # Load data
    df_raw = pd.read_csv(uploaded_file)
    show_debug_info = st.checkbox("Display debugging information after cleaning (generated function & prompt)", value=False, label_visibility="visible")

    # Clean button
    if st.button("Clean Data", on_click=show_output):
        with st.spinner("Cleaning..."):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            agent = LightweightDataCleaningAgent(model=llm, log=True)
            agent.invoke_agent(data_raw=df_raw, user_instructions=user_instructions)
            df_cleaned = agent.get_data_cleaned()
            
            st.success("Done!")

            # Compare the summary of the raw data and the cleaned data
            st.subheader("Summary of Raw and Cleaned Data")
            summary_df = df_cleaned.describe()

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Raw Data")
                st.table(df_raw.describe())
            with col2:
                st.subheader("Cleaned Data")
                st.table(summary_df)

            st.subheader("Cleaned Data")
            st.write(f"Shape: {df_cleaned.shape[0]} rows × {df_cleaned.shape[1]} columns")
            st.dataframe(df_cleaned.head())

            # Download
            csv = df_cleaned.to_csv(index=False)
            st.download_button(
                "Download Cleaned Data",
                data=csv,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

            # Display debugging information if enabled
            if show_debug_info and st.session_state.output_visible:
                st.subheader("Debug Information")

                debug_col1, debug_col2 = st.columns(2)
                with debug_col1:
                    debug_col1.subheader("Agent Generated Function")
                    st.code(agent.get_data_cleaner_function(), language="python")
                with debug_col2:
                    debug_col2.subheader("Message Used to Prompt the Agent")
                    st.code(agent.get_data_cleaner_prompt_message(), language="python")
                    # st.write(f"Default Instructions: \n\n {agent.get_data_cleaner_prompt_message()}")
                    # if user_instructions:
                    #     st.write(f"User Instructions: \n\n {user_instructions}")
                    # else:
                    #     st.write(f"Default Instructions: \n\n {agent.get_data_cleaner_prompt_message()}")
            