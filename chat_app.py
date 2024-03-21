import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure Gemini API with the provided API key
genai.configure(api_key="your api key")  # Replace YOUR_API_KEY with your actual API key

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Function to extract text from PDF documents
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Main function
def main():
    st.set_page_config("Multi PDF Chat", layout="wide")
    st.title("Chat with Multi PDFs")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: black;
            color: white; /* Change text color to white */
        }
        .stTextInput>div>div>div>input::-webkit-input-placeholder {
            color: white;
            border-color: white;
        }
        .stTextInput>div>div>div>input:-ms-input-placeholder {
            color: white;
            border-color: white;
        }
        .stTextInput>div>div>div>input::placeholder {
            color: white;
            border-color: white;
        }
        .stButton>button {
            color: black !important; /* Change button text color to black */
        }
        .st-bc, .st-ef, .st-fu, .st-gx, .st-gh {
            background-color: white; /* Change background color to white */
            border: 2px solid white; /* Change border color to white */
            border-radius: 5px;
            padding: 10px;
        }
        .st-gx p, .st-gh p {
            color: lightyellow; /* Change color of file name section */
        }
        .stOutput>div>div>div {
            background-color: white; /* Change background color of output box */
            border: 2px solid white; /* Change border color of output box */
            border-radius: 5px;
            padding: 10px;
            color: black; /* Change text color in output section */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Upload PDF files
    pdf_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, key="file_uploader")

    if pdf_files:
        st.write("Upload completed!", unsafe_allow_html=True)

    # Ask a question
    user_question = st.text_area("Ask a question:", height=100)

    # Display the result
    if st.button("Ask", key="ask_button") and pdf_files:
        raw_text = get_pdf_text(pdf_files)

        # Start chat with empty history
        convo = model.start_chat(history=[])

        # Send the extracted text from PDF as a message
        convo.send_message(raw_text)

        # Send user question and get response
        convo.send_message(user_question)
        response = convo.last.text

        st.markdown(
            f"""
            <div class="stOutput">
                <div class="st-dg">
                    <div class="st-dh st-dz st-e0">
                        <div>
                            {response}
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
