#!/bin/bash
# Install the conducting-literature-review Claude Code skill.
#
# This script:
#   1. Creates a symlink from ~/.claude/skills/conducting-literature-review -> <repo>/skill
#   2. Clones and sets up the Semantic Scholar MCP server (Python/FastMCP)
#   3. Verifies Node.js is available (for PubMed MCP via npx)
#   4. Prints next steps for manual configuration
#
# Safe to re-run (idempotent). Does not overwrite existing installations.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$HOME/.claude/skills/conducting-literature-review"
MCP_DIR="$HOME/.claude/mcp-servers/semantic-scholar-fastmcp"
S2_REPO="https://github.com/zongmin-yu/semantic-scholar-fastmcp.git"
S2_COMMIT="580ed5a"

echo "=== Conducting Literature Review -- Installation ==="
echo ""

# -------------------------------------------------------
# Step 1: Skill symlink
# -------------------------------------------------------
if [ -e "$SKILL_DIR" ]; then
    echo "[SKIP] Skill directory already exists: $SKILL_DIR"
    echo "       Remove it first if you want to reinstall:"
    echo "       rm -rf $SKILL_DIR"
else
    mkdir -p "$HOME/.claude/skills"
    ln -s "$REPO_DIR/skill" "$SKILL_DIR"
    echo "[OK]   Skill symlinked: $SKILL_DIR -> $REPO_DIR/skill"
fi

# -------------------------------------------------------
# Step 2: Semantic Scholar MCP server
# -------------------------------------------------------
if [ -d "$MCP_DIR" ]; then
    echo "[SKIP] Semantic Scholar MCP server already exists: $MCP_DIR"
else
    echo "[INSTALL] Cloning Semantic Scholar MCP server..."
    mkdir -p "$HOME/.claude/mcp-servers"
    git clone "$S2_REPO" "$MCP_DIR"
    cd "$MCP_DIR"
    git checkout "$S2_COMMIT"
    echo "[OK]   Pinned to commit $S2_COMMIT"

    # Detect Python 3
    if command -v python3 &>/dev/null; then
        PY=python3
    elif command -v python &>/dev/null; then
        PY=python
    else
        echo "[ERROR] Python 3 not found. Install Python 3.10+ and re-run."
        exit 1
    fi

    echo "[INSTALL] Creating Python virtual environment..."
    "$PY" -m venv .venv
    .venv/bin/pip install --quiet -r requirements.txt
    echo "[OK]   Semantic Scholar MCP server installed"
    cd "$REPO_DIR"
fi

# -------------------------------------------------------
# Step 3: Verify Node.js (for PubMed MCP via npx)
# -------------------------------------------------------
if command -v node &>/dev/null; then
    NODE_VER=$(node --version)
    echo "[OK]   Node.js found: $NODE_VER"
    # Check minimum version
    MAJOR=$(echo "$NODE_VER" | sed 's/v\([0-9]*\).*/\1/')
    if [ "$MAJOR" -lt 18 ]; then
        echo "[WARN] Node.js $NODE_VER is below the minimum (v18). Upgrade recommended."
    fi
else
    echo "[WARN] Node.js not found. PubMed MCP server requires Node.js 18+."
    echo "       Install from: https://nodejs.org/"
fi

# -------------------------------------------------------
# Step 4: Print configuration paths for next steps
# -------------------------------------------------------
S2_PYTHON="$MCP_DIR/.venv/bin/python"
S2_RUN="$MCP_DIR/run.py"

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Add MCP server configuration to ~/.claude.json"
echo "   See: $REPO_DIR/setup/examples/claude-json-snippet.json"
echo ""
echo "   For the Semantic Scholar server, use these absolute paths:"
echo "     command: $S2_PYTHON"
echo "     args:    [\"$S2_RUN\"]"
echo ""
echo "2. Add permissions to ~/.claude/settings.json"
echo "   See: $REPO_DIR/setup/examples/settings-snippet.json"
echo ""
echo "3. Obtain API keys (see docs/api-keys.md):"
echo "   - NCBI API key (recommended): https://www.ncbi.nlm.nih.gov/account/"
echo "   - Semantic Scholar key (optional): https://www.semanticscholar.org/product/api"
echo ""
echo "4. Test installation:"
echo "   python3 $REPO_DIR/setup/test-apis.py"
echo ""
echo "5. Use the skill in any project:"
echo "   Type /conducting-literature-review in Claude Code"
echo ""
echo "=== Installation complete ==="
