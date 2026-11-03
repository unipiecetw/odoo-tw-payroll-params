#!/usr/bin/env python3
"""Validate tw_payroll_params.json and sign it with an Ed25519 key.

  python3 tools/sign.py keygen                 -> private.key (KEEP SECRET) + prints the public key
  python3 tools/sign.py check  tw_payroll_params.json
  python3 tools/sign.py sign   tw_payroll_params.json private.key   -> tw_payroll_params.json.sig
Needs: pip install cryptography
"""
import base64
import json
import re
import sys
from datetime import date

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

LIMITS = {
    "nhi_supplement_rate": (0, 10), "nhi_basic_wage": (0, 100000),
    "nhi_supplement_cap": (0, 1e9), "nhi_general_rate": (0, 15),
    "nhi_employee_share": (0, 100), "nhi_max_dependents": (0, 10),
}


def check(path):
    data = json.load(open(path, encoding="utf-8"))
    assert data.get("schema_version") == 1, "schema_version must be 1"
    seen = set()
    for i, e in enumerate(data["parameters"], 1):
        code = e["code"]
        assert code in LIMITS, f"#{i} unknown code {code}"
        d = date.fromisoformat(e["effective_date"])
        assert (code, d) not in seen, f"#{i} duplicate"
        seen.add((code, d))
        v = e["value"]
        assert not isinstance(v, bool) and LIMITS[code][0] <= v <= LIMITS[code][1], f"#{i} value out of range"
        assert len(e.get("note", "")) <= 200, f"#{i} note too long"
    print("OK:", len(seen), "parameters")


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "keygen":
        key = Ed25519PrivateKey.generate()
        raw = key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
        open("private.key", "w").write(base64.b64encode(raw).decode())
        pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        print("Public key (put in Odoo):", base64.b64encode(pub).decode())
    elif len(sys.argv) == 3 and sys.argv[1] == "check":
        check(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == "sign":
        check(sys.argv[2])
        key = Ed25519PrivateKey.from_private_bytes(base64.b64decode(open(sys.argv[3]).read().strip()))
        sig = key.sign(open(sys.argv[2], "rb").read())
        open(sys.argv[2] + ".sig", "w").write(base64.b64encode(sig).decode())
        print("wrote", sys.argv[2] + ".sig")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
