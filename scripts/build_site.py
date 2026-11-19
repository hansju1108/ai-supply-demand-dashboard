#!/usr/bin/env python3
"""Build the downloadable single-file dashboard from the validated JSON snapshot."""
import json
from pathlib import Path
data=json.loads(Path("dashboard-data.json").read_text(encoding="utf-8"))
template=Path("index.template.html").read_text(encoding="utf-8")
marker="__DASHBOARD_JSON__"
assert template.count(marker)==1,"Expected exactly one data insertion marker"
payload=json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
html=template.replace(marker,payload)
assert "id=\"seed-data\"" in html
Path("index.html").write_text(html,encoding="utf-8")
Path("public").mkdir(exist_ok=True)
Path("public/index.html").write_text(html,encoding="utf-8")
Path("public/dashboard-data.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Built public site: {data['version']} / {data['asOf']}")
