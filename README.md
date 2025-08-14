# EcoMindAI

Estimate the environmental impact of your AI project and reduce it through recommendations.

## Quick Start with Docker

### Using the pre-built image from DockerHub

```bash
# Pull the latest image
docker pull sustain4raise/ecomindai:latest

# Run the application
docker run -p 8000:8000 sustain4raise/ecomindai:latest
```

The application will be available at `http://localhost:8000`

#### Using specific versions

```bash
# Pull a specific version
docker pull sustain4raise/ecomindai:1.0.1
```

## Development

### Prerequisites
- Python >= 3.13
- Pip & Pipenv

### Setup
1. Clone and open the project
2. Install dependencies: `pipenv sync`
3. Run the application: `pipenv run python main.py`

