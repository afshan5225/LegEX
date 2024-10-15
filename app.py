import os
import streamlit as st
from langchain_groq import ChatGroq
import base64  # Import base64 to encode the image

def get_base64_image(image_file):
    """Convert an image file to a base64 string."""
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()

# Set the path for the background image
image_path = r"C:\Users\USER\Downloads\Untitled design.png"

# Add custom CSS for the background image and title styling
page_bg_image = f'''
<style>
.stApp {{
    background-image: url("data:image/png;base64,{get_base64_image(image_path)}"); /* Changed to 'image/png' */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

h1 {{
    color: white;  /* Change the text color to yellow */
    font-size: 8em; /* Increase the font size */
    font-weight: bold; /* Make the font bold */
}}
</style>
'''

# Apply the custom CSS with Streamlit
st.markdown(page_bg_image, unsafe_allow_html=True)

# Set API Key via Streamlit secrets (you should add the API key in import

# Set the API key using Streamlit's secret management
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = st.secrets["groq_api_key"]["groq_api_key"]

# Initialize the LLaMA models
extractor_llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
)
summarizer_llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
)

# Streamlit UI
st.title("LegEx")

# Input area for the legal case sentence
legal_case_sentence = st.text_input("Enter a legal case sentence:")

if st.button("upload"):
    # Extract legal features from the sentence
    with st.spinner('Extracting legal features...'):
        extraction_response = extractor_llm.invoke(f"""
        Extract the legal features from the following sentence and present them in the following structure:
        {{
            "classes": [
                "LEGAL_PRINCIPLE",
                "CASE_NAME",
                "YEAR",
                "JUDGE_NAME",
                "LEGISLATION"
            ],
            "annotations": [
                [
                    "{legal_case_sentence}",
                    {{
                        "entities": [
                            ["LEGAL_PRINCIPLE", "CASE_NAME", "YEAR", "JUDGE_NAME", "LEGISLATION"]
                        ]
                    }}
                ]
            ]
        }}

        Sentence: "{legal_case_sentence}"
        """)

        # Store the extracted content
        extracted_content = extraction_response.content

    # Pass the extracted content to the summarization model
    with st.spinner('Summarizing the extracted features...'):
        summary_response = summarizer_llm.invoke(f"""
        Summarize the following extracted legal features. Please note:
        1. The **first case** mentioned is the **primary case**.
        2. Any **subsequent cases** mentioned are **reference cases** that support or cite the primary case.

        Extracted Legal Features:
        {extracted_content}
        """)

        # Output the summary
        st.subheader("Summary")
        st.write(summary_response.content)
