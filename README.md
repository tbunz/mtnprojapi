# mtnprojapi
## https://climbingapi.com/
### Public facing API for mountainproject.com
This project is entirely educational and not being used to generate any income. It is only public facing in order to explore and showcase skills related to web development. Other than me, very few users will ever interact with this site.

### Summary
- A public facing API 
- All data provided is obtained via requests to mountainproject.com
- Response from mountainproject.com is parsed and relevant information is provided in JSON format

### Usage
`https://climbingapi.com/` \
Sanity check home path. Useful for testing. Returns:
```
{"sane?":"yes"}
```
\
`https://climbingapi.com/search/<query>` \
`<query>` is a string of text to search on mountainproject.com. Returns a list of climbs relevant to the search, and the number of climbs returned:
```
{
    "climbs": [
                  {
                      "link": <string link to rock climb's page at mountainproject.com>,
                      "location": <string>,
                      "name": <string>,
                      "rating": <string>
                  },
                  {
                      "link": <string link to rock climb's page at mountainproject.com>,
                      "location": <string>,
                      "name": <string>,
                      "rating": <string>
                  },

                  ...

              ],

  "length": <int>
}
```
### Summary of Tools
- Python (Flask framework, Selenium for requests/parsing)
- Flask app runs requests, parsing, and path handling
- Gunicorn as app web service to run Flask app publicly
- Nginx as public facing reverse proxy, forwarding requests to Gunicorn service

### Citations
- Mountain Project (all information about rock climbs including: static images, names, descriptions, comments, reviews, GPS data)
