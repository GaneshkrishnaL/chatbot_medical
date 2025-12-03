# 🏥 Medical Chatbot AI

A sophisticated medical information chatbot powered by **Retrieval-Augmented Generation (RAG)** that combines clinical knowledge with pharmaceutical product data to provide comprehensive medical insights.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.20-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🌟 Features

- **Dual-Index RAG System**: Combines clinical encyclopedia data with pharmaceutical product catalogs
- **Smart Retrieval**: Searches across both medical knowledge and product databases simultaneously
- **Modern UI**: Beautiful, responsive interface with dark/light mode toggle
- **Product Metadata**: Extracts and indexes NDC codes, HCPCS codes, and manufacturer information
- **Natural Language Processing**: Powered by sentence transformers and OpenAI's language models
- **Vector Search**: Uses Pinecone for fast, semantic similarity search

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   Flask Web Application     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│   Dual Retrieval System     │
├─────────────┬───────────────┤
│  Clinical   │   Product     │
│   Index     │   Catalog     │
└──────┬──────┴───────┬───────┘
       │              │
       ▼              ▼
┌──────────────────────────────┐
│   Pinecone Vector Store      │
│  (Semantic Search Engine)    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   OpenAI Language Model      │
│   (Answer Generation)        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Formatted Response         │
└──────────────────────────────┘
```

---

## 📋 Prerequisites

- **Python 3.11+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone API Key** ([Get one here](https://www.pinecone.io/))
- **PDF Data Files**:
  - `Data/Medical_book.pdf` - Clinical encyclopedia
  - `Data/Product_catalog.pdf` - Pharmaceutical product catalog

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chatbot_medical.git
cd chatbot_medical
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

⚠️ **Never commit your `.env` file to version control!**

---

## 📊 Data Preparation & Indexing

Before running the chatbot, you need to index your medical data into Pinecone.

### 1. Prepare Your Data

Place your PDF files in the `Data/` directory:
- `Data/Medical_book.pdf` - Medical encyclopedia/clinical knowledge
- `Data/Product_catalog.pdf` - Pharmaceutical product information

### 2. Run the Indexing Script

```bash
python store_index.py
```

This script will:
1. ✅ Load and parse PDF documents
2. ✅ Split clinical data into semantic chunks
3. ✅ Extract product metadata (NDC, HCPCS codes)
4. ✅ Generate embeddings using `sentence-transformers/all-MiniLM-L6-v2`
5. ✅ Create two Pinecone indexes:
   - `clinical-index` - Medical knowledge
   - `product-index` - Pharmaceutical products
6. ✅ Upload vectors to Pinecone

**Expected Output:**
```
INFO:root:📥 Loading PDFs...
INFO:root:🔪 Chunking clinical data...
INFO:root:🔪 Extracting product metadata lines...
INFO:root:🧠 Loading embeddings...
INFO:root:📦 Created index: clinical-index
INFO:root:📦 Created index: product-index
INFO:root:⬆️ Uploading clinical data...
INFO:root:⬆️ Uploading product data...
INFO:root:✅ Indexing complete.
```

---

## 🎯 Running the Application

### Start the Flask Server

```bash
python app.py
```

The application will start on **http://127.0.0.1:5000**

### Access the Web Interface

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 💡 Usage Examples

### Example Queries

1. **Clinical Questions:**
   ```
   What is diabetes?
   What are the symptoms of hypertension?
   How is pneumonia treated?
   ```

2. **Product Queries:**
   ```
   Tell me about NDC 50242-0136-01
   What products are available for pain management?
   Show me HCPCS code A4321
   ```

3. **Combined Queries:**
   ```
   What natural treatments are available for arthritis?
   What medications are used for diabetes and their NDC codes?
   ```

---

## 🗂️ Project Structure

```
chatbot_medical/
├── app.py                      # Main Flask application
├── store_index.py              # Data indexing script
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── template.py                 # Project structure generator
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker configuration
├── README.md                   # This file
│
├── src/
│   ├── __init__.py
│   ├── helper.py               # PDF loading and chunking utilities
│   └── prompt.py               # System prompts for the LLM
│
├── templates/
│   └── chat.html               # Web interface template
│
├── static/
│   └── style.css               # Styling with dark/light mode
│
├── Data/
│   ├── Medical_book.pdf        # Clinical knowledge base
│   └── Product_catalog.pdf     # Pharmaceutical products
│
└── research/
    └── trials.ipynb            # Jupyter notebook for experiments
```

---

## 🔧 Configuration

### Modify Index Names

Edit `store_index.py` and `app.py`:

```python
CLINICAL_INDEX = "your-clinical-index-name"
PRODUCT_INDEX = "your-product-index-name"
```

### Change Embedding Model

Edit `store_index.py` and `app.py`:

```python
embeddings = HuggingFaceEmbeddings(
    model_name="your-preferred-model"
)
```

Popular alternatives:
- `sentence-transformers/all-mpnet-base-v2` (better quality, slower)
- `sentence-transformers/paraphrase-MiniLM-L6-v2` (faster)

### Adjust LLM Settings

Edit `app.py`:

```python
llm = OpenAI(
    temperature=0.2,  # Lower = more focused, Higher = more creative
    model_name="gpt-3.5-turbo-instruct"  # or other OpenAI models
)
```

---

## 🎨 UI Features

### Dark/Light Mode
- Click the moon/sun icon in the header to toggle themes
- Preference is saved in browser localStorage

### Responsive Design
- Mobile-friendly layout
- Adapts to different screen sizes
- Modern glassmorphism design

---

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI Rate Limit Error (429)**
```
Error: You exceeded your current quota
```
**Solution:** Add credits to your OpenAI account or switch to a cheaper model

**2. Pinecone Connection Error**
```
Error: Invalid API key
```
**Solution:** Check your `.env` file and ensure `PINECONE_API_KEY` is correct

**3. Module Import Errors**
```
ImportError: cannot import name 'X'
```
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

**4. Port Already in Use**
```
Address already in use - Port 5000
```
**Solution:** Kill the existing process or use a different port
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Or run on different port
flask run --port 5001
```

---

## 📦 Dependencies

### Core Libraries
- **Flask** - Web framework
- **LangChain** - LLM orchestration
- **Pinecone** - Vector database
- **OpenAI** - Language model API
- **Sentence Transformers** - Text embeddings
- **PyPDF** - PDF parsing

### Full List
See `requirements.txt` for complete dependency list.

---

## 🔒 Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use environment variables for API keys
3. ✅ Keep dependencies updated
4. ✅ Use HTTPS in production
5. ✅ Implement rate limiting for production deployments

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build image
docker build -t medical-chatbot .

# Run container
docker run -p 5000:5000 --env-file .env medical-chatbot
```

### Production Considerations

- Use **Gunicorn** or **uWSGI** instead of Flask dev server
- Set up **NGINX** as reverse proxy
- Enable **HTTPS** with SSL certificates
- Implement **rate limiting** and **authentication**
- Use **Redis** for session management
- Monitor with **Prometheus** and **Grafana**

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ganesh Krishna Lakshmisetty**
- Email: ganeshkrishna.lakshmisetty@gmail.com
- GitHub: [@GaneshkrishnaL](https://github.com/GaneshkrishnaL)

---

## 🙏 Acknowledgments

- **LangChain** for the RAG framework
- **Pinecone** for vector database infrastructure
- **OpenAI** for language models
- **Sentence Transformers** for embeddings
- **Flask** community for web framework

---

## ⚠️ Disclaimer

**This chatbot is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.**

---

## 📊 Performance Metrics

- **Average Response Time:** ~2-3 seconds
- **Embedding Dimension:** 384 (all-MiniLM-L6-v2)
- **Index Size:** Depends on your PDF data
- **Retrieval:** Top 3 documents from each index (6 total)

---

## 🔮 Future Enhancements

- [ ] Add support for multiple languages
- [ ] Implement conversation history
- [ ] Add user authentication
- [ ] Create admin dashboard
- [ ] Support for more document formats (DOCX, TXT)
- [ ] Real-time streaming responses
- [ ] Voice input/output
- [ ] Mobile app version
- [ ] Integration with medical databases (PubMed, FDA)

---

**Made with ❤️ for better healthcare information access**
