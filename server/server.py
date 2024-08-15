from flask import Flask, request, Response, send_from_directory
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import csv
import io

app = Flask(__name__)

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
    for url in search_results:
        emails = get_emails_from_url(url)
        all_emails.update(emails)
    return all_emails

@app.route('/api/emails', methods=['POST'])
def get_emails():
    data = request.json
    keyword = data.get('keyword')
    num_results = data.get('num_results', 100)
    emails = find_emails_by_keyword(keyword, num_results)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([keyword])  
    for email in emails:
        writer.writerow([email])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={keyword}_emails.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
