from flask import Flask, render_template
import google.generativeai as palm
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# API KEY Details
load_dotenv()
api_key_palm = os.getenv("API_KEY")


# PaLM API - Can configure threshold to avoid certain content - https://developers.generativeai.google/guide/safety_setting
palm.configure(api_key=api_key_palm)

defaults = {
    "model": "models/text-bison-001",
    "temperature": 0.7,
    "candidate_count": 1,
    "top_k": 40,
    "top_p": 0.95,
    "max_output_tokens": 1024,
    "stop_sequences": [],
    "safety_settings": [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2},
    ],
}

# get logo from web scrape and pass values from AI

# Prompt for AI - Will utilize eventlistener
brand_logo = input("Hello there, what is your company name? ")


# Scrape with brand passed in from input
URL = f"https://worldvectorlogo.com/logo/{brand_logo}"


getURL = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(getURL.text, "html.parser")

image_ = soup.find_all("img")

image_sources = []

for image in image_:
    image_sources.append(image.get("src"))


def get_logo(word, list_of_strings):
    for string in list_of_strings:
        if word in string:
            return string
    return None


# PaLM AI Prompt & Response
prompt = f"How can Movable Ink Help {brand_logo}"

response = palm.generate_text(**defaults, prompt=prompt)
response_chat = response.result

# Image URL to pass into HTML
logo_image = get_logo(brand_logo, image_sources)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", img_url=logo_image, value=response_chat)
