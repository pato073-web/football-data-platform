from app.services.api_football import get_from_api

countries = get_from_api("countries")


print(len(countries))
print(countries[:3])