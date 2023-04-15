import argparse
import os
from typing import Text
import requests
import re
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

# Set up GitHub API authentication
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
CONTENT_REGEX = os.getenv("CONTENT_REGEX")


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description="Search GitHub public repos for regex and Add or search results to a text file."
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    search_repos_parser = subparsers.add_parser(
        "github", help="Search for a regex in public GitHub repos."
    )
    search_repos_parser.add_argument(
        "-r", "--regex", type=str, help="The regex pattern to search for in the repos."
    )
    search_repos_parser.add_argument(
        "-q", "--query", type=str, help="A query to search repos with."
    )
    search_repos_parser.add_argument(
        "-d", "--days", type=int, help="Number of days to traceback the origin."
    )
    search_repos_parser.add_argument(
        "-p", "--page", type=int, help="Number of the result page to navigate through repos."
    )

    add_parser = subparsers.add_parser("add", help="Add a new key to the secrets file.")
    add_parser.add_argument(
        "-k", "--key", type=str, required=True, help="The secret to add to the file."
    )

    search_file_parser = subparsers.add_parser(
        "search", help="Search for a key in the secrets file."
    )
    search_file_parser.add_argument(
        "-k",
        "--key",
        required=True,
        type=str,
        help="The secret to search for in the file.",
    )

    return parser


def trigger_search(regex: Text, query: Text, days: int, page: int = 1) -> None:
    headers = (
        {"Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"}
        if GITHUB_ACCESS_TOKEN
        else {}
    )

    if headers:
        print(f"Accessing GitHub API with Authentication...")

    # topics = ["gpt", "python", "chat gpt", "gpt-3", "gpt3", "gpt 3", "generative ai", "generativeai", "openai", "open ai"]
    topics = []

    if len(topics) < 1:
        print(f"[WARNING] ** You have not specified any topics")

        topics_str = ""
    else:
        topics_str = (
            "+".join(["topic:" + topic for topic in topics])
            if len(topics) > 1
            else f"topic:{topics[0]}"
        )
        topics_str = f"+{topics_str}"

        print(f"TOPICS: \n{topics_str}\n")

    # Calculate the date and time n days ago
    days_ = days if days else 30
    yesterday = datetime.now() - timedelta(days=days_)
    yesterday_str = yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_str = f"+created:>{yesterday_str}"

    # Define the regex pattern to search for
    regex_pattern = rf"{CONTENT_REGEX}" if not regex else regex
    query_pattern = query if query else "chatgpt"

    # Search for repositories that match a certain topic and were created within the last 24 hours
    search_url = f"https://api.github.com/search/repositories?q={query_pattern}{topics_str}{time_str}&sort=stars&order=desc&page={page}"
    response = requests.get(search_url, headers=headers)
    print(f"SEARCH URL: {search_url}\n")
    # print(f"response from repo search: \n{response.json()}")

    if response.status_code != 200 or "items" not in response.json():
        print(f"[ERROR] ** Invalid response")
        return

    json_response = response.json()
    repo_count = len(json_response["items"])
    print(f"REPO COUNT: {repo_count}\n")

    repos = response.json()["items"]

    # Loop through each repository and search for the regex pattern
    print(f"\n[INFO] ** Searching for the regex: {regex_pattern}\n")
    for repo_id, repo in enumerate(repos):
        print(
            f"INSPECTING REPO [{repo_id+1}/{repo_count}]: \n{repo['name']}\n{repo['html_url']}"
        )

        contents_url = f"https://api.github.com/repos/{repo['full_name']}/contents"
        response = requests.get(contents_url, headers=headers)
        contents = response.json()
        print(response.status_code)

        if response.status_code == 403:
            print(f"\n[ERROR] ** API Rate limit exceeded for the IP")
            return
        if response.status_code == 404:
            print(f"[ERROR] ** Repository is empty. Skipping...\n")
            continue

        for file in contents:
            if file["type"] == "file":
                file_url = file["download_url"]
                response = requests.get(file_url, headers=headers)
                file_contents = response.text

                # Search for the regex pattern
                matches = re.findall(regex_pattern, file_contents)
                if matches:
                    # Record the repository name, file name, and line number
                    file_name = file["path"]
                    for match in matches:
                        # line_number = file_contents.count("\n", 0, match.start()) + 1
                        # print(f"{repo_name}/{file_name}:{line_number}: {match}")
                        if search_key_in_file(key=match):
                            status = "DEPRECATED"
                        else:
                            status = "UNSEEN"
                        print(f"*** {file_name}:\t{match} -------- [{status}]")
        print("\n")


def add_key_to_file(key):
    with open("secrets.txt", "r") as f:
        if key in f.read():
            print(f"Key {key} already exists in file.")
        else:
            with open("secrets.txt", "a") as f:
                f.write(key + "\n")
            print(f"Successfully added the {key}.")


def search_key_in_file(key):
    with open("secrets.txt", "r") as f:
        for line in f:
            if line.strip() == key:
                return True
    return False


if __name__ == "__main__":
    try:
        parser = create_arg_parser()
        args = parser.parse_args()

        if args.command == "github":
            trigger_search(regex=args.regex, query=args.query, days=args.days, page=args.page)
        elif args.command == "add":
            add_key_to_file(args.key)
        elif args.command == "search":
            if search_key_in_file(args.key):
                print(f"Key {args.key} found in file.")
            else:
                print(f"Key {args.key} not found in file.")
        else:
            print(f"[INFO] ** No args specified. GitHub search is triggered...")
            trigger_search()
    except KeyboardInterrupt:
        print(f"Gracefully terminating the script...")
