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


@tool
def calculate_tip(bill_amount: float, tip_percentage: float, split_between: int = 1) -> str:
    """
    Calculate tip amount and total bill, optionally split between people.
    
    Args:
        bill_amount: The total bill amount before tip.
        tip_percentage: Tip percentage (e.g., 15, 18, 20).
        split_between: Number of people to split the bill (default: 1).
    
    Returns:
        Breakdown of tip, total, and per-person amount.
    """
    logger.info(f"Tool: calculate_tip | Input: ${bill_amount}, {tip_percentage}%, split {split_between} ways")
    
    try:
        if bill_amount < 0 or tip_percentage < 0 or split_between < 1:
            return "Invalid input: amounts must be positive and split must be at least 1"
        
        tip_amount = bill_amount * (tip_percentage / 100)
        total = bill_amount + tip_amount
        per_person = total / split_between
        
        result = f"""💰 Tip Calculator:
• Bill Amount: ${bill_amount:.2f}
• Tip ({tip_percentage}%): ${tip_amount:.2f}
• Total: ${total:.2f}"""
        
        if split_between > 1:
            result += f"\n• Split {split_between} ways: ${per_person:.2f} per person"
        
        logger.info(f"Tool: calculate_tip | Output: Total ${total:.2f}")
        return result
    except Exception as e:
        error_msg = f"Error calculating tip: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between common units of measurement.
    
    Supported conversions:
    - Length: km ↔ miles, m ↔ feet, cm ↔ inches
    - Weight: kg ↔ lbs, g ↔ oz
    - Temperature: celsius ↔ fahrenheit
    
    Args:
        value: The numeric value to convert.
        from_unit: Source unit (km, miles, m, feet, cm, inches, kg, lbs, g, oz, celsius, fahrenheit).
        to_unit: Target unit.
    
    Returns:
        The converted value with units.
    """
    logger.info(f"Tool: convert_units | Input: {value} {from_unit} to {to_unit}")
    
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()
    
    # Conversion factors
    conversions = {
        # Length
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("m", "feet"): lambda x: x * 3.28084,
        ("feet", "m"): lambda x: x * 0.3048,
        ("cm", "inches"): lambda x: x * 0.393701,
        ("inches", "cm"): lambda x: x * 2.54,
        # Weight
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x * 0.453592,
        ("g", "oz"): lambda x: x * 0.035274,
        ("oz", "g"): lambda x: x * 28.3495,
        # Temperature
        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("c", "f"): lambda x: (x * 9/5) + 32,
        ("f", "c"): lambda x: (x - 32) * 5/9,
    }
    
    key = (from_unit, to_unit)
    
    if from_unit == to_unit:
        return f"{value} {from_unit} = {value} {to_unit}"
    
    if key in conversions:
        result_value = conversions[key](value)
        result = f"📏 {value} {from_unit} = {result_value:.2f} {to_unit}"
        logger.info(f"Tool: convert_units | Output: {result}")
        return result
    else:
        available = "km↔miles, m↔feet, cm↔inches, kg↔lbs, g↔oz, celsius↔fahrenheit"
        return f"Conversion from {from_unit} to {to_unit} not supported. Available: {available}"


@tool
def get_random_quote() -> str:
    """
    Get a random inspirational or motivational quote.
    
    Returns:
        A random quote with its author.
    """
    logger.info("Tool: get_random_quote | Called")
    
    import random
    
    quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
        ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
        ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
        ("The only impossible journey is the one you never begin.", "Tony Robbins"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("The secret of getting ahead is getting started.", "Mark Twain"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
        ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
        ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
        ("Act as if what you do makes a difference. It does.", "William James"),
    ]
    
    quote, author = random.choice(quotes)
    result = f'✨ "{quote}"\n   — {author}'
    logger.info(f"Tool: get_random_quote | Output: Quote by {author}")
    return result


@tool
def analyze_text(text: str) -> str:
    """
    Analyze text and provide statistics like word count, character count, etc.
    
    Args:
        text: The text to analyze.
    
    Returns:
        Text statistics including word count, character count, sentence count, etc.
    """
    logger.info(f"Tool: analyze_text | Input: {len(text)} chars")
    
    try:
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_no_spaces = len(text.replace(" ", ""))
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        paragraph_count = text.count('\n\n') + 1 if text.strip() else 0
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Reading time (average 200 words per minute)
        reading_time_mins = word_count / 200
        
        result = f"""📝 Text Analysis:
• Words: {word_count}
• Characters (with spaces): {char_count}
• Characters (no spaces): {char_no_spaces}
• Sentences: {sentence_count}
• Paragraphs: {paragraph_count}
• Average word length: {avg_word_length:.1f} characters
• Estimated reading time: {reading_time_mins:.1f} minutes"""
        
        logger.info(f"Tool: analyze_text | Output: {word_count} words")
        return result
    except Exception as e:
        error_msg = f"Error analyzing text: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """
    Calculate Body Mass Index (BMI) and provide health category.
    
    Args:
        weight_kg: Weight in kilograms.
        height_cm: Height in centimeters.
    
    Returns:
        BMI value and health category.
    """
    logger.info(f"Tool: calculate_bmi | Input: {weight_kg}kg, {height_cm}cm")
    
    try:
        if weight_kg <= 0 or height_cm <= 0:
            return "Invalid input: weight and height must be positive numbers"
        
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        # Determine category
        if bmi < 18.5:
            category = "Underweight"
            emoji = "⚠️"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            emoji = "✅"
        elif 25 <= bmi < 30:
            category = "Overweight"
            emoji = "⚠️"
        else:
            category = "Obese"
            emoji = "🔴"
        
        result = f"""🏃 BMI Calculator:
• Weight: {weight_kg} kg
• Height: {height_cm} cm ({height_m:.2f} m)
• BMI: {bmi:.1f}
• Category: {emoji} {category}

BMI Categories:
• Underweight: < 18.5
• Normal: 18.5 - 24.9
• Overweight: 25 - 29.9
• Obese: ≥ 30"""
        
        logger.info(f"Tool: calculate_bmi | Output: BMI {bmi:.1f}")
        return result
    except Exception as e:
        error_msg = f"Error calculating BMI: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def calculate_age(birth_date: str) -> str:
    """
    Calculate age from a birth date.
    
    Args:
        birth_date: Birth date in format YYYY-MM-DD (e.g., 1990-05-15).
    
    Returns:
        Age in years, months, and days, plus days until next birthday.
    """
    logger.info(f"Tool: calculate_age | Input: {birth_date}")
    
    try:
        from datetime import datetime
        
        birth = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.now()
        
        if birth > today:
            return "Birth date cannot be in the future!"
        
        # Calculate age
        years = today.year - birth.year
        months = today.month - birth.month
        days = today.day - birth.day
        
        if days < 0:
            months -= 1
            # Get days in previous month
            prev_month = today.month - 1 if today.month > 1 else 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - datetime(prev_year, prev_month, 1)).days if prev_month < 12 else 31
            days += days_in_prev_month
        
        if months < 0:
            years -= 1
            months += 12
        
        # Days until next birthday
        next_birthday = datetime(today.year, birth.month, birth.day) if datetime(today.year, birth.month, birth.day) > today else datetime(today.year + 1, birth.month, birth.day)
        days_until_birthday = (next_birthday - today).days
        
        # Total days lived
        total_days = (today - birth).days
        
        result = f"""🎂 Age Calculator:
• Birth Date: {birth.strftime('%B %d, %Y')}
• Age: {years} years, {months} months, {days} days
• Total days lived: {total_days:,} days
• Days until next birthday: {days_until_birthday} days"""
        
        logger.info(f"Tool: calculate_age | Output: {years} years old")
        return result
    except ValueError:
        return "Invalid date format! Please use YYYY-MM-DD (e.g., 1990-05-15)"
    except Exception as e:
        error_msg = f"Error calculating age: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def generate_password(length: int = 16, include_special: bool = True) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Password length (8-50 characters, default 16).
        include_special: Whether to include special characters (default True).
    
    Returns:
        A randomly generated secure password.
    """
    logger.info(f"Tool: generate_password | Input: length={length}, special={include_special}")
    
    import random
    import string
    
    try:
        if length < 8:
            length = 8
        elif length > 50:
            length = 50
        
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_special else ""
        
        all_chars = lowercase + uppercase + digits + special
        
        # Ensure at least one of each type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
        ]
        
        if include_special:
            password.append(random.choice(special))
        
        # Fill remaining length
        remaining = length - len(password)
        password.extend(random.choice(all_chars) for _ in range(remaining))
        
        # Shuffle
        random.shuffle(password)
        password_str = ''.join(password)
        
        result = f"""🔐 Password Generator:
• Length: {length} characters
• Special characters: {'Yes' if include_special else 'No'}
• Generated password: {password_str}

⚠️ Store this password securely!"""
        
        logger.info(f"Tool: generate_password | Output: Generated {length}-char password")
        return result
    except Exception as e:
        error_msg = f"Error generating password: {str(e)}"
        logger.error(error_msg)
        return error_msg


@tool
def calculate_percentage(value: float, percentage: float, operation: str = "of") -> str:
    """
    Calculate percentages - find percentage of a number, or what percentage one number is of another.
    
    Args:
        value: The main number.
        percentage: The percentage or second number.
        operation: "of" to find percentage of value, "is" to find what % value is of percentage.
    
    Returns:
        The calculated result.
    """
    logger.info(f"Tool: calculate_percentage | Input: {value}, {percentage}, {operation}")
    
    try:
        operation = operation.lower().strip()
        
        if operation == "of":
            # What is X% of Y?
            result_value = (percentage / 100) * value
            result = f"📊 {percentage}% of {value} = {result_value:.2f}"
        elif operation == "is":
            # X is what % of Y?
            if percentage == 0:
                return "Cannot calculate: division by zero"
            result_value = (value / percentage) * 100
            result = f"📊 {value} is {result_value:.2f}% of {percentage}"
        elif operation == "change":
            # Percentage change from value to percentage
            if value == 0:
                return "Cannot calculate percentage change from zero"
            change = ((percentage - value) / value) * 100
            direction = "increase" if change > 0 else "decrease"
            result = f"📊 Change from {value} to {percentage} = {abs(change):.2f}% {direction}"
        else:
            result = f"Unknown operation '{operation}'. Use 'of', 'is', or 'change'"
        
        logger.info(f"Tool: calculate_percentage | Output: {result}")
        return result
    except Exception as e:
        error_msg = f"Error calculating percentage: {str(e)}"
        logger.error(error_msg)
        return error_msg


# Export all tools as a list for the agent
ALL_TOOLS = [
    calculate_sum,
    convert_currency,
    get_current_date,
    get_weather,
    search_web,
    calculate_tip,
    convert_units,
    get_random_quote,
    analyze_text,
    calculate_bmi,
    calculate_age,
    generate_password,
    calculate_percentage,
]
