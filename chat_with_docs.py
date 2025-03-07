import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

# Configure Gemini API
genai.configure(api_key="AIzaSyCGNR4nQ1HfVhBpGO4NwT7nVJIsECO13-o")
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_gemini_response(prompt, pdf_content):
    combined_prompt = f"Context from PDF:\n{pdf_content}\n\nUser Question: {prompt}"
    response = model.generate_content(combined_prompt)
    return response.text

# Streamlit UI with branding
st.set_page_config(
    page_title="Pawan kumar - PDF Chat",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for branding
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTitle {
        color: #FF0000;
        font-size: 3rem !important;
    }
    .youtube-link {
    background-color: black;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    margin: 10px 0;
}
    </style>
""", unsafe_allow_html=True)

# Header with branding
st.title("Pawan kumar - PDF Chat Assistant")
st.markdown("Powered by Gemini AI 🤖")

# YouTube channel link
st.markdown("""
    <a href="https://www.youtube.com/channel/UClgbj0iYh5mqY_81CMCw25Q" 
       target="_blank" 
       class="youtube-link" style="  text-decoration: none;">
        📺 Subscribe to Pawan kumar
    </a>
""", unsafe_allow_html=True)

st.markdown("---")

# File upload
uploaded_file = st.file_uploader("📄 Upload your PDF file", type=['pdf'])

if uploaded_file is not None:
    pdf_content = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded successfully!")

    # Store PDF content in session state
    if 'pdf_content' not in st.session_state:
        st.session_state.pdf_content = pdf_content

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Improved chat interface
    st.markdown("### 💬 Chat with your PDF")
    user_question = st.text_input("💭 What would you like to know about the document?")
    if user_question:
        response = get_gemini_response(user_question, st.session_state.pdf_content)
        
        # Add to chat history
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("Assistant", response))

    # Enhanced chat history display
    if st.session_state.chat_history:
        st.markdown("### 📝 Conversation History")
        for role, text in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"""
                    <div style='background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                        <strong>You:</strong> {text}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                        <strong>Assistant:</strong> {text}
                    </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Pawan kumar")
