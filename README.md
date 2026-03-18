# # Python Basic as Hell MCP Server

This is a really basic MCP server that exposes a simple tool that gets a weather from [weatherapi.com](https://www.weatherapi.com/). It uses the [FastMCP framework](https://gofastmcp.com/getting-started/welcome) to create the MCP server.

Given I'm lazy, I created this README largely with AI. So complain to Anthropic if you don't like it.

## Features

- MCP server over `streamable-http`
- Tool: `get_weather(city: str)`
- Uses `WEATHER_API_KEY` from environment variables

## Project Structure

- `src/server.py` — MCP server and weather tool
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container build config

## Requirements

- Python 3.11+ (or Docker)
- WeatherAPI key: https://www.weatherapi.com/

## Local Setup

1. Create and activate a virtual environment
2. Install dependencies
3. Add env var
4. Run server

### Example

````bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export WEATHER_API_KEY="your_api_key_here"
python server.py
````

## Docker Setup

1. Build the Docker container from the Dockerfile
2. Spin up a container from the image

````bash
docker buildx build --platform linux/amd64 -t weather-mcp:latest .
docker run --rm -p 8080:8080 -e WEATHER_API_KEY=YOUR_WEATHER_API_KEY weather-mcp
````

