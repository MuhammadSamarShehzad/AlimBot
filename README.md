# 🤖 AlimBot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46+-red.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-orange.svg)
![AI](https://img.shields.io/badge/AI-Gemini%202.0-purple.svg)

**An intelligent Islamic guidance system powered by AI, providing scholarly answers based on Quran, Hadith, and Fatwa sources.**


</div>

---

## 🌟 Features

### 🤖 **AI-Powered Responses**
- **Gemini 2.0 Flash** integration for intelligent Islamic guidance
- **Multi-source knowledge base** combining Quran, Hadith, and Fatwa
- **Structured responses** with proper citations and references
- **Context-aware answers** tailored to user queries

### 📚 **Comprehensive Knowledge Base**
- **Quran Index**: Complete Quranic text with verse references
- **Hadith Database**: Authentic Hadith collections with proper citations
- **Fatwa Repository**: Extensive collection of Islamic rulings
- **Vector Search**: Semantic similarity search for relevant answers

### 🎨 **Modern Web Interface**
- **Streamlit-based UI** with elegant, responsive design
- **Interactive Q&A interface** with example questions
- **Real-time processing** with loading indicators
- **Mobile-friendly** responsive design

### 🏗️ **Robust Architecture**
- **Microservices architecture** with FastAPI backend
- **Docker containerization** for easy deployment
- **Session management** for conversation continuity
- **Error handling** and graceful degradation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Google AI API key (for Gemini 2.0)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alimbot.git
   cd alimbot
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Google AI API key
   ```

3. **Launch with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **Web Interface**: http://localhost:8501
   - **API Endpoint**: http://localhost:8000

---

## 🏛️ Architecture

```
AlimBot
├── 🎯 Frontend (Streamlit)
│   ├── Modern UI with Islamic design elements
│   ├── Interactive Q&A interface
│   └── Real-time response display
│
├── 🔧 Backend (FastAPI)
│   ├── RESTful API endpoints
│   ├── Session management
│   └── Error handling
│
├── 🧠 Core Engine
│   ├── AI Agent (Gemini 2.0)
│   ├── Knowledge Tools
│   └── Response Formatter
│
├── 📚 Knowledge Base
│   ├── Quran Index (FAISS)
│   ├── Hadith Index (FAISS)
│   └── Fatwa Index (FAISS)
│
└── 🐳 Infrastructure
    ├── Docker containers
    ├── Environment management
    └── Service orchestration
```

---

## 🔧 API Usage

### Query Endpoint
```bash
POST /query
Content-Type: application/json

{
  "query": "What breaks wudu?"
}
```

### Response Format
```json
{
  "result": "📖 **Quran References:**\n- Surah Al-Ma'idah 5:6\n\n📜 **Hadith References:**\n- Sahih Bukhari, Book of Ablution, Hadith #135\n- Sahih Muslim, Book of Purification, Hadith #225\n\n📚 **Fatwa Answer:**\n- Breaking wind, urination, defecation, deep sleep, and loss of consciousness break wudu.\n\n💡 **Conclusion:**\nWudu is invalidated by natural bodily functions and states that affect consciousness."
}
```

---

## 🛠️ Development

### Project Structure
```
├── api/                 # FastAPI backend
│   ├── main.py         # FastAPI application
│   ├── routes.py       # API endpoints
│   └── Dockerfile      # Backend container
├── app/                # Streamlit frontend
│   ├── main.py         # Web interface
│   └── Dockerfile      # Frontend container
├── core/               # Core AI engine
│   ├── agent.py        # AI agent configuration
│   ├── tools.py        # Knowledge tools
│   ├── services.py     # Search services
│   └── config.py       # Configuration
├── data/               # Knowledge base
│   └── fatwas.csv      # Fatwa dataset
├── indexing/           # Vector indices
│   ├── quran_index/    # Quran embeddings
│   ├── hadith_index/   # Hadith embeddings
│   └── fatwas_index/   # Fatwa embeddings
└── docker-compose.yml  # Service orchestration
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
cd api && uvicorn main:app --reload

# Run frontend (in another terminal)
cd app && streamlit run main.py
```

---

## 📊 Knowledge Base

### Data Sources
- **Quran**: Complete text with verse metadata
- **Hadith**: Authentic collections with proper citations
- **Fatwa**: Comprehensive Islamic rulings database

### Search Capabilities
- **Semantic Search**: Using sentence-transformers embeddings
- **Multi-modal Queries**: Text-based question processing
- **Relevant Retrieval**: Top-k most relevant results
- **Citation Tracking**: Proper source attribution

---

## 🎨 Features in Detail

### 🤖 AI Agent Capabilities
- **Multi-tool Integration**: Seamlessly combines Quran, Hadith, and Fatwa tools
- **Structured Responses**: Organized answers with clear sections
- **Citation Management**: Proper references to Islamic sources
- **Context Awareness**: Understands complex Islamic queries

### 🎯 User Experience
- **Example Questions**: Pre-loaded common Islamic queries
- **Real-time Processing**: Live response generation
- **Error Handling**: Graceful degradation on API failures
- **Mobile Responsive**: Works on all device sizes

### 🔒 Security & Privacy
- **Local Processing**: No sensitive data sent to external services
- **Session Isolation**: Separate conversation contexts
- **Input Validation**: Sanitized user queries
- **Error Logging**: Comprehensive error tracking

---

## 🚀 Deployment

### Docker Deployment
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Development deployment
docker-compose up --build
```

### Environment Variables
```bash
# Required
GOOGLE_AI_API_KEY=your_gemini_api_key
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Important Disclaimer

**This AI system is designed to provide general Islamic information and should not be considered a replacement for qualified Islamic scholars or religious authorities. Always consult with knowledgeable scholars for important religious decisions and rulings.**

## 🙏 Acknowledgments

- **Open Source Community**: For the amazing tools and libraries that made this project possible
- **Google AI**: For providing the Gemini 2.0 model
- **Islamic Knowledge Sources**: For the authentic Quran, Hadith, and Fatwa databases

---



<div align="center">

**🤲 May Allah guide us all with knowledge and wisdom**

*Built with ❤️ for the Muslim community*

</div>