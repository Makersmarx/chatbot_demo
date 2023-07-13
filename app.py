from flask import Flask, render_template, request
import google.generativeai as palm
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re

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


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        inputUser = request.form.get("textEntry")
        prompt = f"How can Movable Ink Help {inputUser} as a list"
        response = palm.generate_text(**defaults, prompt=prompt)
        response_chat = response.result
        company_prompt = f"What category of company is ${inputUser}?"
        company_response = palm.generate_text(**defaults, prompt=company_prompt)
        company_type = company_response.result
        print('COMPANY TYPE', company_type)

        URL = f"https://worldvectorlogo.com/logo/{inputUser}"

        getURL = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(getURL.text, "html.parser")

        getProduct = requests.get("https://www.abercrombie.com/shop/us/womens", headers={"User-Agent": "Mozilla/5.0"})
        company_soup = BeautifulSoup(getProduct.text, 'html.parser')
        image_dictionary = {}
        alt_texts = []
        images_ = company_soup.find_all('img')
      
        

        for i in range(len(images_) - 1):
            if images_[i] is not None and hasattr(images_[i], 'get'):
                text = images_[i].get('alt')
                if bool(text):
                    alt_texts.append(images_[i].get('alt'))
                    image_dictionary[text] = images_[i].get('src')
            # return alt_texts
        alt_strings = "|".join(alt_texts)
        alt_prompt = f'Given the | separated list ${alt_strings}, can you identify 4 different products and return them as a | separated list'
        alt_response = palm.generate_text(**defaults, prompt=alt_prompt)
        product_array = alt_response.result.split('|')
        print('PRODUCT', product_array)
        product_dictionary = {p.strip():image_dictionary[p.strip()] for p in product_array}
        print('FINALY???', product_dictionary)
        image_ = soup.find_all("img")

        image_sources = []

        for image in image_:
            image_sources.append(image.get("src"))

        def get_logo(word, list_of_strings):
            for string in list_of_strings:
                if word in string:
                    return string
            return None

        # Image URL to pass into HTML
        logo_image = get_logo(inputUser, image_sources)

        return render_template(
            "demoBlocks.html",
            img_url=logo_image,
            value=re.sub(r"\s+", " ", response_chat),
            dic=product_dictionary,
        )
    elif request.method == "GET":
        chatty = "Hello and welcome to our SC bot. Feel free to ask me about the ways Movable ink can help your company"

        # Image URL to pass into HTML
        logo_image = "static/images/logo.jpg"

        return render_template("index.html", img_url=logo_image, value=chatty)
