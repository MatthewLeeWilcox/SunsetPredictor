def get_sunset_time(latitude, longitude, date):
    # Build the API request URL
    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}&formatted=0"


    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Extract the sunset time
    sunset = data['results']['sunset']
    
    return sunset


locations = {"Golden, CO": [39.7555, -105.2211, 'America/Denver']}