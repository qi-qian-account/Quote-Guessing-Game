import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice
# list to store scraped data
all_quotes = []

# constant url
base_url = "http://quotes.toscrape.com/"

# non-constant url
url = "/page/1/"

while url:

    # concatenate both urls
    # make request
    res = requests.get(f"{base_url}{url}")
    print(f"Now Scraping nb{base_url}{url}")
    soup = BeautifulSoup(res.text, 'html.parser')

    # extract all elements
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_="text").get_text(),
            "author": quote.find(class_="author").get_text(),
            "bio-link": quote.find("a")["href"]
        })
    next_btn = soup.find(class_="next")
    url = next_btn.find("a")["href"] if next_btn else None
    sleep(2)

# randomly choose one quote from all_quotes
quote = choice(all_quotes)
remaining_guesses = 4
print("Here's a quote: ")
print(quote["text"])

guess = ''
while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
    guess = input(
        f"Who said this quote? Guesses remaining {remaining_guesses}"
    )

    if guess == quote["author"]:
        print("Congratulations. The answer is correct.")
        break
    remaining_guesses -= 1

    # if player did not get the first guess right, give hint on author's birth date and birth place
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(
            f"Here's a hint: The author was born on {birth_date} {birth_place}"
        )
    
    # if player didn'tmget the second guess right either
    # give hint on the first letter of author's first name
    elif remaining_guesses == 2:
        print(
            f"Here's a hint. The author's first name starts with {quote['author'][0]}"
        )
    
    # if player didn'tmget the third guess right either
    # give hint on the first letter of author's last name
    elif remaining_guesses == 1:
        last_initial = quote["author"].split(" ")[1][0]
        print(
            f"Here's a hint. The author's last name starts with {last_initial}"
        )
    
    else:
        print(
            f"Sorry, you ran out of guesses. The answer is {quote['author']}"
        )