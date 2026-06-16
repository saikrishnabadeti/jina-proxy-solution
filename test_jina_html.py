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


def extract_heading(html: str) -> str:
    """Extract equipment heading/title from HTML"""
    if not html:
        return "No heading found"
    
    if BS4_AVAILABLE:
        soup = BeautifulSoup(html, 'html.parser')
        # Try h1 first, then h2, then title
        for tag in ['h1', 'h2', 'title']:
            element = soup.find(tag)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
    else:
        # Simple string extraction as fallback
        import re
        # Look for <h1> or <title> tags
        patterns = [
            r'<h1[^>]*>(.*?)</h1>',
            r'<h2[^>]*>(.*?)</h2>',
            r'<title[^>]*>(.*?)</title>'
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                # Clean up HTML tags if any
                text = re.sub(r'<[^>]+>', '', match.group(1))
                return text.strip()[:100]  # Limit length
    
    return "No heading found"


def test_get_jina_html():
    """Test the get_jina_html function with examples"""
    print("="*60)
    print("TEST: get_jina_html() Function")
    print("="*60)
    
    # Test 1: Get HTML with proxy and extract heading
    print("\n[TEST 1] Get HTML with proxy rotation:")
    url = "https://www.ironplanet.com/for-sale/Bucket-Trucks-2016-Altec-AM55E-56-ft-on-2016-Freightliner-M2-106-M2106-4x2-Bucket-Truck-Florida/15293435"
    
    html = get_jina_html(url, use_proxy=True)
    
    if html:
        print(f"  SUCCESS! Got {len(html)} characters")
        heading = extract_heading(html)
        print(f"  Equipment: {heading}")
    else:
        print("  FAILED to get HTML")
    
    # Test 2: Get HTML without proxy (direct)
    print("\n[TEST 2] Get HTML without proxy (direct):")
    html_direct = get_jina_html(url, use_proxy=False)
    
    if html_direct:
        print(f"  SUCCESS! Got {len(html_direct)} characters")
        heading = extract_heading(html_direct)
        print(f"  Equipment: {heading}")
    else:
        print("  FAILED to get HTML")
    
    # Test 3: Multiple calls with proxy rotation + extract headings
    print("\n[TEST 3] Multiple calls with proxy rotation:")
    for i in range(1, 6):
        html = get_jina_html(url, use_proxy=True)
        status = "OK" if html else "FAIL"
        size = len(html) if html else 0
        heading = extract_heading(html) if html else "N/A"
        print(f"  Call {i}: {status} ({size} chars)")
        if html and i == 1:  # Show heading from first successful call
            print(f"    Equipment: {heading[:60]}...")
        time.sleep(0.5)
    
    print("\n" + "="*60)


def test_custom_url():
    """Test with user-provided URL"""
    print("\n[TEST 4] Custom URL test:")
    
    # You can change this URL
    test_url = "https://www.google.com"
    
    print(f"  Testing URL: {test_url}")
    html = get_jina_html(test_url, use_proxy=True)
    
    if html:
        print(f"  SUCCESS! Got {len(html)} characters")
        print(f"  First 100 chars: {html[:100]}...")
    else:
        print("  FAILED")


if __name__ == "__main__":
    test_get_jina_html()
    test_custom_url()
