"""
Test get_jina_html() Function
Tests the HTML extraction function with and without proxies
"""

from jina_proxy import get_jina_html, time


def test_get_jina_html():
    """Test the get_jina_html function with examples"""
    print("="*60)
    print("TEST: get_jina_html() Function")
    print("="*60)
    
    # Test 1: Get HTML with proxy
    print("\n[TEST 1] Get HTML with proxy rotation:")
    url = "https://www.ironplanet.com/for-sale/Bucket-Trucks-2016-Altec-AM55E-56-ft-on-2016-Freightliner-M2-106-M2106-4x2-Bucket-Truck-Florida/15293435"
    
    html = get_jina_html(url, use_proxy=True)
    
    if html:
        print(f"  SUCCESS! Got {len(html)} characters")
        print(f"  First 200 chars: {html[:200]}...")
    else:
        print("  FAILED to get HTML")
    
    # Test 2: Get HTML without proxy (direct)
    print("\n[TEST 2] Get HTML without proxy (direct):")
    html_direct = get_jina_html(url, use_proxy=False)
    
    if html_direct:
        print(f"  SUCCESS! Got {len(html_direct)} characters")
    else:
        print("  FAILED to get HTML")
    
    # Test 3: Multiple calls with proxy rotation
    print("\n[TEST 3] Multiple calls with proxy rotation:")
    for i in range(1, 6):
        html = get_jina_html(url, use_proxy=True)
        status = "OK" if html else "FAIL"
        size = len(html) if html else 0
        print(f"  Call {i}: {status} ({size} chars)")
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
