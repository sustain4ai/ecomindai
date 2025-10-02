# EcoMindAI

Estimate the environmental impact of your AI project and reduce it through recommendations.

## About

EcoMindAI is a gradio / FastAPI-based web application that helps you:
- 🌱 **Estimate** the environmental impact of your AI/ML projects
- 📊 **Analyze** energy consumption and carbon footprint
- 💡 **Get recommendations** to reduce environmental impact

The application provides a REST API for integration into your existing workflows and a web interface for interactive usage.

## 🚀 For Users - Quick Start

Use the pre-built Docker image to run EcoMindAI without any setup:

```bash
# Pull and run the latest version
docker pull sustain4raise/ecomindai:latest
docker run -p 8000:8000 sustain4raise/ecomindai:latest
```

**Access the application:**
- 🌐 Web interface: `http://localhost:8000`

### Using specific versions

```bash
# Pull a specific version
docker pull sustain4raise/ecomindai:1.0.1
docker run -p 8000:8000 sustain4raise/ecomindai:1.0.1
```

## 🛠️ For Developers - Local Development

### Prerequisites
- Python >= 3.13
- Pip & Pipenv

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/sustain4ai/ecomindai.git
   cd ecomindai
   ```

2. Install dependencies:
   ```bash
   pipenv sync
   ```


3. Run the application:
   ```bash
   pipenv run python main.py
   ```

The development server will start at `http://localhost:8000`

## 🧪 Testing the API

EcoMindAI uses FastAPI, which automatically generates interactive API documentation:

### Interactive Documentation
- **Swagger UI**: Go to `http://localhost:8000/docs`
  - Try API endpoints directly in your browser
  - See request/response schemas
  - Test with sample data

- **ReDoc**: Go to `http://localhost:8000/redoc`
  - Alternative documentation format
  - Better for reading and understanding

