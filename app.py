import streamlit as st
import pymupdf4llm
import pathlib
import os
import html
import time
from docling.document_converter import DocumentConverter
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from markitdown import MarkItDown
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Set page configuration
st.set_page_config(
    page_title="PDF to Markdown Converter",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        margin-bottom: 100px;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E86C1;
        color: white;
        border-radius: 10px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1A5276;
        transform: translateY(-2px);
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1C2833;
        color: white;
        padding: 1.5rem;
        text-align: center;
        z-index: 1000;
    }
    .main-content {
        margin-bottom: 250px;
    }
    .footer a {
        color: #3498DB;
        text-decoration: none;
        margin: 0 10px;
        transition: color 0.3s ease;
    }
    .footer a:hover {
        color: #85C1E9;
    }
    .stTab {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .welcome-header {
        background: linear-gradient(135deg, #2E86C1, #1A5276);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .social-icons {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 1rem;
    }
    .settings-section {
        background-color: #F4F6F7;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .api-input {
        background-color: white;
        border: 1px solid #AED6F1;
        border-radius: 5px;
        padding: 0.5rem;
    }
    .tab-content {
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Hide Streamlit Deploy Panel */
    .stDeployButton {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden;
    }
    [data-testid="stToolbar"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Settings
with st.sidebar:
    st.markdown("""
        <div class='settings-section'>
            <h2>🛠️ API Settings</h2>
        </div>
    """, unsafe_allow_html=True)
    
    gemini_key = st.text_input(
        "Google Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        key="gemini_key",
        help="Enter your Google Gemini API key"
    )
    
    if st.button("Save API Key"):
        with open(".env", "w") as f:
            f.write(f"GEMINI_API_KEY={gemini_key}")
        st.success("✅ API key saved successfully!")
        st.rerun()

# Welcome Header
st.markdown("""
    <div class='welcome-header'>
        <h1>🚀 Welcome to PDF2MD</h1>
        <p style='font-size: 1.2rem;'>A powerful tool to convert your PDF documents into clean, formatted Markdown.</p>
        <p style='font-size: 1rem; opacity: 0.9;'>Choose from multiple conversion engines to get the best results for your documents.</p>
    </div>
""", unsafe_allow_html=True)

# Documentation
st.header("📖 How to Use PDF2MD")
st.write("Choose from five different conversion methods based on your needs:")

with st.expander("1. PyMuPDF Converter", expanded=True):
    st.subheader("Best for: General PDF documents with simple formatting")
    st.markdown("""
    - Fast and reliable conversion
    - Maintains basic text formatting
    - Ideal for text-heavy documents
    """)

with st.expander("2. Docling Converter", expanded=True):
    st.subheader("Best for: Documents with complex structure")
    st.markdown("""
    - Preserves document structure
    - Handles tables and lists well
    - Perfect for academic papers
    """)

with st.expander("3. Marker Converter", expanded=True):
    st.subheader("Best for: Documents with special formatting")
    st.markdown("""
    - Advanced formatting preservation
    - Handles custom styles
    - Great for styled documents
    """)

with st.expander("4. MarkItDown Converter", expanded=True):
    st.subheader("Best for: Simple documents needing quick conversion")
    st.markdown("""
    - Fast processing
    - Clean output
    - Ideal for basic documents
    """)

with st.expander("5. Gemini Converter (AI-Powered)", expanded=True):
    st.subheader("Best for: Complex documents requiring intelligent processing")
    st.markdown("""
    - AI-powered conversion
    - Handles complex layouts
    - Requires API key setup in settings
    """)

st.subheader("Quick Steps:")
st.markdown("""
1. Select a conversion method tab
2. Upload your PDF file
3. Click the convert button
4. Preview the result
5. Download your converted markdown file

**Note:** For Gemini conversion, make sure to set up your API key in the settings panel (left sidebar).
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["PyMuPDF Converter", "Docling Converter", "Marker Converter", "MarkItDown Converter", "Gemini Converter"])

with tab1:
    st.markdown("#### Convert using PyMuPDF")
    with st.container():
        # File uploader for PyMuPDF
        uploaded_file_pymupdf = st.file_uploader("Choose a PDF file (PyMuPDF)", type=['pdf'], key="pymupdf")

        if uploaded_file_pymupdf is not None:
            # Save uploaded file temporarily
            temp_path = os.path.join("temp", uploaded_file_pymupdf.name)
            os.makedirs("temp", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file_pymupdf.getvalue())
            
            if st.button("Convert with PyMuPDF"):
                with st.spinner("Converting..."):
                    try:
                        # Convert PDF to Markdown
                        md_text = pymupdf4llm.to_markdown(temp_path)
                        
                        # Save the markdown file
                        output_filename = f"{os.path.splitext(uploaded_file_pymupdf.name)[0]}_pymupdf.md"
                        output_path = os.path.join("output", output_filename)
                        os.makedirs("output", exist_ok=True)
                        
                        pathlib.Path(output_path).write_bytes(md_text.encode())
                        
                        # Show success message
                        st.success(f"✅ Conversion successful! File saved as: {output_filename}")
                        
                        # Display markdown content
                        st.markdown("### Preview:")
                        st.text_area("Markdown Content", md_text, height=300, key="pymupdf_preview")
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="Download Markdown File",
                                data=file,
                                file_name=output_filename,
                                mime="text/markdown",
                                key="pymupdf_download"
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

with tab2:
    st.markdown("#### Convert using Docling")
    with st.container():
        # File uploader for Docling
        uploaded_file_docling = st.file_uploader("Choose a PDF file (Docling)", type=['pdf'], key="docling")

        if uploaded_file_docling is not None:
            # Save uploaded file temporarily
            temp_path = os.path.join("temp", uploaded_file_docling.name)
            os.makedirs("temp", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file_docling.getvalue())
            
            if st.button("Convert with Docling"):
                with st.spinner("Converting..."):
                    try:
                        # Initialize converter
                        converter = DocumentConverter()
                        result = converter.convert(temp_path)
                        docling_text = result.document.export_to_markdown()
                        
                        # Unescape HTML entities
                        docling_text = html.unescape(docling_text)
                        
                        # Save the markdown file
                        output_filename = f"{os.path.splitext(uploaded_file_docling.name)[0]}_docling.md"
                        output_path = os.path.join("output", output_filename)
                        os.makedirs("output", exist_ok=True)
                        
                        with open(output_path, "w", encoding="utf-8") as myfile:
                            myfile.write(docling_text)
                        
                        # Show success message
                        st.success(f"✅ Conversion successful! File saved as: {output_filename}")
                        
                        # Display markdown content
                        st.markdown("### Preview:")
                        st.text_area("Markdown Content", docling_text, height=300, key="docling_preview")
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="Download Markdown File",
                                data=file,
                                file_name=output_filename,
                                mime="text/markdown",
                                key="docling_download"
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

with tab3:
    st.markdown("#### Convert using Marker")
    with st.container():
        # File uploader for Marker
        uploaded_file_marker = st.file_uploader("Choose a PDF file (Marker)", type=['pdf'], key="marker")

        if uploaded_file_marker is not None:
            # Save uploaded file temporarily
            temp_path = os.path.join("temp", uploaded_file_marker.name)
            os.makedirs("temp", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file_marker.getvalue())
            
            if st.button("Convert with Marker"):
                with st.spinner("Converting..."):
                    try:
                        # Initialize converter
                        converter = PdfConverter(
                            artifact_dict=create_model_dict(),
                        )
                        rendered = converter(temp_path)
                        
                        # Save the markdown file
                        output_filename = f"{os.path.splitext(uploaded_file_marker.name)[0]}_marker.md"
                        output_path = os.path.join("output", output_filename)
                        os.makedirs("output", exist_ok=True)
                        
                        with open(output_path, "w", encoding="utf-8") as myfile:
                            myfile.write(rendered.markdown)
                        
                        # Show success message
                        st.success(f"✅ Conversion successful! File saved as: {output_filename}")
                        
                        # Display markdown content
                        st.markdown("### Preview:")
                        st.text_area("Markdown Content", rendered.markdown, height=300, key="marker_preview")
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="Download Markdown File",
                                data=file,
                                file_name=output_filename,
                                mime="text/markdown",
                                key="marker_download"
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

with tab4:
    st.markdown("#### Convert using MarkItDown")
    with st.container():
        # File uploader for MarkItDown
        uploaded_file_markitdown = st.file_uploader("Choose a PDF file (MarkItDown)", type=['pdf'], key="markitdown")

        if uploaded_file_markitdown is not None:
            # Save uploaded file temporarily
            temp_path = os.path.join("temp", uploaded_file_markitdown.name)
            os.makedirs("temp", exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file_markitdown.getvalue())
            
            if st.button("Convert with MarkItDown"):
                with st.spinner("Converting..."):
                    try:
                        # Initialize converter
                        md = MarkItDown()
                        result = md.convert(temp_path)
                        
                        # Save the markdown file
                        output_filename = f"{os.path.splitext(uploaded_file_markitdown.name)[0]}_markitdown.md"
                        output_path = os.path.join("output", output_filename)
                        os.makedirs("output", exist_ok=True)
                        
                        with open(output_path, "w", encoding="utf-8") as myfile:
                            myfile.write(result.text_content)
                        
                        # Show success message
                        st.success(f"✅ Conversion successful! File saved as: {output_filename}")
                        
                        # Display markdown content
                        st.markdown("### Preview:")
                        st.text_area("Markdown Content", result.text_content, height=300, key="markitdown_preview")
                        
                        # Download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="Download Markdown File",
                                data=file,
                                file_name=output_filename,
                                mime="text/markdown",
                                key="markitdown_download"
                            )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

with tab5:
    st.markdown("#### Convert using Gemini")
    with st.container():
        if not os.getenv("GEMINI_API_KEY"):
            st.warning("⚠️ Please set your GEMINI_API_KEY in the .env file to use this converter.")
        else:
            # File uploader for Gemini
            uploaded_file_gemini = st.file_uploader("Choose a PDF file (Gemini)", type=['pdf'], key="gemini")

            if uploaded_file_gemini is not None:
                # Save uploaded file temporarily
                temp_path = os.path.join("temp", uploaded_file_gemini.name)
                os.makedirs("temp", exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file_gemini.getvalue())
                
                if st.button("Convert with Gemini"):
                    with st.spinner("Converting... This may take a few moments."):
                        try:
                            # Upload file to Gemini
                            file = genai.upload_file(temp_path, mime_type="application/pdf")
                            
                            # Wait for file processing
                            while True:
                                file_status = genai.get_file(file.name)
                                if file_status.state.name == "ACTIVE":
                                    break
                                elif file_status.state.name != "PROCESSING":
                                    raise Exception(f"File processing failed: {file_status.state.name}")
                                time.sleep(2)
                            
                            # Create model and chat session
                            model = genai.GenerativeModel(
                                model_name="gemini-2.0-flash",
                                generation_config=generation_config,
                            )
                            
                            chat = model.start_chat(
                                history=[
                                    {
                                        "role": "user",
                                        "parts": [
                                            file,
                                            "You are a PDF to markdown converter. Convert this PDF document into a valid markdown document.",
                                        ],
                                    }
                                ]
                            )
                            
                            response = chat.send_message("Convert the PDF to markdown format.")
                            markdown_text = response.text
                            
                            # Save the markdown file
                            output_filename = f"{os.path.splitext(uploaded_file_gemini.name)[0]}_gemini.md"
                            output_path = os.path.join("output", output_filename)
                            os.makedirs("output", exist_ok=True)
                            
                            with open(output_path, "w", encoding="utf-8") as myfile:
                                myfile.write(markdown_text)
                            
                            # Show success message
                            st.success(f"✅ Conversion successful! File saved as: {output_filename}")
                            
                            # Display markdown content
                            st.markdown("### Preview:")
                            st.text_area("Markdown Content", markdown_text, height=300, key="gemini_preview")
                            
                            # Download button
                            with open(output_path, "rb") as file:
                                st.download_button(
                                    label="Download Markdown File",
                                    data=file,
                                    file_name=output_filename,
                                    mime="text/markdown",
                                    key="gemini_download"
                                )
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                        finally:
                            # Clean up temporary file
                            if os.path.exists(temp_path):
                                os.remove(temp_path)

# Add some spacing before the footer
st.markdown("<br><br>", unsafe_allow_html=True)

# Footer with social links
st.markdown("""
    <div class="footer">
            <div class="social-icons">
            <a href="https://www.linkedin.com/in/falah-gatea-060a211a7/" target="_blank">LinkedIn</a>
            <a href="https://github.com/falahgs" target="_blank">GitHub</a>
            <a href="https://www.instagram.com/falah.g.saleih/" target="_blank">Instagram</a>
            <a href="https://www.facebook.com/falahgs" target="_blank">Facebook</a>
            <a href="https://iraqprogrammer.wordpress.com/" target="_blank">Blog</a>
            <a href="https://medium.com/@falahgs" target="_blank">Medium</a>
            <a href="https://pypi.org/user/falahgs/" target="_blank">PyPI</a>
            <a href="https://www.youtube.com/@FalahgsGate" target="_blank">YouTube</a>
            <a href="https://www.amazon.com/stores/Falah-Gatea-Salieh/author/B0BYHXLP7R" target="_blank">Amazon</a>
            <a href="https://huggingface.co/Falah" target="_blank">Hugging Face</a>
            <a href="https://www.kaggle.com/falahgatea" target="_blank">Kaggle</a>
            </div>
        <p style='margin-top: 1rem;'>Made with ❤️ by Falah Gatea | © 2024</p>
    </div>
""", unsafe_allow_html=True)
