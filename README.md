# [Live Site](https://rdelliot-parsons-problem-generator.glitch.me)

# Parsons Problem Generator API

This project is a FastAPI-based application for generating Parsons problems, which are educational programming exercises. The application uses OpenAI's GPT model to generate problems based on user-selected programming concepts and difficulty levels.

## Features

- **Dynamic Front-End**: A user-friendly front-end built with HTML and JavaScript, dynamically updates based on user input.
- **AI-Generated Problems**: Uses OpenAI's GPT model to generate Parsons problems tailored to the selected programming language, concepts, and difficulty.
- **GET API Endpoints**:
  - `/generate-problems`: Accepts query parameters to generate Parsons problems.
  - `/generate-topics`: Accepts an activity name to fetch a list of relevant topics.
- **Cross-Origin Support**: Configured with CORS middleware to allow requests from any origin.

## Project Structure

```
pyproject.toml       # Project configuration file
README.md            # Project documentation
server.py            # Main FastAPI application
uv.lock              # Dependency lock file
static/              # Static files (e.g., CSS, JS)
templates/           # HTML templates
    index.html       # Front-end interface
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies using `uv`:
   ```bash
   uv pip install -r pyproject.toml
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```env
   OPENAI_API_KEY=<your-openai-api-key>
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_API_MODEL_NAME=gpt-4.1
   ```

## Running the Application

1. Start the server in debug mode:
   ```bash
   uv run uvicorn server:app --reload
   ```

2. Open your browser and navigate to:
   - Front-end: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - API Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Usage

1. Use the front-end interface to select a programming language, concepts, and the number of problems.
2. The application dynamically generates a URL for the API request.
3. Click "Preview Result" to fetch and display the generated problems.
4. Copy the generated URL to use it in other tools or applications.

## API Reference

### `GET /generate-topics`

Fetches a list of topics based on the provided activity name.

#### Query Parameter:
- `activity_name` (string): The name of the activity for which topics should be generated.

#### Example Request:
```bash
curl "http://127.0.0.1:8000/generate-topics?activity_name=Python%20Basics"
```

#### Example Response:
```json
{
    "topics": {
        "topics": ["Variables", "Loops", "Functions"]
    }
}
```

---

### `GET /generate-problems`

Generates Parsons problems based on the provided query parameter.

#### Query Parameter:
- `specification` (string): A base64-encoded JSON string containing the problem specification. The JSON object should have the following structure:
  ```json
  {
      "topics": ["Variables", "Loops", "Functions"],
      "num_problems": 3
  }
  ```

#### Example Request:
```bash
curl "http://127.0.0.1:8000/generate-problems?specification=eyJ0b3BpY3MiOiBbIlZhcmlhYmxlcyIsICJMb29wcyIsICJGdW5jdGlvbnMiXSwgIm51bV9wcm9ibGVtcyI6IDN9"
```

#### Example Response:
```json
{
    "activityName": "Custom Parsons Problem",
    "problems": [
        {
            "prompt": "Calculate the factorial of a number using a loop.",
            "blocks": [
                {
                    "id": "a",
                    "code": "let result = 1;"
                },
                {
                    "id": "b",
                    "code": "for (let i = 1; i <= n; i++) {"
                },
                {
                    "id": "c",
                    "code": "result = result * i;"
                },
                {
                    "id": "d",
                    "code": "}"
                },
                {
                    "id": "e",
                    "code": "result = result + i;"
                },
                {
                    "id": "f",
                    "code": "for (let i = 0; i <= n; i++) {"
                }
            ],
            "correctOrder": [
                "a",
                "b",
                "c",
                "d"
            ]
        },
        {
            "prompt": "Write code to find the maximum value in an array named nums.",
            "blocks": [
                {
                    "id": "a",
                    "code": "let max = nums[0];"
                },
                {
                    "id": "b",
                    "code": "for (let i = 1; i < nums.length; i++) {"
                },
                {
                    "id": "c",
                    "code": "if (nums[i] > max) {"
                },
                {
                    "id": "d",
                    "code": "max = nums[i];"
                },
                {
                    "id": "e",
                    "code": "}"
                },
                {
                    "id": "f",
                    "code": "}"
                },
                {
                    "id": "g",
                    "code": "if (nums[i] < max) {"
                }
            ],
            "correctOrder": [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f"
            ]
        },
        {
            "prompt": "Check if a string variable str is a palindrome.",
            "blocks": [
                {
                    "id": "a",
                    "code": "let reversed = '';"
                },
                {
                    "id": "b",
                    "code": "for (let i = str.length - 1; i >= 0; i--) {"
                },
                {
                    "id": "c",
                    "code": "reversed += str[i];"
                },
                {
                    "id": "d",
                    "code": "}"
                },
                {
                    "id": "e",
                    "code": "let isPalindrome = str === reversed;"
                },
                {
                    "id": "f",
                    "code": "let isPalindrome = str !== reversed;"
                },
                {
                    "id": "g",
                    "code": "for (let i = 0; i < str.length; i++) {"
                }
            ],
            "correctOrder": [
                "a",
                "b",
                "c",
                "d",
                "e"
            ]
        }
    ]
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Written by [Adam Smith](https://adamsmith.as) using [GitHub Copilot agent mode](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI GPT](https://openai.com/)