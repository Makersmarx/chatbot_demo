import requests
from bs4 import BeautifulSoup


URL = "https://movableink.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div")
logos = soup.find(class_="Footer__LinkedLogo-sc-1mmo66d-9 gxZSWc")

for i in results:
    if logos in i:
        print("I AM HERE" + str(i))


# with open("test.html", "w") as file:
#     file.write(results.prettify())
