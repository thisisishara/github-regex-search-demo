#  github-public-search-demo

A simple Python script that searches public GitHub repos for a specific regex pattern  
<br>

##  Caution!
This scipt is useful for finding publicly exposed well-known regex patterns. This script must not be used with the intention of causing any harm and it was implemented for educational and research purposes only. If used this for any illegal activities, the original author cannot be held accountable.  
<br>

##  Limitations
GitHub API rate limitations are applicable. Provide with an Auth token to extend the rate limits of the unauthenticated API requests.  

You can find more details on rate limitations [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28) and [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#increasing-the-unauthenticated-rate-limit-for-oauth-apps)  
<br>

_Note:_ Unless created the "secrets.txt" and ".env", it is more likely that the script won't work as expected.  
<br>


##  How to run github_search.py?
1. Create a new virtual environment with the latest version of Python
2. Install the requirements with `pip install -r requirements.txt`
3. Create a `.env` in the project root and follow the instructions given in `.env.example`. You can leave `GITHUB_ACCESS_TOKEN` empty if you are not going to use auth. Providing `CONTENT_REGEX` is also optional as you can specify the regex at run time by passing the --regex argument
4. Create a `secrets.txt` to persist results manually if required. More info on secret persisting later [refer step 6]
5. Trigger public github repo search by executing the `github_search.py` script with necessary arguments with following command.

```Python
python github_search.py github
```
Following arguments are supported by the positional argument `github`.
| OptionalArgument | Default Value | Usage |
|--|--|--|
| -r, --regex | RegEx specified in the `.env` file | This regex will be searched in every candidate repo contents. | 
| -q, --query | "chatgpt" | Used to find public repositories. | 
| -d, --days | 30 | An integer to determine how many days to traceback. All repositories created after the specified number of dates from today in the past are only considered for the search. | 
| -p, --page | 1 | By default, the first 30 repos in the 1st result page are shown. To navigate further down the resultset, --page can be used. |

6. Secrets can be persisted for future reference using the following command.

```Python
python github_search.py add --key <secret_you_found>
```

7. You can also check if a secret already exists in the list of persisted secrets by execting the following command.

```Python
python github_search.py search --key <secret_you_found>
```