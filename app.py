import streamlit as st
from PyPDF2 import PdfReader
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='feedback_app.log', filemode='a', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        logging.info("Text extraction completed.")
        logging.debug(f"Extracted text: {text[:500]}")  # Log the first 500 characters of extracted text for verification
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

# Main Streamlit app function
def main():
    st.header("PDF Text Reader and Feedback Collector")

    # Sidebar information
    with st.sidebar:
        st.title('Feedback App')
        st.markdown('''
        ## About
        This app allows users to upload a PDF, read its text, and provide feedback.
        ''')
    
    # Upload PDF file
    pdf = st.file_uploader("Upload your PDF", type='pdf')
    if pdf is not None:
        try:
            text = extract_text_from_pdf(pdf)
            if not text.strip():
                st.error("The PDF does not contain any extractable text. Please upload a different PDF.")
                return
            
            st.subheader("Extracted Text")
            st.text_area("PDF Content", text, height=300)
            
            # Collect feedback
            st.subheader("Provide Your Feedback")
            feedback = st.text_area("Your Feedback", height=100)
            if st.button("Submit Feedback"):
                with open("feedback.txt", "a") as f:
                    f.write(f"Feedback for {pdf.name}:\n{feedback}\n\n")
                st.success("Thank you for your feedback!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
