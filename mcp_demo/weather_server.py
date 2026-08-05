from fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(city: str) -> str:
    return f"It's always sunny in {city}! ☀️"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)