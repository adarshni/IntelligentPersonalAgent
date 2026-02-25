"""
Agent Tools Module.
Contains all the tools that the LangChain agent can use.
"""

import logging
from datetime import datetime
from typing import List
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

# Configure logging
logger = logging.getLogger(__name__)


@tool
def calculate_sum(numbers: List[float]) -> str:
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: A list of numbers to sum up.
    
    Returns:
        The sum of all numbers as a formatted string.
    """
    logger.info(f"Tool: calculate_sum | Input: {numbers}")
    try:
        total = sum(numbers)
        result = f"The sum of {numbers} is {total}"
        logger.info(f"Tool: calculate_sum | Output: {result}")
        return result
    except Exception as e:
        error_msg = f"Error calculating sum: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using hardcoded exchange rates.
    
    Supported conversions:
    - USD to INR (rate: 83)
    - EUR to INR (rate: 90)
    - USD to EUR (rate: 0.92)
    - And reverse conversions
    
    Args:
        amount: The amount to convert.
        from_currency: Source currency code (USD, EUR, INR).
        to_currency: Target currency code (USD, EUR, INR).
    
    Returns:
        The converted amount as a formatted string.
    """
    logger.info(f"Tool: convert_currency | Input: {amount} {from_currency} to {to_currency}")
    
    # Hardcoded exchange rates
    rates = {
        ("USD", "INR"): 83.0,
        ("EUR", "INR"): 90.0,
        ("USD", "EUR"): 0.92,
        ("INR", "USD"): 1 / 83.0,
        ("INR", "EUR"): 1 / 90.0,
        ("EUR", "USD"): 1 / 0.92,
    }
    
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    # Same currency
    if from_currency == to_currency:
        result = f"{amount} {from_currency} = {amount} {to_currency}"
        logger.info(f"Tool: convert_currency | Output: {result}")
        return result
    
    # Get conversion rate
    rate_key = (from_currency, to_currency)
    if rate_key in rates:
        converted = amount * rates[rate_key]
        result = f"{amount} {from_currency} = {converted:.2f} {to_currency}"
        logger.info(f"Tool: convert_currency | Output: {result}")
        return result
    else:
        error_msg = f"Conversion from {from_currency} to {to_currency} is not supported. Supported: USD, EUR, INR"
        logger.warning(error_msg)
        return error_msg


@tool
def get_current_date() -> str:
    """
    Get the current date and time.
    
    Returns:
        Current date and time in a readable format.
    """
    logger.info("Tool: get_current_date | Called")
    now = datetime.now()
    result = now.strftime("%A, %B %d, %Y at %I:%M %p")
    logger.info(f"Tool: get_current_date | Output: {result}")
    return f"Current date and time: {result}"


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a city (mock data).
    
    Supported cities: Bangalore, Berlin, New York
    
    Args:
        city: The name of the city to get weather for.
    
    Returns:
        Weather information for the specified city.
    """
    logger.info(f"Tool: get_weather | Input: {city}")
    
    # Mock weather data
    weather_data = {
        "bangalore": {"temp": 28, "condition": "Partly Cloudy", "humidity": 65},
        "berlin": {"temp": 10, "condition": "Cloudy", "humidity": 75},
        "new york": {"temp": 15, "condition": "Sunny", "humidity": 55},
    }
    
    city_lower = city.lower()
    
    if city_lower in weather_data:
        data = weather_data[city_lower]
        result = f"Weather in {city}: {data['temp']}°C, {data['condition']}, Humidity: {data['humidity']}%"
        logger.info(f"Tool: get_weather | Output: {result}")
        return result
    else:
        available = ", ".join(weather_data.keys())
        result = f"Weather data not available for {city}. Available cities: {available}"
        logger.info(f"Tool: get_weather | Output: {result}")
        return result


@tool
def search_web(query: str) -> str:
    """
    Search the web using DuckDuckGo and return top 3 results.
    
    Args:
        query: The search query string.
    
    Returns:
        Top 3 search results with titles and snippets.
    """
    logger.info(f"Tool: search_web | Input: {query}")
    
    try:
        # DuckDuckGo HTML endpoint
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.post(url, data={"q": query}, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find search results
        results = []
        result_divs = soup.find_all("div", class_="result")[:3]
        
        for div in result_divs:
            title_elem = div.find("a", class_="result__a")
            snippet_elem = div.find("a", class_="result__snippet")
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else "No description"
                results.append(f"**{title}**: {snippet}")
        
        if results:
            combined = "\n\n".join(results)
            result = f"Search results for '{query}':\n\n{combined}"
        else:
            result = f"No search results found for '{query}'"
        
        logger.info(f"Tool: search_web | Found {len(results)} results")
        return result
        
    except requests.RequestException as e:
        error_msg = f"Error searching web: {str(e)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error during web search: {str(e)}"
        logger.error(error_msg)
        return error_msg


# Export all tools as a list for the agent
ALL_TOOLS = [
    calculate_sum,
    convert_currency,
    get_current_date,
    get_weather,
    search_web,
]
