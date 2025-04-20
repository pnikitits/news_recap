import requests
from bs4 import BeautifulSoup
import re


def analyze_and_fetch_bbc_headlines():
    """
    Analyze the BBC News website structure and fetch top headlines.
    This script adapts to changes in the website's HTML structure.
    """
    url = "https://www.bbc.com/news"
    
    try:
        # Add user-agent header to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Make the request
        print(f"Fetching BBC News website...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("Analyzing website structure to locate headlines...")
        
        # Try multiple strategies to find headline elements
        headline_candidates = []
        headline_elements = []
        
        # Strategy 1: Common heading elements with substantial text
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            text = heading.get_text().strip()
            if len(text) > 20 and len(text) < 150:  # Likely headline length
                headline_candidates.append({
                    'element': heading,
                    'text': text,
                    'strategy': 'heading',
                    'tag': heading.name,
                    'class': str(heading.get('class', []))
                })
        
        # Strategy 2: Look for anchor tags with substantial text
        anchors = soup.find_all('a')
        for anchor in anchors:
            text = anchor.get_text().strip()
            if len(text) > 20 and len(text) < 150:  # Likely headline length
                # Avoid navigation links with "BBC" or typical menu items
                if not re.search(r'(BBC|Home|News|Sport|Weather|iPlayer|Sounds|Account|Search)', text):
                    headline_candidates.append({
                        'element': anchor,
                        'text': text,
                        'strategy': 'anchor',
                        'tag': anchor.name,
                        'class': str(anchor.get('class', []))
                    })
        
        # Strategy 3: Look for elements with classes containing typical headline-related terms
        headline_elements = soup.find_all(class_=re.compile(r'(headline|title|heading|promo)', re.IGNORECASE))
        for element in headline_elements:
            text = element.get_text().strip()
            if len(text) > 20 and len(text) < 150:
                headline_candidates.append({
                    'element': element,
                    'text': text,
                    'strategy': 'class',
                    'tag': element.name,
                    'class': str(element.get('class', []))
                })
        
        # Find common patterns in headline candidates
        if headline_candidates:
            # Group by tag and class pattern to identify the most common pattern
            patterns = {}
            for candidate in headline_candidates:
                key = f"{candidate['tag']}:{candidate['class']}"
                if key not in patterns:
                    patterns[key] = []
                patterns[key].append(candidate)
            
            # Find the pattern with the most candidates (likely the headline pattern)
            most_common_pattern = max(patterns.items(), key=lambda x: len(x[1]))
            pattern_key, pattern_candidates = most_common_pattern
            
            print(f"Identified likely headline pattern: {pattern_key} with {len(pattern_candidates)} matches")
            
            # Extract tag and class from the pattern key
            tag, class_str = pattern_key.split(':')
            
            # Use the identified pattern to extract headlines
            if '[' in class_str and ']' not in class_str:  # Handle malformed class string
                class_str += ']'
            
            try:
                class_list = eval(class_str) if class_str and class_str != '[]' else None
                if isinstance(class_list, list):
                    headlines = soup.find_all(tag, class_=class_list)
                else:
                    headlines = soup.find_all(tag, class_=lambda c: c and any(cls in str(c) for cls in class_list) if class_list else True)
            except Exception:
                # If there's an issue with class parsing, just use the tag
                headlines = soup.find_all(tag)
                # Filter to likely headlines by text length
                headlines = [h for h in headlines if 20 < len(h.get_text().strip()) < 150]
            
            # If still no headlines found, use the candidates directly
            if not headlines:
                headlines = [candidate['element'] for candidate in pattern_candidates]
        else:
            # Fallback: just try to find anything that looks like a headline
            headlines = [h for h in soup.find_all(['h1', 'h2', 'h3']) if 20 < len(h.get_text().strip()) < 150]
        
        # Filter out duplicates
        unique_headline_texts = set()
        filtered_headlines = []
        for headline in headlines:
            text = headline.get_text().strip()
            if text and text not in unique_headline_texts:
                unique_headline_texts.add(text)
                filtered_headlines.append(headline)
        
        headlines = filtered_headlines[:15]  # Limit to top 15 headlines
        
        if not headlines:
            print("No headlines found. The website structure may be significantly different.")
            return

            
        return headlines
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the BBC News website: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
