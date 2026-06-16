# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python Dependencies

```bash
pip install requests
```

### Step 2: Get Free Proxies (Oxylabs)

1. Go to https://oxylabs.io
2. Sign up with email
3. Click "Create proxy user" in dashboard
4. Note down:
   - Username: `user-yourname-country-US`
   - Password: (shown once, copy it!)

### Step 3: Edit jina_proxy.py

Open `jina_proxy.py` and update lines 17-23:

```python
PROXIES = [
    None,  # Your direct IP
    "http://user-YOURNAME-country-US:YOURPASSWORD@dc.oxylabs.io:8000",
    "http://user-YOURNAME-country-US:YOURPASSWORD@dc.oxylabs.io:8001",
    "http://user-YOURNAME-country-US:YOURPASSWORD@dc.oxylabs.io:8002",
]
```

Replace `YOURNAME` and `YOURPASSWORD` with your actual credentials.

### Step 4: Run Test

```bash
python jina_proxy.py
```

### Expected Output

```
============================================================
JINA AI API - Proxy Rotation Test
============================================================

============================================================
FUNCTION 1: Same IP (No Rotation)
============================================================
  [ 1/20] Status: 200 | Size: 2407 bytes
  ...
  Results:
    Success:      15
    Rate Limited: 5

============================================================
FUNCTION 2: Proxy Rotation
============================================================
  [ 1/20] Direct                         | Status: 200
  [ 2/20] http://proxy1:8080             | Status: 200
  ...
  Results:
    Success:      20
    Rate Limited: 0

  Proxy rotation is BETTER!
```

## That's It!

If you see `Proxy rotation is BETTER!` - it's working!

## Common Issues

### "Proxy failed" errors?

- Check your username/password are correct
- Make sure you copied the full proxy URL
- Try using just one proxy first

### Still rate limited?

- Add more proxies (up to 5 with Oxylabs free)
- Increase delay between requests (change `time.sleep(0.5)` to `time.sleep(2)`)

### SSL errors?

- Try different proxy port (8001 instead of 8000)
- Some proxies have SSL issues - use another

## Next Steps

- Share with your team
- Add more proxies for higher throughput
- Integrate into your main project
- Read full README.md for details
