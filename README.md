## How to run a server
Just install all the needed packages (virtualenv is highly recommended)

`pip install -r requirements.txt`

and run the application using the following command:
 
`python app.py`

## Endpoints

`/games`

- returns all the parsed games by categories 

`/games?categories=someCategory`

- returns list of games by requested category according to the query parameter 

Examples:

http://127.0.0.1:5000/games

http://127.0.0.1:5000/games?category=Console%20classics


## Used libs
* https://aiohttp.readthedocs.io/
* https://aiohttp-cache.readthedocs.io/

## Info
I've decided to use async libs and cache cuz we have the external call to 3rd party resource (google web site), and it takes about 1 second per request.
And it is not good for 2 reasons: 
1) A client should wait at least one 1 second (create a lot of workers it's resource wasting)
2) We will generate a lot of requests to the google and it's a potential risk to get the ban.