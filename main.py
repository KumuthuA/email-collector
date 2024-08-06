import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search

def get_emails_from_url(url):
    emails = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return emails

def find_emails_by_keyword(keyword, num_results=10):
    search_results = search(keyword, num=num_results)
    all_emails = set()
    # print(list(search_results))
    for url in search_results:
        emails = get_emails_from_url(url)
        all_emails.update(emails)
    return all_emails

if __name__ == "__main__":
    keyword = "lithium ion battery in Sri Lanka"
    num_results = 10
    emails = find_emails_by_keyword(keyword, num_results=num_results)
    if emails:
        print(f"Found the following email addresses:\n{', '.join(emails)}")
    else:
        print("No email addresses found.")
