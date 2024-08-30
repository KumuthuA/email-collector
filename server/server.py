from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import io

app = Flask(__name__)

def get_emails_and_contacts_from_url(url):
    """Extract emails, contact numbers, and page title from the provided URL."""
    emails = set()
    contacts = set()
    title = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))      
            contacts.update(re.findall(r'\+?\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}', text))
            title = soup.title.string if soup.title else "No title found"
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return emails, contacts, title

def find_emails_and_contacts_by_keyword(keyword, num_results=10):
    """Search for emails and contact numbers by keyword using Google search, and retrieve page titles."""
    search_results = search(keyword, num=num_results)
    all_results = []
    for url in search_results:
        emails, contacts, title = get_emails_and_contacts_from_url(url)
        if emails or contacts:
            all_results.append({
                "url": url,
                "title": title,
                "emails": emails,
                "contacts": contacts
            })
    return all_results

@app.route('/api/emails', methods=['POST'])
def get_emails():
    """API endpoint to get emails and contact numbers based on a keyword search."""
    data = request.json
    keyword = data.get('keyword')
    num_results = data.get('num_results', 10)
    results = find_emails_and_contacts_by_keyword(keyword, num_results)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Keyword", "Title", "URL", "Email", "Contact Number"])
    
    for result in results:
        for email in result["emails"]:
            writer.writerow([keyword, result["title"], result["url"], email, ""])
        for contact in result["contacts"]:
            writer.writerow([keyword, result["title"], result["url"], "", contact])
    
    output.seek(0)
    
    # Return the CSV file as a response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={keyword}_contacts.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
