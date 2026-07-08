"""Internet Speed Check — download ~5 MB and report Mbps + rough latency (stdlib only)."""
import time
import urllib.request

# Some CDNs 403 the default "Python-urllib" agent — send a browser-ish UA.
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MayaSpeedCheck/1.0"}


def _get(url: str, timeout: int):
    return urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=timeout)


TEST_URL = "https://speed.cloudflare.com/__down?bytes=5000000"


def main():
    # Latency: small HEAD-ish request first
    try:
        t0 = time.monotonic()
        with _get("https://speed.cloudflare.com/__down?bytes=1", 10):
            pass
        latency_ms = (time.monotonic() - t0) * 1000
    except Exception as e:
        print(f"Internet down lagta hai — connect nahi hua: {e}")
        return

    try:
        t0 = time.monotonic()
        total = 0
        with _get(TEST_URL, 30) as r:
            while True:
                chunk = r.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
        elapsed = max(0.001, time.monotonic() - t0)
        mbps = total * 8 / elapsed / 1e6
        print("=== INTERNET SPEED CHECK ===")
        print(f"Latency (rough): {latency_ms:.0f} ms")
        print(f"Download: {mbps:.1f} Mbps ({total / 1e6:.1f} MB in {elapsed:.1f}s)")
        verdict = "Excellent" if mbps > 100 else "Good" if mbps > 25 else "OK" if mbps > 5 else "Slow"
        print(f"Verdict: {verdict}")
    except Exception as e:
        print(f"Speed test failed: {e}")


if __name__ == "__main__":
    main()
