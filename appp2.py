import streamlit as st
import PyPDF2
import io
import openai
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
import pdfplumber

openai.api_key = "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"

def pdf_to_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

st.title("PDF-based Chatbot")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Extracting text from the PDF..."):
        pdf_text = pdf_to_text(io.BytesIO(uploaded_file.getbuffer()))

    # Truncate the text before using it as a prompt
    pdf_text = pdf_text[:10000]

    st.success("PDF processed successfully. You can now use the chatbot.")

    user_message = st.text_input("Ask a question related to the PDF content:")

    def openai_chat(pdf_text, user_message, max_completion_tokens=100):
        # Combine the truncated pdf_text with the user_message
        prompt = f"PDF Content: {pdf_text}\nQuestion: {user_message}\nAnswer:"

        # Generate a response using OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=max_completion_tokens,
            n=1,
            stop=None,
            temperature=0.5
        )

        # Extract the response text
        answer = response.choices[0].text.strip()
        return answer

    def is_answer_related(pdf_text, answer):
        pdf_words = set(pdf_text.lower().split())
        answer_words = set(answer.lower().split())
        return len(pdf_words.intersection(answer_words)) > 0

    if st.button("Submit"):
        with st.spinner("Generating response..."):
            answer = openai_chat(pdf_text, user_message)
            if is_answer_related(pdf_text, answer):
                st.write(answer)
            else:
                st.write("The answer to your question is beyond the scope of this PDF.")
else:
    st.warning("Please upload a PDF file to begin.")
