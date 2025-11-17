import os
import sys
from google import genai
from dotenv import load_dotenv
from phoenix.otel import register

# Load environment variables
load_dotenv()


def ask_country(default: str | None = None) -> str:
    """Prompt the user to enter a country name.

    If the user presses Enter with no input, the default (if provided) is used.
    If input is not available (e.g., non-interactive), the default is returned
    or an empty string if no default was provided.
    """
    prompt = f"Enter country name [{default}]: " if default else "Enter country name: "
    try:
        val = input(prompt).strip()
    except EOFError:
        # Non-interactive environment: fall back to default or empty string
        return default or ""
    return val or default or ""


def setup_phoenix_tracing():
    """Configure Phoenix tracing for observability."""
    phoenix_api_key = os.environ.get("PHOENIX_API_KEY")
    phoenix_endpoint = os.environ.get("PHOENIX_COLLECTOR_ENDPOINT")
    
    if not phoenix_api_key or not phoenix_endpoint:
        print(
            "Warning: Phoenix tracing not configured.\n"
            "Set PHOENIX_API_KEY and PHOENIX_COLLECTOR_ENDPOINT in your .env file.\n"
            "Continuing without tracing..."
        )
        return None
    
    # Configure the Phoenix tracer with auto-instrumentation
    tracer_provider = register(
        project_name="gemini-capital-assistant",  # Customize this name
        auto_instrument=True  # Auto-instrument based on installed dependencies
    )
    
    print("Phoenix tracing enabled")
    return tracer_provider


def main():
    """Run the capital city query using Google Gemini with Phoenix tracing."""
    # Validate API key early and print a helpful message if missing
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Missing GEMINI_API_KEY environment variable.\n"
            "Set it in your .env file or shell and re-run, for example:\n"
            "  export GEMINI_API_KEY=your_api_key_here"
        )
        sys.exit(1)

    # Setup Phoenix tracing (optional but recommended)
    setup_phoenix_tracing()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Ask the user for a country name; default to Earth if they press Enter
    country_name = ask_country(default="Earth")

    model = "gemini-flash-latest"
    contents = f"What is the capital of {country_name}"

    try:
        print(f"\nGenerating response for: {country_name}\n")
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
        ):
            print(chunk.text, end="")
        print("\n")  # Add newline after streaming completes
    except Exception as e:
        # Surface a readable error message for debugging
        print(f"\nError while generating content: {e}")
        raise


if __name__ == "__main__":
    main()