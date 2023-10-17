import requests
from bs4 import BeautifulSoup
url = "https://realpython.github.io/fake-jobs/"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

container = soup.find(id="ResultsContainer")

cards = soup.find_all("div", class_="card")
job_titles = []
for card in cards:
    print(card, end="\n"*2)
    title = soup.find("h2", class_="title is-5")
    print(title)
    job_titles.append(title)

print(job_titles)
