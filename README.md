# Python Learning LLM

Experimental repository for learning Python and AI, featuring a capital city query application powered by Google Gemini.

## Features

- Query capital cities of any country using Google Gemini Flash
- Phoenix tracing integration for observability
- Two interfaces:
  - Command-line interface (CLI)
  - Web UI with Streamlit

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PHOENIX_API_KEY=your_phoenix_api_key_here  # Optional
   PHOENIX_COLLECTOR_ENDPOINT=your_endpoint_here  # Optional
   ```

## Usage

### CLI Version

Run the command-line interface:
```bash
python main.py
```

You'll be prompted to enter a country name. The app will query Gemini and stream the response.

### Web UI Version

Run the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

This will open a web browser with an interactive UI where you can enter country names and see the results in real-time.

## Project Structure

- `main.py` - Core application logic and CLI interface
- `streamlit_app.py` - Streamlit web UI
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not committed to git)

## Technologies

- Google Gemini Flash - LLM for generating responses
- Streamlit - Web UI framework
- Phoenix OTEL - Observability and tracing
- Python-dotenv - Environment variable management
