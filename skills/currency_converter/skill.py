"""Currency Converter — live rates via open.er-api.com (free, no key).

stdin: "<amount> <FROM> <TO>" e.g. "100 USD INR". Default: "1 USD INR".
"""
import json
import sys
import urllib.request


def main():
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    amount, src, dst = 1.0, "USD", "INR"
    parts = raw.split()
    if len(parts) >= 3:
        try:
            amount = float(parts[0])
            src, dst = parts[1].upper(), parts[2].upper()
        except ValueError:
            pass

    url = f"https://open.er-api.com/v6/latest/{src}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
    except Exception as e:
        print(f"Rate fetch failed (internet check karo): {e}")
        return

    rates = data.get("rates") or {}
    if dst not in rates:
        print(f"Currency '{dst}' not found. Common: USD, INR, EUR, GBP, AED, JPY")
        return
    rate = float(rates[dst])
    print(f"{amount:g} {src} = {amount * rate:,.2f} {dst}")
    print(f"Rate: 1 {src} = {rate:,.4f} {dst} (source: open.er-api.com, {data.get('time_last_update_utc', 'n/a')})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Currency converter error: {e}")
