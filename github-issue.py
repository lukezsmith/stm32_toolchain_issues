import sys
import requests
import csv
from datetime import datetime
def extract_github_owner_repo(url):
    # Remove trailing slash if present
    url = url.rstrip('/')

    # Split the URL by '/'
    parts = url.split('/')

    # Extract the owner's username and repository name
    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def scrape_issues(owner, repo):
    params = {
        'sort': 'created',
        'direction': 'asc'
    }
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues?state=open", params=params)
    if response.status_code == 200:
        issues = response.json()
        return issues
    else:
        print("Failed to retrieve issues:", response.status_code)
        return []

def write_issues_to_file(repo_name, issues):
    with open(f"{repo_name}_issues_{datetime.now().date().strftime('%d%m%y')}.csv", 'w') as file:
        writer = csv.writer(file)
        for issue in issues:
            writer.writerow([issue["number"], issue["title"], issue["url"]])

def main():
    # Check if the URL argument is provided
    if len(sys.argv) != 2:
        print("Usage: python get_issues.py <Github Repository URL>")
        return
    
    url = sys.argv[1]
    owner, repo = extract_github_owner_repo(url)
    
    issues = scrape_issues(owner, repo)
    write_issues_to_file(repo, issues)

if __name__ == "__main__":
    main()