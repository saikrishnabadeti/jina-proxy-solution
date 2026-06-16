"""
Test get_jina_html() Function
Tests the HTML extraction function with and without proxies
"""

from jina_proxy import get_jina_html, time
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("[WARNING] BeautifulSoup not installed. Run: pip install beautifulsoup4")


def extract_body_text(html: str, max_words: int = 100) -> str:
    """Extract first N words of text from HTML body"""
    if not html:
        return "No content found"
    
    text = ""
    
    if BS4_AVAILABLE:
        soup = BeautifulSoup(html, 'html.parser')
        # Get text from body or entire document
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
    else:
        # Simple fallback - remove all HTML tags
        import re
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
    
    # Clean up: remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    # Get first N words
    words = text.split()
    first_n_words = words[:max_words]
    
    result = ' '.join(first_n_words)
    if len(words) > max_words:
        result += "..."
    
    return result if result else "No text content"


def test_get_jina_html():
    """Test the get_jina_html function with examples"""
    print("="*60)
    print("TEST: get_jina_html() Function")
    print("="*60)
    
    # Test 1: Get HTML (direct connection)
    print("\n[TEST 1] Get HTML (direct):")
    url = "https://www.ironplanet.com/for-sale/Bucket-Trucks-2016-Altec-AM55E-56-ft-on-2016-Freightliner-M2-106-M2106-4x2-Bucket-Truck-Florida/15293435"
    
    html = get_jina_html(url)
    
    if html:
        print(f"  SUCCESS! Got {len(html)} characters")
        body_text = extract_body_text(html, max_words=100)
        print(f"  First 100 words: {body_text}")
    else:
        print("  FAILED to get HTML")
    
    # Test 2: Multiple calls (direct)
    print("\n[TEST 2] Multiple calls (direct):")
    for i in range(1, 6):
        html = get_jina_html(url)
        status = "OK" if html else "FAIL"
        size = len(html) if html else 0
        body_text = extract_body_text(html, max_words=50) if html else "N/A"
        print(f"  Call {i}: {status} ({size} chars)")
        if html and i == 1:  # Show first 50 words from first successful call
            print(f"    Preview: {body_text[:80]}...")
        time.sleep(0.5)
    
    print("\n" + "="*60)


def test_custom_url():
    """Test with user-provided URL"""
    print("\n[TEST 3] Custom URL test:")
    
    # You can change this URL
    test_url = "https://www.google.com"
    
    print(f"  Testing URL: {test_url}")
    html = get_jina_html(test_url)
    
    if html:
        print(f"  SUCCESS! Got {len(html)} characters")
        body_text = extract_body_text(html, max_words=50)
        print(f"  First 50 words: {body_text}")
    else:
        print("  FAILED")


if __name__ == "__main__":
    test_get_jina_html()
    test_custom_url()
