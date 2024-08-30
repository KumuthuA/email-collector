from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import io

app = Flask(__name__)

def get_emails_from_url(url):
    """Extract emails and page title from the provided URL."""
    emails = set()
    title = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
            title = soup.title.string if soup.title else "No title found"
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return emails, title

def find_emails_by_keyword(keyword, num_results=10):
    """Search for emails by keyword using Google search, and retrieve page titles."""
    search_results = search(keyword, num=num_results)
    all_results = []
    for url in search_results:
        emails, title = get_emails_from_url(url)
        if emails:
            all_results.append({
                "url": url,
                "title": title,
                "emails": emails
            })
    return all_results

@app.route('/api/emails', methods=['POST'])
def get_emails():
    """API endpoint to get emails based on a keyword search."""
    data = request.json
    keyword = data.get('keyword')
    num_results = data.get('num_results', 10)
    results = find_emails_by_keyword(keyword, num_results)

    # Write emails, titles, and URLs to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Keyword", "Title", "URL", "Email"])
    
    for result in results:
        for email in result["emails"]:
            writer.writerow([keyword, result["title"], result["url"], email])
    
    output.seek(0)
    
    # Return the CSV file as a response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={keyword}_emails.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
