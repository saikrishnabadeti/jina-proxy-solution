# Jina AI API with Proxy Rotation

Python solution for accessing Jina AI API with automatic proxy rotation to bypass rate limits.

## What This Does

- Compares API access with vs without proxy rotation
- Automatically rotates through multiple proxy IPs
- Tracks success rate and detects rate limiting
- Shows which method works better

## Quick Start

### 1. Install Requirements

```bash
pip install requests
```

Or create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
pip install requests
```

### 2. Add Your Proxies

Edit `jina_proxy.py` line 12-16:

```python
PROXIES = [
    None,  # Your direct IP (fallback)
    # Add your proxies here:
    "http://username:password@proxy:port",
]
```

**Get Free Proxies:**
- **Oxylabs** (Recommended): https://oxylabs.io - 5 free IPs, 5GB/month
- Other free lists: https://free-proxy-list.net/

### 3. Run Test

```bash
python jina_proxy.py
```

## How It Works

### Two Functions

1. **`test_with_same_ip()`** - Makes all requests from same IP
   - Good baseline test
   - Hits rate limit after ~20 requests

2. **`test_with_rotation()`** - Rotates through proxy list
   - Each request uses different IP
   - Spreads rate limit across multiple IPs
   - Higher success rate

### Rate Limit Behavior

Without proxy:
```
Request 1  → Your IP → API (count: 1)
Request 2  → Your IP → API (count: 2)
...
Request 20 → BLOCKED (429 error)
```

With proxy rotation:
```
Request 1 → Proxy IP 1 → API (IP1 count: 1)
Request 2 → Proxy IP 2 → API (IP2 count: 1)
Request 3 → Proxy IP 3 → API (IP3 count: 1)
...
Request 20→ Still OK (different IPs)
```

## Expected Output

```
============================================================
JINA AI API - Proxy Rotation Test
============================================================

============================================================
FUNCTION 1: Same IP (No Rotation)
============================================================
  [ 1/20] Status: 200 | Size: 2407 bytes
  [ 2/20] Status: 200 | Size: 2407 bytes
  ...
  [20/20] Status: 429 | Size: 292 bytes  <-- Rate limited!

  Results:
    Success:      15
    Rate Limited: 5
    Failed:       0

============================================================
FUNCTION 2: Proxy Rotation
============================================================
Proxies: 3
  [ 1/20] Direct                         | Status: 200 | Size: 2407
  [ 2/20] http://proxy1:8080             | Status: 200 | Size: 2407
  [ 3/20] http://proxy2:8080             | Status: 200 | Size: 2407
  ...

  Results:
    Success:      20
    Rate Limited: 0
    Failed:       0

============================================================
COMPARISON
============================================================
  Same IP:       15/20 success
  With Rotation: 20/20 success

  Proxy rotation is BETTER!
============================================================
```

## Free Proxy Options

### Option 1: Oxylabs (Recommended)

**Website:** https://oxylabs.io

**Free Tier:**
- 5 datacenter proxies
- 5 GB traffic per month
- No time limit (resets monthly)
- US location

**Steps:**
1. Sign up at https://oxylabs.io
2. Go to Dashboard → Datacenter Proxies
3. Create proxy user (get username/password)
4. Copy proxy endpoints (dc.oxylabs.io:8000-8005)

**Format:**
```python
PROXIES = [
    None,
    "http://user-yourname-country-US:password@dc.oxylabs.io:8000",
    "http://user-yourname-country-US:password@dc.oxylabs.io:8001",
    "http://user-yourname-country-US:password@dc.oxylabs.io:8002",
]
```

### Option 2: Free Public Proxies

**Website:** https://free-proxy-list.net/

**Warning:** 
- Often unreliable (20-50% work)
- Slow speeds
- Short lifespan
- Good for testing only

**Format:**
```python
PROXIES = [
    None,
    "http://203.192.199.146:8080",
    "http://103.105.196.99:80",
]
```

## Troubleshooting

### SSL Certificate Error

If you see:
```
SSL: CERTIFICATE_VERIFY_FAILED
```

The proxy has SSL issues. Solutions:
1. Use different proxy
2. Disable SSL verify (not recommended):
   ```python
   response = requests.get(url, proxies=proxies, verify=False)
   ```

### All Requests Fail

Check:
1. Proxy format is correct (`http://user:pass@host:port`)
2. Username/password are correct
3. Proxy is online (test with simple request first)

### Still Rate Limited

Even with proxies, you're still rate limited? Solutions:
1. Add more proxies (spread load)
2. Increase delay between requests:
   ```python
   time.sleep(2)  # Add in the loop
   ```
3. Use premium proxy service

## Understanding Rate Limits

The Jina AI API has these limits:
- ~20 requests per IP per minute
- ~100-200 requests per IP per hour

**With proxy rotation:**
- 1 proxy = 20 req/min
- 3 proxies = 60 req/min
- 5 proxies = 100 req/min

## Files

- `jina_proxy.py` - Main script
- `README.md` - This file
- `requirements.txt` - Dependencies (just `requests`)

## License

MIT - Free to use and modify.

## Support

For issues with:
- **This code** - Check comments in `jina_proxy.py`
- **Proxies** - Contact your proxy provider
- **Jina API** - Visit https://jina.ai
