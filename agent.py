from google import genai
import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
gmaps = googlemaps.Client(key=os.getenv("MAPS_API_KEY"))

def search_places(query, location, radius=5000):
    geocode = gmaps.geocode(location)
    if not geocode:
        return "Location not found."
    
    lat = geocode[0]["geometry"]["location"]["lat"]
    lng = geocode[0]["geometry"]["location"]["lng"]
    
    places = gmaps.places_nearby(
        location=(lat, lng),
        radius=radius,
        keyword=query
    )
    
    results = []
    for place in places.get("results", [])[:5]:
        name = place.get("name")
        address = place.get("vicinity")
        rating = place.get("rating", "N/A")
        results.append(f"- {name} | {address} | Rating: {rating}")
    
    return "\n".join(results) if results else "No places found."

def ask_agent(user_query, location):
    places_data = search_places(user_query, location)
    
    prompt = f"""
    User is looking for: {user_query}
    Location: {location}
    
    Here are nearby places found:
    {places_data}
    
    Give a helpful, concise recommendation based on this data.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text, places_data