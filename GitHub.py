import requests
import json

tokenFile = open("ghtoken.txt", 'r')
token = tokenFile.readline()
tokenFile.close()

headers = {"Authorization" : f"Bearer {token}",
    "Accept": "application/vnd.github+json"}

def createIssue(Repositoryname : str, title :str, body :str):
    data = {"title": title, "body": body}
    url = f"https://api.github.com/repos/Caltinor/{Repositoryname}/issues"
    requests.post(url,data=json.dumps(data),headers=headers)