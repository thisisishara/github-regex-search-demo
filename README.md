# github-public-search-demo
A simple Python script that searches public GitHub repos for a specific regex pattern

## Caution!
This scipt is useful for finding publicly exposed well-known regex patterns. This script must not be used with the intention of causing any harm and it was implemented for educational and research purposes only. If used this for any illegal activities, the original author cannot be held accountable.

## Limitations
GitHub API rate limitations are applicable. Provide with an Auth token to extend the rate limits of the unauthenticated API requests.  
You can find more details on rate limitations [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28) and [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#increasing-the-unauthenticated-rate-limit-for-oauth-apps)

_Note:_ Unless created the "secrets.txt" and ".env", it is more likely that the script won't work as expected.
