from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import io

app = Flask(__name__)

def get_emails_and_contacts_from_url(url):
    """Extract emails, valid contact numbers (at least 10 digits), and page title from the provided URL."""
    emails = set()
    contacts = set()
    title = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            # Extract emails
            emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
            
            # Extract valid contact numbers (at least 10 digits)
            contacts.update(re.findall(r'\b(?:\+?\d{1,3})?[\s.-]?\(?\d{3,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4}\b', text))
            
            title = soup.title.string if soup.title else "No title found"
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return emails, contacts, title

def find_emails_and_contacts_by_keyword(keyword, num_results=10):
    """Search for emails and valid contact numbers by keyword using Google search, and retrieve page titles."""
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
    """API endpoint to get emails and valid contact numbers based on a keyword search."""
    data = request.json
    keyword = data.get('keyword')
    num_results = data.get('num_results', 10)
    results = find_emails_and_contacts_by_keyword(keyword, num_results)

    # Write emails, valid contact numbers, titles, and URLs to CSV
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
        headers={"Content-Disposition": f"attachment;filename={keyword}_emails_contacts.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
