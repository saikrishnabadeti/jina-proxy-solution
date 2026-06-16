"""
Jina AI API with Proxy Rotation
Makes requests to r.jina.ai with automatic proxy rotation to bypass rate limits.
"""

import requests
import random
import time
from typing import List, Optional, Dict


# ============================================
# CONFIGURATION - Update with your proxies
# ============================================

# Oxylabs free proxies (or add your own)
PROXIES = [
    None,  # Your direct IP (fallback)
    # Oxylabs ports 8000-8005 (6 IPs total = ~120 requests/min capacity)
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8000",
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8001",
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8002",
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8003",
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8004",
    "http://user-saiBadeti_8tHUU-country-US:7gp=5KG+CD7kHq@dc.oxylabs.io:8005",
]

# Target URL
URL = "https://r.jina.ai/https://www.ironplanet.com/for-sale/Bucket-Trucks-2016-Altec-AM55E-56-ft-on-2016-Freightliner-M2-106-M2106-4x2-Bucket-Truck-Florida/15293435"

# Headers (Host header removed - it causes 403 errors)
HEADERS = {
    "X-Return-Format": "html"
}


# ============================================
# PROXY ROTATOR
# ============================================

class ProxyRotator:
    """Rotates through proxies and tracks health"""
    
    def __init__(self, proxies: List[Optional[str]]):
        self.proxies = proxies or [None]
        self.current = 0
        self.failed = set()
    
    def get_next(self) -> Optional[str]:
        """Get next working proxy"""
        for _ in range(len(self.proxies)):
            proxy = self.proxies[self.current % len(self.proxies)]
            self.current += 1
            if proxy not in self.failed:
                return proxy
        return None
    
    def mark_failed(self, proxy: Optional[str]):
        self.failed.add(proxy)


# ============================================
# REQUEST FUNCTIONS
# ============================================

def make_request(url: str, proxy: Optional[str] = None) -> Optional[requests.Response]:
    """Make HTTP request through proxy"""
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(
            url,
            headers=HEADERS,
            proxies=proxies,
            timeout=30,
            allow_redirects=True
        )
        return response
    except Exception as e:
        print(f"    Error: {e}")
        return None


def get_jina_html(target_url: str, use_proxy: bool = True) -> Optional[str]:
    """
    Call Jina AI API and return HTML response
    
    Args:
        target_url: URL to extract HTML from (e.g., "https://example.com")
        use_proxy: Whether to use proxy rotation (default: True)
    
    Returns:
        HTML content as string, or None if failed
    
    Example:
        html = get_jina_html("https://www.ironplanet.com/for-sale/...")
        if html:
            print(html[:500])  # Print first 500 chars
    """
    # Build Jina API URL
    jina_url = f"https://r.jina.ai/{target_url}"
    
    # Get proxy if requested
    proxy = None
    if use_proxy and len(PROXIES) > 1:
        rotator = ProxyRotator(PROXIES)
        proxy = rotator.get_next()
    
    # Make request
    response = make_request(jina_url, proxy)
    
    if response and response.status_code == 200:
        return response.text
    else:
        status = response.status_code if response else "No response"
        print(f"[ERROR] Failed to get HTML. Status: {status}")
        return None


def test_with_same_ip(num_requests: int = 30) -> Dict:
    """Test with same IP (no proxy rotation)"""
    print(f"\n{'='*60}")
    print("FUNCTION 1: Same IP (No Rotation)")
    print(f"{'='*60}")
    
    results = []
    for i in range(1, num_requests + 1):
        response = make_request(URL)
        
        if response:
            status = response.status_code
            size = len(response.text)
            print(f"  [{i:2}/{num_requests}] Status: {status} | Size: {size} bytes")
            results.append({"status": status, "size": size})
        else:
            print(f"  [{i:2}/{num_requests}] Failed")
            results.append({"status": None, "size": 0})
        
        time.sleep(0.5)
    
    return summarize(results)


def test_with_rotation(num_requests: int = 30) -> Dict:
    """Test with proxy rotation"""
    print(f"\n{'='*60}")
    print("FUNCTION 2: Proxy Rotation")
    print(f"Proxies: {len(PROXIES)}")
    print(f"{'='*60}")
    
    rotator = ProxyRotator(PROXIES)
    results = []
    
    for i in range(1, num_requests + 1):
        proxy = rotator.get_next()
        proxy_name = proxy or "Direct"
        
        response = make_request(URL, proxy)
        
        if response:
            status = response.status_code
            size = len(response.text)
            print(f"  [{i:2}/{num_requests}] {proxy_name[:30]:<30} | Status: {status} | Size: {size}")
            results.append({"status": status, "size": size, "proxy": proxy})
            
            if status != 200:
                rotator.mark_failed(proxy)
        else:
            print(f"  [{i:2}/{num_requests}] {proxy_name[:30]:<30} | Failed")
            results.append({"status": None, "size": 0, "proxy": proxy})
            rotator.mark_failed(proxy)
        
        time.sleep(0.5)
    
    return summarize(results)


def summarize(results: List[Dict]) -> Dict:
    """Summarize results"""
    success = sum(1 for r in results if r.get("status") == 200)
    rate_limited = sum(1 for r in results if r.get("status") == 429)
    failed = len(results) - success - rate_limited
    
    print(f"\n  Results:")
    print(f"    Success:      {success}")
    print(f"    Rate Limited: {rate_limited}")
    print(f"    Failed:       {failed}")
    
    return {
        "success": success,
        "rate_limited": rate_limited,
        "failed": failed,
        "total": len(results)
    }


# ============================================
# TEST get_jina_html FUNCTION
# ============================================

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


# ============================================
# MAIN
# ============================================

def main():
    """Run comparison test"""
    print("="*60)
    print("JINA AI API - Proxy Rotation Test")
    print("="*60)
    print(f"URL: {URL[:50]}...")
    print(f"Proxies configured: {len(PROXIES)}")
    
    # Run both tests
    results_same = test_with_same_ip(num_requests=30)
    results_rotation = test_with_rotation(num_requests=30)
    
    # Comparison
    print(f"\n{'='*60}")
    print("COMPARISON")
    print(f"{'='*60}")
    print(f"  Same IP:       {results_same['success']}/30 success")
    print(f"  With Rotation: {results_rotation['success']}/30 success")
    
    if results_rotation['success'] > results_same['success']:
        print(f"\n  Proxy rotation is BETTER!")
    elif results_rotation['success'] == results_same['success']:
        print(f"\n  Both methods similar (rate limit not hit)")
    else:
        print(f"\n  Same IP was better (check proxy quality)")
    
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--test-html":
        test_get_jina_html()
    else:
        main()
        print("\n[Tip] Run with --test-html to test get_jina_html() function")
