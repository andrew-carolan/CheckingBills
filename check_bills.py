import pandas as pd
import json
import subprocess

CSV_FILE = "/Users/andrewcarolan/Documents/GitHub/CheckingBills/Apple Card Transactions - August 2025.csv"
MODEL = "llama3"  # or another model you have locally

# 1. Load data
df = pd.read_csv(CSV_FILE)

# Optional: quick duplicate check by Pandas before asking LLM
duplicate_rows = df[df.duplicated()]
if not duplicate_rows.empty:
    print("Exact duplicate rows found:\n", duplicate_rows, "\n")

# 2. Prepare a prompt for the LLM
sample = df.head(50).to_dict(orient="records")  # send only a slice if big
prompt = f"""
You are a financial fraud detection assistant.
Given this list of Apple Card transactions in JSON:
{json.dumps(sample, indent=2)}
List any transactions that look:
  - duplicated (even if not byte-for-byte identical),
  - suspicious (unusual merchants, odd amounts, etc.).
Explain briefly why.
Return a JSON list of the suspicious items with a short reason.
"""

# 3. Call Ollama locally
result = subprocess.run(
    ["ollama", "run", MODEL],
    input=prompt.encode("utf-8"),
    capture_output=True
)

print("---- LLM analysis ----")
print(result.stdout.decode("utf-8"))
