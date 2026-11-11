#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""

import json

total = 0.0
count = 0
transactions = {}

with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
            txn_id = event.get("txn_id")

            if txn_id:
                if txn_id not in transactions or event["ts"] > transactions[txn_id]["ts"]:
                    transactions[txn_id] = event
                    total += float(event["amount"])

        except Exception as e:
            print(f"Skipping malformed line: {e}")
            continue

for event in transactions.values():
    if event["status"] == "success":
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
