# AI Engineering

This project is a small Python example that uses the Groq API to answer user questions through a structured prompt and a Pydantic response model.

## Project Structure

- prompts.py: contains the system prompt template used by the app.
- pydantic_testing.py: main script that sends a question to Groq and parses the response into a structured JSON object.
- requirements.txt: Python dependencies for the project.
- README.md: project documentation.

## Setup

1. Create and activate a virtual environment:
   - python -m venv .venv
   - .\.venv\Scripts\activate

2. Install dependencies:
   - pip install -r requirements.txt

3. Configure your API key:
   - Create a .env file in the project root.
   - Add your Groq API key:
     - GROQ_API_KEY=your_api_key_here

## Usage

Run the application:

- python pydantic_testing.py

You will be prompted to enter a question. The program will send it to the Groq model and print the structured answer.

## Notes

- This project requires a valid Groq API key.
- The current script uses the model openai/gpt-oss-120b.
- The response is validated with a Pydantic model defined in pydantic_testing.py.
