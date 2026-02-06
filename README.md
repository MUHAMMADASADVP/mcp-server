# My MCP Server

A Model Context Protocol server built with Python.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# OR
pip install -e ".[dev]"
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Running
```bash
python -m src.main
```

## Testing
```bash
pytest
```

## Project Structure
```
src/
├── server/       # Server configuration
├── handlers/     # Tool/Resource handlers
├── services/     # Business logic
├── repositories/ # Data access
├── models/       # Data models
└── utils/        # Utilities
```
