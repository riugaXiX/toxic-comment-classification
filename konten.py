import streamlit as st
from streamlit_lottie import st_lottie
import plotly.express as px
import pandas as pd
from openai import OpenAI
import os
import shutil
from io import BytesIO
from audio_preprocess import AudioProcessor

class Konten:
    def __init__(self, dashboard_name, analisis, prediksi, dataset, animation):
        self.dashboard_name = dashboard_name
        self.analisis = analisis
        self.prediksi = prediksi
        self.dataset = dataset
        self.animation = animation
        self.client_OpenAi = OpenAI(api_key='your_api_key')
        self.audio_processor = AudioProcessor('output/lstmModel.keras', 'output/tokenizer.pkl')
    
    
    def dashboard(self):
        with st.container():
            leftSide, rightSide = st.columns(2)
            with leftSide:
                st.subheader("Hallo, Rizky :wave:")
                st.title("Toxic Comment Classification")
                st.write("Di website ini kamu dapat Melakukan prediksi untuk mengklasifikasikan sebuah text yang ter indikasi toxic")
                st.write("Dengan beberapa fitur menarik seperti speech to text, prediksi melalui csv, dan textarea biasa")
            with rightSide:
                st_lottie(self.animation, height=300, key="coding")

    def show_charts(self):
        # Sample data
        data = {
            'Category': ['pornografi', 'sara', 'radikalisme', 'pencemaran_nama_baik'],
            'Count': [69, 102, 88, 136]
        }
        df = pd.DataFrame(data)
        
        # Display summary boxes
        with st.container():
            st.markdown("### Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Users", "4")
            col2.metric("Dataset Size", "200")
            col3.metric("Category 1", "69")
            col4.metric("Category 2", "102")
        
        # Bar chart
        bar_chart = px.bar(df, x='Category', y='Count', title='Count of Each Category')
        
        # Pie chart
        pie_chart = px.pie(df, names='Category', values='Count', title='Proportion of Each Category')

        # Display charts
        st.plotly_chart(bar_chart)
        st.plotly_chart(pie_chart)


    def dts(self, df_dataset):
        try:
            df = pd.read_csv(df_dataset)
            st.dataframe(df)
        except FileNotFoundError:
            st.error("File 'selected_samples.csv' tidak ditemukan. Pastikan file tersedia di direktori yang benar.")

    def cs_folding(self, df_casefolding):
        try:
            df = pd.read_csv(df_casefolding)
            # st.dataframe(df)
            st.subheader('Sebelum di lakukan case folding')
            st.dataframe(df['original_text'], width=1000, height=400)
            st.subheader('Setelah di lakukan Case Folding')
            st.dataframe(df['lemmatized_text'], width=1000, height=400)

        except FileNotFoundError:
            st.error("File 'selected_samples.csv' tidak ditemukan. Pastikan file tersedia di direktori yang benar.")


    def tknz(self, df_casefolding):
        try:
            df = pd.read_csv(df_casefolding)
            # st.dataframe(df)
            st.subheader('Sebelum di lakukan Tokenizing')
            st.dataframe(df['original_text'], width=1000, height=400)
            st.subheader('Setelah di lakukan Tokenizing')
            st.dataframe(df['tokenized_text'], width=1000, height=400)

        except FileNotFoundError:
            st.error("File 'selected_samples.csv' tidak ditemukan. Pastikan file tersedia di direktori yang benar.")


    def swr(self, df_casefolding):
        try:
            df = pd.read_csv(df_casefolding)
            # st.dataframe(df)
            st.subheader('Sebelum di lakukan Stopword removal')
            st.dataframe(df['original_text'], width=1000, height=400)
            st.subheader('Setelah di lakukan Stopword removal')
            st.dataframe(df['stopword_tokenized'], width=1000, height=400)

        except FileNotFoundError:
            st.error("File 'selected_samples.csv' tidak ditemukan. Pastikan file tersedia di direktori yang benar.")


    def lemma(self, df_casefolding):
        try:
            df = pd.read_csv(df_casefolding)
            # st.dataframe(df)
            st.subheader('Sebelum di lakukan Lemmatisasi')
            st.dataframe(df['original_text'], width=1000, height=400)
            st.subheader('Setelah di lakukan Lemmatisasi')
            st.dataframe(df['lemmatized_text'], width=1000, height=400)

        except FileNotFoundError:
            st.error("File 'selected_samples.csv' tidak ditemukan. Pastikan file tersedia di direktori yang benar.")


    def prdks(self):
        st.title("Prediksi Toxic Comment")

                # Audio to Text
        # Direktori folder audio
        audio_folder = 'audio'

        st.header("Audio to Text")
        audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg"])

        if audio_file is not None:
            try:
                recognized_text = self.audio_processor.transcribe_audio(audio_file)
                
                if recognized_text:
                    st.write("Recognized Text:")
                    st.write(f"textnya adalah: {recognized_text}")
                    st.write(self.audio_processor.predict_toxicity(recognized_text))
                else:
                    st.error("Failed to transcribe audio.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        # Text Area
        st.header("Text Area")
        text_input = st.text_area("Enter Text")
        if st.button("Predict from Text Area"):
            if text_input:
                # Implement prediction function here
                st.write("Predicted result for the input text")

        # CSV Input
        st.header("CSV Input")
        csv_file = st.file_uploader("Upload CSV File", type=["csv"])
        if csv_file is not None:
            df = pd.read_csv(csv_file)
            st.dataframe(df)
            if st.button("Predict from CSV"):
                # Implement prediction function here
                st.write("Predicted results for the uploaded CSV")
    