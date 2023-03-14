import requests
import base64
import pandas as pd

#a simple program that creates a CSV file with the name of repositories and their descriptions
# belonging to an account with the help of the GitHUB API
token=""
username=""

class MyGitHub:
    def __init__(self,username,token):
        self.username=username
        self.token = token
        self.headers = {'Authorization': self.token}
    def get_repos(self):
        url = f"https://api.github.com/users/{self.username}/repos"
        response = requests.get(url, headers=self.headers)
        return response.json()

dataframe = pd.DataFrame (columns = ["Repository name","Repository description"])

api_instance =MyGitHub(username,token)
repos=api_instance.get_repos()
for repo in repos:
    reponame=(repo["name"])
    encoded_readme=requests.get(f"https://api.github.com/repos/{api_instance.username}/{reponame}/readme",headers=api_instance.headers).json()["content"]
    decoded_readme = base64.b64decode(encoded_readme).decode("utf-8")
    new_row = pd.DataFrame([[reponame,decoded_readme]], columns=["Repository name","Repository description"])
    dataframe = dataframe.append(new_row)
dataframe.to_csv("repository_data.csv")

