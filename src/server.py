# Basic
import os
import fastmcp
import requests
from dotenv import load_dotenv
from mcp.server.auth.middleware.auth_context import get_access_token

# FastMCP shit
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

# Load environmental variables
load_dotenv(override=True)

# Validate JWT is issued by trusted token
#verifier = JWTVerifier(
#    jwks_uri="https://login.microsoftonline.com/common/discovery/v2.0/keys",
#    issuer=f"https://sts.windows.net/{os.getenv('ENTRA_ID_TENANT_ID')}/",
#    audience="mcp-production-api"
#)

mcp = FastMCP(
    name="WeatherAssistant",
    instructions="""
        This server provides one tool: get_weather(city).
        It returns current weather conditions for a city using WeatherAPI.
        Response includes `location` and `current` objects (C/F units, wind, humidity, condition, etc.).
    """
)

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather conditions for a city.

    Args:
        city: City name or query string (for example: "London", "New York", "Tokyo").

    Returns:
        A JSON object from WeatherAPI `current.json` containing:
        - location: name, region, country, lat/lon, timezone, local time
        - current: temperature (C/F), feels-like (C/F), condition, wind, pressure,
          humidity, cloud, visibility, UV, gust, and related metrics

    Notes:
        - Data comes from WeatherAPI current endpoint only (no hourly/daily forecast, no alerts).
        - Units are provided by WeatherAPI
    """

    access_token = get_access_token()
    if access_token is not None:
        print(f"JWT: {access_token.token}")
    else:
        print("JWT: <none>")


    try:
        result = requests.get(
            url="http://api.weatherapi.com/v1/current.json",
            params={
                "key": os.getenv("WEATHER_API_KEY"),
                "q": city,
                "aqi": "no",
            },
            timeout=10,
        )
    # Return failure to agent if script fails and log exception locally
    except requests.RequestException as e:
        print(f"Network error fetching weather for {city}: {e}")
        return {
            "error": {
                "type": "tool_error",
                "code": "WEATHER_NETWORK_ERROR",
                "message": "Unable to reach weather provider",
            }
        }

    if result.status_code == 200:
        print("Weather data fetched successfully for city:", city)
        return result.json()

    # Return an error to the agent if the api fails with an non 200 status code
    print(f"Provider error fetching weather for {city}: {result.status_code} - {result.text}")
    return {
        "error": {
            "type": "tool_error",
            "code": "WEATHER_PROVIDER_FAILURE",
            "message": "Weather provider request failed",
        }
    }

if __name__ == "__main__":
    mcp.run("streamable-http", host="0.0.0.0", port=8080, show_banner="My Shitty MCP Server")#, auth=verifier)