
import yfinance as yf

symbols = ["4456.KL", "5323.KL", "8524.KL"]

for symbol in symbols:
    print(f"\nChecking {symbol}")

    try:
        data = yf.Ticker(symbol).history(period="5d")

        if data.empty:
            print("NO DATA")
            continue

        last = data.iloc[-1]
        print("Date:", data.index[-1])
        print("Close:", last["Close"])
        print("Volume:", last["Volume"])
        print("PASS")

    except Exception as e:
        print("ERROR:", str(e))
