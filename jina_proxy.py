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


def get_jina_html(target_url: str) -> Optional[str]:
    """
    Call Jina AI API and return HTML response (direct connection)
    
    Args:
        target_url: URL to extract HTML from (e.g., "https://example.com")
    
    Returns:
        HTML content as string, or None if failed
    
    Example:
        html = get_jina_html("https://www.ironplanet.com/for-sale/...")
        if html:
            print(html[:500])  # Print first 500 chars
    """
    # Build Jina API URL
    jina_url = f"https://r.jina.ai/{target_url}"
    
    # Make direct request (no proxy)
    response = make_request(jina_url, proxy=None)
    
    if response and response.status_code == 200:
        return response.text
    else:
        status = response.status_code if response else "No response"
        print(f"[ERROR] Failed to get HTML. Status: {status}")
        return None


# ============================================
# MAIN (for backward compatibility)
# ============================================

if __name__ == "__main__":
    print("="*60)
    print("JINA AI API - Proxy Rotation Module")
    print("="*60)
    print("\nThis is a module. Import it in your code:")
    print('  from jina_proxy import get_jina_html, ProxyRotator')
    print("\nOr run the test files:")
    print('  python test_performance.py')
    print('  python test_jina_html.py')
    print("="*60)
