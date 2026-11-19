#!/usr/bin/env python3
"""Fail closed on structurally invalid research snapshots; warn on stale or unverifiable evidence."""
import json,sys,datetime,math
from zoneinfo import ZoneInfo
from pathlib import Path
p=Path("dashboard-data.json")
data=json.loads(p.read_text(encoding="utf-8"))
required=["00_總覽","01_CSP資本支出","02_終端AI","03_硬體供應","04_交叉驗證","05_警示規則","06_資料來源","07_週次歷史","08_方法與說明","09_推論需求","10_CSP容量預測","11_資料中心逐案","12_延期取消事件","13_一致性檢查","14_變現與租金覆蓋","15_2028情境模型","16_融資與信用鏈","17_專案租金風險標籤","18_四層跨層驗證"]
assert isinstance(data.get("sheets"),dict), "sheets must be an object"
assert all(isinstance(data["sheets"].get(k),list) and data["sheets"][k] for k in required),"14 sheets required"
d=datetime.date.fromisoformat(data["asOf"])
today=datetime.datetime.now(ZoneInfo('Asia/Taipei')).date()
assert d<=today,'Snapshot date cannot be in future in Asia/Taipei'
assert isinstance(data.get("version"),str) and data["version"].strip(),"version required"
for name,rows in data["sheets"].items():
    for idx,row in enumerate(rows):
        assert isinstance(row,list),f"{name} row {idx} must be an array"
        for val in row:
            assert val is None or isinstance(val,(str,int,float,bool)),f"{name} invalid scalar"
            assert not isinstance(val,float) or math.isfinite(val),f"{name} nonfinite number"
age=(today-d).days
if age>10: print(f"::warning::Published data is {age} days old (asOf={d}); scheduling does not imply fresh research")
print(f"Validated {len(required)} sheets, version={data['version']}, date={d}, age={age}d")
print("ATTENTION: structural validation does NOT independently verify claims, source credibility, or latest market values.")

# Semantic guardrails for the explicitly unverified SKY scenarios.
sc=data['sheets']
metrics={r[0]:r for r in sc["14_變現與租金覆蓋"] if r and isinstance(r[0],str) and r[0].startswith("M")}
assert "M09" in metrics and "M10" in metrics, "SKY hypothetical revenue and hurdle must be tracked"
assert "C" in str(metrics["M09"][6]) and "C" in str(metrics["M10"][6]), "SKY forecasts must remain third-party C inputs"
assert abs(metrics["M10"][3]/metrics["M09"][3] - 347/441)<0.0001, "Base revenue scenario inconsistent"
assert "X07" in [r[0] for r in sc["18_四層跨層驗證"] if r], "CapEx vs rent accounting QA missing"
for row in sc["16_融資與信用鏈"]:
    if row and isinstance(row[0],str) and row[0].startswith("F") and row[5].startswith("A"):
        assert str(row[8]).startswith("https://"), "Primary-source financing rows need a public URL"
print("V3 financial model safeguards passed (scenario only; not verified rent coverage).")
