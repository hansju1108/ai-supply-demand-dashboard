#!/usr/bin/env python3
"""Validate embedded JS syntax via Node without executing any website data."""
import re,subprocess,sys,tempfile
from pathlib import Path
html=Path("public/index.html").read_text(encoding="utf-8")
assert "function pageMonetization()" in html, "Missing monetization page"
assert "function pageFinancing()" in html, "Missing financing page"
assert "function pageLogic()" in html, "Missing four-layer audit"
scripts=re.findall(r"<script([^>]*)>([\s\S]*?)</script>",html,re.I)
js=[body for attrs,body in scripts if 'application/json' not in attrs.lower()]
assert len(js)==1, f"Expected one executable JS script, got {len(js)}"
with tempfile.NamedTemporaryFile("w",suffix=".js",encoding="utf-8",delete=False) as f:
    f.write(js[0]);name=f.name
p=subprocess.run(["node","--check",name],capture_output=True,text=True)
if p.returncode:
    print(p.stderr,file=sys.stderr)
    raise SystemExit(p.returncode)
print("Embedded site JavaScript syntax passed.")
