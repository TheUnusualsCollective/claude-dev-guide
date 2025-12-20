#!/usr/bin/env python3
"""
Simple directive loader hook.
Injects quick-reference directive into context.
"""
import os
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
if not project_dir:
    exit(0)

directives_dir = Path(project_dir) / "claude-config" / "directives"
quick_ref = directives_dir / "directives-quick-reference.md"

if quick_ref.exists():
    print("=== CODING DIRECTIVES (auto-loaded) ===\n")
    print(quick_ref.read_text(encoding='utf-8'))

exit(0)
