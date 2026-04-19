#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Startup check script for Kim Mun Dictionary Hub
Run this at the start of each session to verify environment and files.
"""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AI_CTX = ROOT / '.ai_context'
DB = ROOT / 'kim_mun_dict_v2.db'
REQUIRED_MD = ['ARCHITECTURE.md','ROADMAP.md','task.md','implementation_plan.md','AI_PROMPT_INIT.md','AGENT_SUMMARY.md','PAGE_REFERENCES_GUIDE.md']

print('\n=== STARTUP CHECK - Kim Mun Dictionary Hub ===\n')

# 1. Check .ai_context exists
print('1) .ai_context folder: ', 'FOUND' if AI_CTX.exists() else 'MISSING')

# 2. List markdown files and existence
print('\n2) Required .md files:')
for md in REQUIRED_MD:
    p = AI_CTX / md
    print(f'   - {md}:', 'OK' if p.exists() else 'MISSING')

# 3. Database check
print('\n3) Database check:')
if DB.exists():
    print(f'   - DB found: {DB} (size: {DB.stat().st_size // 1024} KB)')
    try:
        conn = sqlite3.connect(str(DB))
        c = conn.cursor()
        c.execute("SELECT count(*) FROM dictionary")
        total = c.fetchone()[0]
        print(f'   - Total entries in `dictionary` table: {total}')
        # Count entries with page_ref
        c.execute("SELECT count(*) FROM dictionary WHERE page_ref != '' AND page_ref IS NOT NULL")
        pr = c.fetchone()[0]
        print(f'   - Entries with page_ref: {pr}')
        conn.close()
    except Exception as e:
        print('   - ERROR reading DB:', e)
else:
    print('   - DB missing: create or place `kim_mun_dict_v2.db` in the folder')

# 4. Web UI check
print('\n4) Web UI check:')
web_ui = ROOT / 'web_ui' / 'app.py'
print('   - web_ui/app.py:', 'OK' if web_ui.exists() else 'MISSING')

# 5. Page mapping check
print('\n5) Page mapping file:')
pr_map = ROOT / 'page_reference_mapping.json'
print('   - page_reference_mapping.json:', 'OK' if pr_map.exists() else 'MISSING')

# 6. Git notice
print('\n6) GitHub notice:')
gh = AI_CTX / 'GITHUB_NOTICE.md'
print('   - GITHUB_NOTICE.md:', 'OK' if gh.exists() else 'MISSING')

print('\n=== END OF CHECK. If any items are MISSING, please read .ai_context files and follow instructions. ===\n')
