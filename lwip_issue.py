import requests
from bs4 import BeautifulSoup
from datetime import datetime
def scrape_issues(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the issues
        issues = soup.find_all('tr', class_='priore')

        # write issues
        with open(f"lwip_issues_{datetime.now().date().strftime('%d%m%y')}.txt", "w") as file:
            for issue in issues:
                issue_fields = issue.find_all('a')
                id = issue_fields[0].get_text()
                title = issue_fields[1].get_text()
                url = issue_fields[1].get('href')
                file.write(f"[{id}] {title}\n{'https://savannah.nongnu.org/bugs/'+url}\n")

    else:
        print("Failed to fetch page:", response.status_code)

def main():
    # URL of the page with issues
    url = "https://savannah.nongnu.org/bugs/?group=lwip&func=browse&set=custom&msort=0&status_id[]=1&resolution_id[]=0&assigned_to[]=0&category_id[]=0&bug_group_id[]=0&advsrch=0&msort=0&chunksz=150&spamscore=5&report_id=100&sumORdet=&morder=date%3C&order=date#results"

    # Scrape the issues
    scrape_issues(url)

if __name__ == "__main__":
    main()