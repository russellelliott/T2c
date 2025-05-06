from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
import os
import json
import openai
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import base64

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API base and model name from environment variables
openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
openai_api_model_name = os.getenv("OPENAI_API_MODEL_NAME", "gpt-4o")

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please add your OpenAI API key to the .env file.")

# Configure OpenAI API
client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/generate-topics")
def generate_topics(activity_name: str):
    try:
        # Construct the system prompt for generating topic ideas
        system_prompt = f"""You are a creative assistant. Generate a list of topic ideas for Parsons problems.
The topics should be relevant to the activity: "{activity_name}".
Provide 5-10 diverse and interesting topics that could be discussed in this activity.
The output must be a valid JSON array of strings, like this:
["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model=openai_api_model_name,
            messages=[{"role": "system", "content": system_prompt}],
            response_format={"type": "json_object"}
        )

        # Extract the AI-generated content
        ai_response = response.choices[0].message.content
        topics = json.loads(ai_response)

        return JSONResponse(content={"topics": topics})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating topics: {str(e)}")


@app.get("/generate-problems")
def generate_problems(specification: str):
    try:
        # Decode the base64-encoded specification
        decoded_spec = base64.b64decode(specification).decode("utf-8")
        spec_data = json.loads(decoded_spec)
        topics = spec_data.get("topics", [])
        num_problems = spec_data.get("num_problems", 1)

        # Construct the system prompt
        system_prompt = f"""You are a Parsons problem generator.

Your task is to generate a set of problems based on the selected topics.
Each problem should include:
- A problem statement.
- A list of code blocks, including distractor blocks.
- The correct order of the blocks.

The following rules must be followed:
1. Each block must contain only code. No block should contain comments.
2. None of the blocks should have any indentation. All code should be left-aligned.

The output should be a JSON object with the following structure:

{{
    "activityName": "Custom Parsons Problem",
    "problems": [
        {{
            "prompt": "Divide the cost of a meal and tip among a given number of people.",
            "blocks": [
                {{ "id": "a", "code": "let tipAmount = mealCost * (tipPercentage /100);" }},
                {{ "id": "b", "code": "let totalCost = mealCost + tipAmount;" }},
                {{ "id": "c", "code": "let costPerPerson = totalCost / numPeople;" }},
                {{ "id": "d", "code": "let costPerPerson = mealCost / numPeople;" }},
                {{ "id": "e", "code": "let totalCost = mealCost - tipAmount;" }},
                {{ "id": "f", "code": "let tipAmount = mealCost + (tipPercentage /100);" }}
            ],
            "correctOrder": ["a", "b", "c"]
        }},
        ...
    ]
}}

The problems should be based on the following topics: {', '.join(topics)}.
The collection should have exactly {num_problems} problems."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model=openai_api_model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": decoded_spec}
            ],
            response_format={"type": "json_object"}
        )

        # Extract the AI-generated content
        ai_response = response.choices[0].message.content
        problems = json.loads(ai_response)

        return JSONResponse(content=problems)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating problems: {str(e)}")
