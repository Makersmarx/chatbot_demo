import requests
from bs4 import BeautifulSoup


URL = "https://movableink.com/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
# image_ = soup.find_all("div")

image_ = soup.find_all("svg")

for index, i in enumerate(image_):
    with open(f"image_{index}.svg", "w") as f:
        f.write(str(i))

# results = soup.find_all("div")
# logos = soup.find(class_="Footer__LinkedLogo-sc-1mmo66d-9 gxZSWc")

# for i in results:
#     if logos in i:
#         with open("test.html", "w") as file:
#             file.write(i.prettify())
#     else:
#         print("Cant Find It")


# with open("test.html", "w") as file:
#     file.write(results.prettify())
