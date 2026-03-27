from pypdf import PdfReader

def extract_text_from_file(uploaded_file):
    """Extracts text from uploaded TXT or PDF files in memory."""
    if uploaded_file is None:
        return ""

    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'txt':
        return uploaded_file.getvalue().decode("utf-8")
    elif file_extension == 'pdf':
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    else:
        return "Unsupported file type."