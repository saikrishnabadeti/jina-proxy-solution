"""
Test Proxy Rotation Performance
Compares same IP vs proxy rotation success rates
"""

from jina_proxy import make_request, PROXIES, ProxyRotator, URL, summarize, Dict, List, Optional
import time


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


def main():
    """Run comparison test"""
    print("="*60)
    print("JINA AI API - Proxy Rotation Performance Test")
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
    main()
