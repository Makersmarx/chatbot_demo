from flask import Flask, render_template, request
import google.generativeai as palm
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import re
import json

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
        inputUserOne = request.form.get("textEntry")
        inputUserTwo = request.form.get("textEntryTwo")
        prompt = f"How can Movable Ink help {inputUserOne} with their email marketing spoken as a friendly solutions consultant name Inky"

        response = palm.generate_text(**defaults, prompt=prompt)
        response_chat = response.result

        company_prompt = f"What category of company is ${inputUserOne}?"
        company_response = palm.generate_text(**defaults, prompt=company_prompt)
        company_type = company_response.result

        print("COMPANY TYPE", company_type)

        URL = f"https://worldvectorlogo.com/logo/{inputUserOne}"
        getURL = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(getURL.text, "html.parser")

        getProduct = requests.get(
            inputUserTwo,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        company_soup = BeautifulSoup(getProduct.text, "html.parser")
        image_dictionary = {}
        final_dictionary = {}
        alt_texts = []
        images_ = company_soup.find_all("img")

        if (
            company_type == "retailer"
            or "clothing"
            or "Clothing & Accessories" in company_type
        ):
            for i in range(len(images_) - 1):
                if images_[i] is not None and hasattr(images_[i], "get"):
                    text = images_[i].get("alt")
                    if bool(text):
                        alt_texts.append(images_[i].get("alt"))
                        image_dictionary[text] = images_[i].get("src")

            alt_strings = "|".join(alt_texts)
            alt_prompt = f"Given the | separated list ${alt_strings}, can you identify 4 different products and return them as a | separated list"
            alt_response = palm.generate_text(**defaults, prompt=alt_prompt)
            product_array = alt_response.result.split("|")
            for product in product_array:
                final_dictionary[product.strip()] = image_dictionary[product.strip()]

        elif bool(company_type):
            getDestinations = requests.get(
                "https://www.marriott.com/en/destinations/dublin.mi",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            travel_soup = BeautifulSoup(getDestinations.text, "html.parser")
            image_tags = travel_soup.find_all("pre", text=True)
            hotel_images = []

            for tag in image_tags:
                if "hotelsList" in tag.getText():
                    hotelsList = tag.getText()
                    hotelObj = json.loads(hotelsList)
                    for item in hotelObj["hotelsList"]:
                        if "image" in item:
                            hotel_images.append(item["image"])

            hotel_image_strings = "|".join(hotel_images)
            hotel_tags = travel_soup.find_all("a", href=True)
            hotel_list = []
            for a in hotel_tags:
                hotel_list.append(a["href"])
            hotel_strings = "|".join(hotel_list)
            hotel_prompt = f"Given the | separated list of hyperlinks ${hotel_strings}, can you identify 4 different hotels and return the name as a | separated list"
            hotel_response = palm.generate_text(**defaults, prompt=hotel_prompt)
            hotel_matching_prompt = f"given the | separated list of image src links: ${hotel_image_strings}, return a object an where the key  hotel in this | separted list ${hotel_response.result} and formatted with proper spacing and capitalization. The value is the src link. The key and values should be enclosed in double quotes not single quotes"
            matches_response = palm.generate_text(
                **defaults, prompt=hotel_matching_prompt
            )
            hotel_dictionary = json.loads(matches_response.result)
            for hotel in hotel_dictionary.keys():
                final_dictionary[hotel] = hotel_dictionary[hotel]

        def get_logo(word, list_of_strings):
            for string in list_of_strings:
                if word in string:
                    return string
            return None

        # Image URL to pass into HTML
        image_ = soup.find_all("img")

        image_sources = []

        for image in image_:
            image_sources.append(image.get("src"))

        logo_image = get_logo(inputUserOne, image_sources)

        return render_template(
            "demoBlocks.html",
            img_url=logo_image,
            value=re.sub(r"\s+", " ", response_chat),
            dic=final_dictionary,
        )

    elif request.method == "GET":
        chatty = "Hello and welcome to our SC bot. Please enter your company name and website"

        # Image URL to pass into HTML
        logo_image = "static/images/logo.jpg"

        return render_template("index.html", img_url=logo_image, value=chatty)
