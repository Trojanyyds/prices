import os
import requests

UA = {"User-Agent": "Mozilla/5.0"}


def btc_price():
    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": "bitcoin", "vs_currencies": "usd"},
        headers=UA,
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["bitcoin"]["usd"]


def qqqm_price():
    r = requests.get(
        "https://query1.finance.yahoo.com/v8/finance/chart/QQQM",
        headers=UA,
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]


def main():
    lines = []
    for label, fn, fmt in [("BTC", btc_price, "${:,.0f}"), ("QQQM", qqqm_price, "${:,.2f}")]:
        try:
            lines.append(f"{label}: {fmt.format(fn())}")
        except Exception as e:
            lines.append(f"{label}: unavailable ({type(e).__name__})")
    message = "\n".join(lines)
    print(message)

    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        print("(NTFY_TOPIC not set - not sending)")
        return
    requests.post(
        f"https://ntfy.sh/{topic}",
        data=message.encode("utf-8"),
        headers={"Title": "Daily prices"},
        timeout=15,
    ).raise_for_status()


if __name__ == "__main__":
    main()
