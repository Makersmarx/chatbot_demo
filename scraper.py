import requests
from bs4 import BeautifulSoup


URL = "https://movableink.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div")

with open("test.html", "w") as file:
    file.write(results.prettify())
