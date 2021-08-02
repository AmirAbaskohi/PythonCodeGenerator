from github import Github
from datetime import datetime
import time
import os

ACCESS_TOKEN = open("token.txt", "r").read()
github = Github(ACCESS_TOKEN)

SECONDS_IN_A_DAY = 86400

end_time = time.time()
start_time = end_time - SECONDS_IN_A_DAY

for i in range(3):
    start_time_str = datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d")
    end_time_str = datetime.utcfromtimestamp(end_time).strftime("%Y-%m-%d")

    query = f"language:python created:{start_time_str}..{end_time_str}"
    print(query)

    start_time -= SECONDS_IN_A_DAY
    end_time -= SECONDS_IN_A_DAY

    result = github.search_repositories(query)
    print(result.totalCount)

    for repository in result:
        print(repository.clone_url)
        os.system(f"git clone {repository.clone_url} repos/{repository.owner.login}/{repository.name}")
    
