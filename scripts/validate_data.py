#!/usr/bin/env python3
"""Fail closed on structurally invalid research snapshots; warn on stale or unverifiable evidence."""
import json,sys,datetime,math
from pathlib import Path
p=Path("dashboard-data.json")
data=json.loads(p.read_text(encoding="utf-8"))
required=["00_總覽","01_CSP資本支出","02_終端AI","03_硬體供應","04_交叉驗證","05_警示規則","06_資料來源","07_週次歷史","08_方法與說明","09_推論需求","10_CSP容量預測","11_資料中心逐案","12_延期取消事件","13_一致性檢查"]
assert isinstance(data.get("sheets"),dict), "sheets must be an object"
assert all(isinstance(data["sheets"].get(k),list) and data["sheets"][k] for k in required),"14 sheets required"
d=datetime.date.fromisoformat(data["asOf"])
assert d<=datetime.date.today(),"Snapshot date cannot be in future"
assert isinstance(data.get("version"),str) and data["version"].strip(),"version required"
for name,rows in data["sheets"].items():
    for idx,row in enumerate(rows):
        assert isinstance(row,list),f"{name} row {idx} must be an array"
        for val in row:
            assert val is None or isinstance(val,(str,int,float,bool)),f"{name} invalid scalar"
            assert not isinstance(val,float) or math.isfinite(val),f"{name} nonfinite number"
age=(datetime.date.today()-d).days
if age>10: print(f"::warning::Published data is {age} days old (asOf={d}); scheduling does not imply fresh research")
print(f"Validated {len(required)} sheets, version={data['version']}, date={d}, age={age}d")
print("ATTENTION: structural validation does NOT independently verify claims, source credibility, or latest market values.")
