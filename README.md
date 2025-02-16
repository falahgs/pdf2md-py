# PDF2MD - Advanced PDF to Markdown Converter

![PDF2MD Logo](https://raw.githubusercontent.com/falahgs/pdf2md-py/main/assets/logo.png)

A powerful web application that converts PDF documents to Markdown format using multiple conversion engines, including AI-powered solutions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.0%2B-FF4B4B)](https://streamlit.io/)

## 🌟 Features

- **Multiple Conversion Engines:**
  - PyMuPDF: Fast and reliable for general documents
  - Docling: Excellent for complex document structures
  - Marker: Advanced formatting preservation
  - MarkItDown: Quick conversion for simple documents
  - Gemini AI: Intelligent processing for complex layouts

- **User-Friendly Interface:**
  - Clean, intuitive design
  - Real-time markdown preview
  - Easy file upload and download
  - Progress indicators
  - Detailed documentation

- **Advanced Capabilities:**
  - Maintains document structure
  - Preserves formatting
  - Handles tables and lists
  - Supports complex layouts
  - AI-powered conversion option

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/falahgs/pdf2md-py.git
cd pdf2md-py
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the project root
- Add your Gemini API key (if using the AI converter):
```
GEMINI_API_KEY=your_api_key_here
```

## 💻 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Choose a conversion method:
   - **PyMuPDF**: Best for general PDF documents
   - **Docling**: Ideal for academic papers and complex structures
   - **Marker**: Great for documents with special formatting
   - **MarkItDown**: Perfect for simple documents
   - **Gemini**: AI-powered conversion for complex layouts

4. Upload your PDF file and click convert

5. Preview the result and download your markdown file

## 🛠️ Technologies Used

- **Frontend:**
  - Streamlit
  - Custom CSS
  - Responsive Design

- **Backend:**
  - Python 3.8+
  - PyMuPDF
  - Google Gemini AI
  - Multiple PDF Processing Libraries

- **Development:**
  - Environment Management: python-dotenv
  - Version Control: Git
  - Code Quality: Black, Flake8

## 📝 Citation

If you use PDF2MD in your research or project, please cite:

```bibtex
@software{gatea2024pdf2md,
  author = {Gatea, Falah},
  title = {PDF2MD: Advanced PDF to Markdown Converter},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/falahgs/pdf2md-py}
}
```

## 👨‍💻 Author

**Falah Gatea**
- 🌐 [Portfolio](https://iraqprogrammer.wordpress.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/falah-gatea-060a211a7)
- 🐙 [GitHub](https://github.com/falahgs)
- 📝 [Medium](https://medium.com/@falahgs)
- 📦 [PyPI](https://pypi.org/user/falahgs)
- 📺 [YouTube](https://www.youtube.com/@FalahgsGate)
- 📚 [Amazon Author](https://www.amazon.com/stores/Falah-Gatea-Salieh/author/B0BYHXLP7R)
- 🤗 [Hugging Face](https://huggingface.co/Falah)
- 📊 [Kaggle](https://www.kaggle.com/falahgatea)
- 🎨 [Civitai](https://civitai.com/user/falahgs)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/falahgs/pdf2md-py/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⭐ Show your support

Give a ⭐️ if this project helped you!
