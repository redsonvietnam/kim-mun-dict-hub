#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent Onboarding Checklist
Danh sách kiểm tra cho AI Agent mới
Chạy script này khi bắt đầu session mới!
"""
import os
import sqlite3
from pathlib import Path

print("\n" + "="*70)
print("🤖 AI AGENT ONBOARDING CHECKLIST")
print("="*70)

project_root = Path(".")
db_path = "kim_mun_dict_v2.db"
context_dir = ".ai_context"

# ✅ Checklist items
checklist = []

# 1. Check README.md
print("\n[1/7] 📖 Kiểm tra README.md...")
if (project_root / "README.md").exists():
    size = (project_root / "README.md").stat().st_size
    print(f"    ✅ README.md: {size} bytes")
    checklist.append(True)
else:
    print("    ❌ README.md: NOT FOUND")
    checklist.append(False)

# 2. Check context files
print("\n[2/7] 📚 Kiểm tra các file context...")
context_files = [
    "QUICK_START.md",
    "AI_AGENT_INIT.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "task.md",
    "implementation_plan.md",
    "PAGE_REFERENCES_GUIDE.md"
]

all_context_ok = True
for cf in context_files:
    path = project_root / context_dir / cf
    if path.exists():
        print(f"    ✅ {cf}")
    else:
        print(f"    ❌ {cf}: MISSING")
        all_context_ok = False

checklist.append(all_context_ok)

# 3. Check database
print("\n[3/7] 🗄️ Kiểm tra Database...")
if Path(db_path).exists():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM dictionary")
    count = c.fetchone()[0]
    print(f"    ✅ Database: {count} entries")
    checklist.append(True)
    conn.close()
else:
    print(f"    ❌ Database: NOT FOUND ({db_path})")
    checklist.append(False)

# 4. Check web_ui files
print("\n[4/7] 🌐 Kiểm tra Web UI files...")
web_ui_files = [
    "web_ui/app.py",
    "web_ui/templates/index.html"
]

web_ui_ok = True
for wf in web_ui_files:
    if (project_root / wf).exists():
        print(f"    ✅ {wf}")
    else:
        print(f"    ❌ {wf}: MISSING")
        web_ui_ok = False

checklist.append(web_ui_ok)

# 5. Check utility scripts
print("\n[5/7] 🔧 Kiểm tra Utility scripts...")
scripts = [
    "check_db_status.py",
    "show_page_samples.py",
    "export_for_page_review.py"
]

scripts_ok = True
for s in scripts:
    if (project_root / s).exists():
        print(f"    ✅ {s}")
    else:
        print(f"    ❌ {s}: MISSING")
        scripts_ok = False

checklist.append(scripts_ok)

# 6. Check JSON data files
print("\n[6/7] 📊 Kiểm tra Data files...")
json_files = [
    "page_reference_mapping.json",
    "kim_mun_dict_with_pages.csv"
]

json_ok = True
for jf in json_files:
    if (project_root / jf).exists():
        print(f"    ✅ {jf}")
    else:
        print(f"    ⚠️  {jf}: optional")

checklist.append(True)  # Optional files

# 7. Database health check
print("\n[7/7] ❤️ Database Health Check...")
if Path(db_path).exists():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check each source
    c.execute("SELECT source, COUNT(*) FROM dictionary GROUP BY source")
    sources = c.fetchall()
    
    health_ok = True
    for source, count in sources:
        print(f"    ✅ {source}: {count} entries")
        if count == 0:
            health_ok = False
    
    conn.close()
    checklist.append(health_ok)
else:
    checklist.append(False)

# Summary
print("\n" + "="*70)
print("📊 KIỂM TRA TỔNG HỢP")
print("="*70)

passed = sum(checklist)
total = len(checklist)

print(f"\nĐã kiểm tra: {passed}/{total} ✅")

if passed == total:
    print("\n🎉 TẤT CẢ KIỂM TRA PASSED!")
    print("\n📖 TIẾP THEO:")
    print("  1. Đọc: .ai_context/QUICK_START.md (2 phút)")
    print("  2. Đọc: .ai_context/AI_AGENT_INIT.md (5-10 phút)")
    print("  3. Đọc: Toàn bộ các file .md trong .ai_context/")
    print("  4. Chạy: python check_db_status.py")
    print("  5. Hỏi user: 'Chúng ta tiếp tục ở đâu?'")
    print("\n✨ Ready to go! 🚀")
else:
    print(f"\n⚠️ CẢNH BÁO: {total - passed} kiểm tra không passed")
    print("Kiểm tra các file bị thiếu ở trên")

print("\n" + "="*70 + "\n")
