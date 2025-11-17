import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Functions
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
    return val or (default or "")

# Gemini Project
def generate():
    # Validate API key early and print a helpful message if missing.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "Missing GEMINI_API_KEY environment variable.\n"
            "Set it in your shell and re-run, for example:\n"
            "  export GEMINI_API_KEY=your_api_key_here"
        )
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Ask the user for a country name; default to Taiwan if they press Enter.
    country_name = ask_country(default="Earth")

    model = "gemini-flash-latest"
    # Use an f-string so country_name is interpolated into the prompt.
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"What is the capital of {country_name}"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=4096,
        ),
        image_config=types.ImageConfig(
            image_size="1K",
        ),
    )

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")
    except Exception as e:
        # Surface a readable error message for debugging.
        print("Error while generating content:", e)
        raise


if __name__ == "__main__":
    generate()