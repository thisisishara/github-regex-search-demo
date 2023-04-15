import os
import requests
import re
from datetime import datetime, timedelta

# Set up GitHub API authentication
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
CONTENT_REGEX = os.getenv("CONTENT_REGEX")


def trigger_search() -> None:
    headers = (
        {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
        if GITHUB_ACCESS_TOKEN
        else {}
    )

    topics = ["chatgpt", "gpt", "python"]

    if len(topics) < 1:
        print(f"you need to specify at least 1 topic")

    topics_str = (
        "+".join(["topic:" + topic for topic in topics])
        if len(topics) > 1
        else f"topic:{topics[0]}"
    )
    topics_str = f"{topics_str}+"

    print(f"topics: \n{topics_str}\n")

    # Calculate the date and time n days ago
    yesterday = datetime.now() - timedelta(days=30)
    yesterday_str = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_str = f"created:>{yesterday_str}"

    # Define the regex pattern to search for
    regex_pattern = rf"{CONTENT_REGEX}"

    # Search for repositories that match a certain topic and were created within the last 24 hours
    search_url = f"https://api.github.com/search/repositories?q={topics_str}{time_str}"
    response = requests.get(search_url, headers=headers)
    print(f"search url: {search_url}\n")
    # print(f"response from repo search: \n{response.json()}")

    if response.status_code != 200 or "items" not in response.json():
        print(f"Invalid response")

    json_response = response.json()
    repo_count = len(json_response["items"])
    print(f"REPO COUNT: {repo_count}\n")

    repos = response.json()["items"]

    # Loop through each repository and search for the regex pattern
    for repo_id, repo in enumerate(repos):
        print(
            f"inspecting repo ({repo_id+1}/{repo_count}): {repo['name']}\n{repo['html_url']}"
        )

        contents_url = f"https://api.github.com/repos/{repo['full_name']}/contents"
        response = requests.get(contents_url, headers=headers)
        contents = response.json()

        if response.status_code == 403:
            print(f"API Rate limit exceeded for the IP")

        for file in contents:
            if file["type"] == "file":
                file_url = file["download_url"]
                response = requests.get(file_url, headers=headers)
                file_contents = response.text

                # Search for the regex pattern
                matches = re.findall(regex_pattern, file_contents)
                if matches:
                    # Record the repository name, file name, and line number
                    repo_name = repo["full_name"]
                    file_name = file["path"]
                    for match in matches:
                        # line_number = file_contents.count("\n", 0, match.start()) + 1
                        # print(f"{repo_name}/{file_name}:{line_number}: {match}")
                        print(f"{repo_name}/{file_name}: {match}")
        print("\n")


if __name__ == "__main__":
    trigger_search()
