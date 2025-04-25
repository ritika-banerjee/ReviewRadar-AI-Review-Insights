from serpapi.google_search import GoogleSearch
import json
import time
import pprint

API_KEY = "25ce6087971506858454de92275bc3778b82982d0e8d99180ccc7f7a34244b11"

def fetch_reviews(business_name, location):

    params_search = {
            "engine": "google_maps",
            "q": business_name + " " + location,
            "api_key": API_KEY,
            "type": "search"
        }
        
    search = GoogleSearch(params_search)
    search_results = search.get_dict()


    if "place_results" in search_results:
        place_results = search_results["place_results"]
            
            # Get place_id from place_results
        place_id = place_results.get("place_id")

        # Check if we have local_results (list of businesses)
    elif "local_results" in search_results and search_results["local_results"]:
        business = search_results["local_results"][0]

            
            # Get data_id from the business result
        place_id = business.get("place_id")

        
        # STEP 2: Use place_id to fetch reviews
    params_reviews = {
            "engine": "google_maps_reviews",
            "place_id": place_id,
            "api_key": API_KEY,
            "sort": "newest_first"
        }
        
    reviews_search = GoogleSearch(params_reviews)
    reviews_results = reviews_search.get_dict()
        
        # Extract the reviews
    reviews = reviews_results.get("reviews", [])
        
    return reviews