import os
import requests
from dotenv import load_dotenv


class GitHub:

    def __init__(self):
        self.base_url = 'https://api.github.com'
        self.total = []


    def get_repos(self, username: str, perPage: int, page: int):

        endpoint = f"{self.base_url}/users/{username}/repos?per_page={perPage}$page={page}"

        try:

            response = requests.get(
                url=endpoint, headers={
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
            )

            response.raise_for_status()

            data = response.json()

            return data
        
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 403:
                print("Rate Limit Achieved. Please you 'ill have to wait an hour.")
                SystemExit("Rate Limit Encountered.")
            else:
                print(f"Some error occured: {error.response.status_code} - {error.response.reason}")
                SystemExit("Something went wrong")

    def fetch_repos(self, username: str):

        perPage=20
        page = 1

        while True:
            repositories = self.get_repos(username, perPage, page)

            if len(repositories) == 0:
                print(f"The {username} have no repository\n")
                break

            self.total.extend([repository['name'] for repository in repositories])

            if len(self.total) >= 50:
                self.total = self.total[:50]
                break
            
            page = page + 1

    def display(self):

        repos = "\n".join(f"{i} - {self.total[i]}" for i in range(len(self.total)))

        print(f"""\n GitHub Report\n -------------- \n {repos}""")

if __name__ == "__main__":

    load_dotenv()
    github = GitHub()

    while True:
        username = input("Enter a user name: ")
        github.fetch_repos(username)
        github.display()
        leave = input("Would you like to continue? (y/n):  ") or "n"
        if leave.lower() == 'n':
            break