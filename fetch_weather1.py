import requests
import json

def fetch_weather_data():
    # Make API request
    response = requests.get('https://api.openweathermap.org/data/2.5/HERE YOUR LOCATION AND API KEY')
    data = response.json()
    # Write data to file
    with open('/path/to/store/file', 'w') as file: 
        json.dump(data, file)

if __name__ == '__main__':
    fetch_weather_data()
