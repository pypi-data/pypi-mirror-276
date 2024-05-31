import requests
import json


def fetch_weather_data(city: str = "Huntsville, Al") -> str:
    """
    Fetch near real-time weather data for a city using wttr.in and return the most valuable temperature metrics.

    Args:
        city (str): The name of the city (e.g., "Austin, Tx").

    Returns:
        str: A string containing the most valuable temperature metrics.

    Raises:
        Exception: If the request fails or the response is invalid.
    """
    url = f"http://wttr.in/{city}"
    params = {"format": "j1"}  # JSON format
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract the most valuable temperature metrics
        temp_c = data["current_condition"][0]["temp_C"]
        feels_like_c = data["current_condition"][0]["FeelsLikeC"]
        humidity = data["current_condition"][0]["humidity"]
        wind_speed = data["current_condition"][0]["windspeedKmph"]
        visibility = data["current_condition"][0]["visibility"]
        date_time = data["current_condition"][0]["observation_time"]

        return f"Date/Time: {date_time}, Temperature: {temp_c}°C, Feels Like: {feels_like_c}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} Kmph, Visibility: {visibility} Km"

    except requests.RequestException as e:
        raise Exception(f"Failed to fetch weather data: {e}")
    except (ValueError, KeyError):
        raise Exception("Invalid response format.")


# out = get_openai_function_schema_from_func(fetch_weather_data, name="fetch_weather_data", description="Fetch near real-time weather data for a city using wttr.in and return the most valuable temperature metrics.")
# print(out)

# import json


def parse_city_state(json_str):
    """
    Parse the city and state from a JSON string.

    Args:
        json_str (str): The JSON string to parse.

    Returns:
        str: The city and state, or None if the city and state could not be parsed.
    """
    if not isinstance(json_str, str):
        print("Input is not a string")
        return None

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("Invalid JSON")
        return None

    if "function" not in data or "parameters" not in data["function"]:
        print("Missing 'function' or 'parameters' key in JSON")
        return None

    parameters = data["function"]["parameters"]

    if (
        "properties" in parameters
        and "city" in parameters["properties"]
        and "default" in parameters["properties"]["city"]
    ):
        # Handle the first format
        return parameters["properties"]["city"]["default"]
    elif "city" in parameters:
        # Handle the second format
        return parameters["city"]

    print("Missing 'city' key in JSON")
    return None


# # Example usage
# json_str = '{"type": "function", "function": {"description": "Fetch near real-time weather data for a city using wttr.in and return the most valuable temperature metrics.", "name": "fetch_weather_data", "parameters": {"type": "object", "properties": {"city": {"type": "string", "default": "Huntsville, Al", "description": "city"}}, "required": []}}}'
# city_state = parse_city_state(json_str)
# print(city_state)  # Outputs: 'Huntsville, Al'

# # Example usage
# city = "Miami, Fl"

# try:
#     weather_data = fetch_weather_data(city)
#     print("Weather Data:", weather_data)
# except Exception as e:
#     print(e)
