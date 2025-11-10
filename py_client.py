import requests
import logging
import os
import dotenv
import pprint
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
dotenv.read_dotenv()

log=logging.getLogger(__name__)
scretkey=os.environ.get('OMDB_API_KEY')
endpoint="http://www.omdbapi.com/?apikey=9ed44e6f"

log.debug(endpoint.format(scretkey))
response=requests.get(endpoint,{'r':'json','t':'tr'})
pprint.pprint(response.json())


#first application of movie OMDB what this application to do 
# 1- client will be able to search the movie tite 
# 2- client will be able to add movie favorite list and remove movie from the list 


