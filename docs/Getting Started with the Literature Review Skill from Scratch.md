# Getting Started with the Literature Review Skill from Scratch 

A beginner-friendly guide to setting up the **conducting-literature-review** Claude Code skill. This skill automates rigorous literature reviews using PubMed, Semantic Scholar, and web search.

---

## What You Need

### Software to Install (all free)

1. **VS Code** — A code editor (you'll use its built-in terminal and the Claude Code extension)
   - Download: https://code.visualstudio.com
   - Install it like any normal app

2. **Claude Code extension for VS Code** — This is what actually runs the skill
   - Open VS Code → click the Extensions icon (left sidebar, looks like 4 squares) → search "Claude Code" → Install
   - You'll need an Anthropic account. Claude Code uses your Claude Pro/Team subscription or API credits.
   - More info: https://docs.anthropic.com/en/docs/claude-code

3. **Node.js 18+** — Needed for the PubMed search server
   - Download: https://nodejs.org (choose the LTS version)
   - Install it like any normal app

4. **Python 3.10+** — Needed for the Semantic Scholar search server
   - Download: https://www.python.org/downloads/ (choose the latest version)
   - **Important (Windows):** During install, check the box that says "Add Python to PATH"

5. **Git** — Needed to download the skill
   - Download: https://git-scm.com/downloads
   - Install with default settings

### API Keys (free, takes ~5 minutes)

- **NCBI API Key** (for PubMed) — Recommended. Register at https://www.ncbi.nlm.nih.gov/account/ and request an API key from your account settings.
- **Semantic Scholar API Key** — Optional. Request at https://www.semanticscholar.org/product/api#api-key-form

---

## Setup Steps

### Step 1: Open VS Code's Terminal

Open VS Code → click **Terminal** in the top menu → **New Terminal**. A command line panel appears at the bottom.

### Step 2: Clone the Repository

Type the following in the terminal and press Enter:

```
git clone https://github.com/Hcarm/conducting-literature-review.git
cd conducting-literature-review
```

### Step 3: Run the Install Script

**Mac/Linux:**
```
bash setup/install.sh
```

**Windows (PowerShell):**
```
powershell -ExecutionPolicy Bypass -File setup\install.ps1
```

This does three things automatically:
- Links the skill so Claude Code can find it
- Sets up the Semantic Scholar search server
- Checks that Node.js is available

### Step 4: Configure MCP Servers

The install script will print a block of JSON. You need to add it to your Claude Code configuration file at `~/.claude.json`.

- On Mac/Linux: `~/.claude.json`
- On Windows: `C:\Users\YourName\.claude.json`

There's a template at `setup/examples/claude-json-snippet.json` in the repo. The server names **must** be exactly `pubmed-mcp-server` and `semantic-scholar`.

### Step 5: Add Permissions

Merge the contents of `setup/examples/settings-snippet.json` into `~/.claude/settings.json`. This pre-approves access to academic publisher websites and the MCP search tools.

### Step 6: Add Your API Keys

Set your NCBI API key as an environment variable:

**Mac/Linux** (add to `~/.zshrc` or `~/.bashrc`):
```
export NCBI_API_KEY="your-key-here"
```

**Windows** (PowerShell):
```
[System.Environment]::SetEnvironmentVariable("NCBI_API_KEY", "your-key-here", "User")
```

### Step 7: Verify Everything Works

```
python setup/test-apis.py
```

You should see mostly `[PASS]` results. A `[WARN]` for S2 keyword search is normal.

---

## Using the Skill

1. Open VS Code
2. Open the Claude Code panel (click the Claude icon in the sidebar, or use the command palette)
3. Navigate to any project folder where you want your literature review saved
4. Type: `/conducting-literature-review`
5. Follow the prompts — choose Narrow Search (quick, 8–14 papers) or Full Review (comprehensive, 30–48+ papers)

The skill will create a `Literature/` folder in your project with all outputs.

---

## Troubleshooting

- **"command not found" errors** — Make sure Node.js, Python, and Git are in your system PATH. Restart VS Code after installing them.
- **MCP server connection failures** — Double-check the server names in `~/.claude.json` are exactly `pubmed-mcp-server` and `semantic-scholar`.
- **The skill works even if some things fail** — If PubMed is down, it uses Semantic Scholar. If both are down, it uses web search. You'll be notified of any fallbacks.
- **Full troubleshooting guide** — See `TROUBLESHOOTING.md` in the repo.

---

## Quick Reference

| What | Where |
|------|-------|
| Skill repo | https://github.com/Hcarm/conducting-literature-review |
| Claude Code docs | https://docs.anthropic.com/en/docs/claude-code |
| VS Code download | https://code.visualstudio.com |
| Node.js download | https://nodejs.org |
| Python download | https://www.python.org/downloads |
| NCBI API key | https://www.ncbi.nlm.nih.gov/account |
