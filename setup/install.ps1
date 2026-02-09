# Install the conducting-literature-review Claude Code skill (Windows).
#
# This script:
#   1. Creates a symlink from ~/.claude/skills/conducting-literature-review -> <repo>\skill
#   2. Clones and sets up the Semantic Scholar MCP server (Python/FastMCP)
#   3. Verifies Node.js is available (for PubMed MCP via npx)
#   4. Prints next steps for manual configuration
#
# Safe to re-run (idempotent). Does not overwrite existing installations.
# Requires Administrator privileges or Developer Mode for symlinks.

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SkillDir = Join-Path $env:USERPROFILE ".claude\skills\conducting-literature-review"
$McpDir = Join-Path $env:USERPROFILE ".claude\mcp-servers\semantic-scholar-fastmcp"
$S2Repo = "https://github.com/zongmin-yu/semantic-scholar-fastmcp.git"
$S2Commit = "580ed5a"

Write-Host "=== Conducting Literature Review -- Installation ===" -ForegroundColor Cyan
Write-Host ""

# -------------------------------------------------------
# Step 1: Skill symlink
# -------------------------------------------------------
if (Test-Path $SkillDir) {
    Write-Host "[SKIP] Skill directory already exists: $SkillDir" -ForegroundColor Yellow
    Write-Host "       Remove it first if you want to reinstall."
} else {
    $SkillsParent = Join-Path $env:USERPROFILE ".claude\skills"
    if (-not (Test-Path $SkillsParent)) {
        New-Item -ItemType Directory -Path $SkillsParent -Force | Out-Null
    }

    $SkillSource = Join-Path $RepoDir "skill"

    try {
        New-Item -ItemType SymbolicLink -Path $SkillDir -Target $SkillSource -ErrorAction Stop | Out-Null
        Write-Host "[OK]   Skill symlinked: $SkillDir -> $SkillSource" -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Symlink creation failed. Trying directory junction instead." -ForegroundColor Yellow
        Write-Host "       (Symlinks require Administrator or Developer Mode.)" -ForegroundColor Yellow
        try {
            cmd /c mklink /J "$SkillDir" "$SkillSource" | Out-Null
            Write-Host "[OK]   Skill junction created: $SkillDir -> $SkillSource" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] Could not create symlink or junction." -ForegroundColor Red
            Write-Host "        Enable Developer Mode (Settings > For developers) or run as Administrator." -ForegroundColor Red
            exit 1
        }
    }
}

# -------------------------------------------------------
# Step 2: Semantic Scholar MCP server
# -------------------------------------------------------
if (Test-Path $McpDir) {
    Write-Host "[SKIP] Semantic Scholar MCP server already exists: $McpDir" -ForegroundColor Yellow
} else {
    Write-Host "[INSTALL] Cloning Semantic Scholar MCP server..." -ForegroundColor Cyan

    $McpParent = Join-Path $env:USERPROFILE ".claude\mcp-servers"
    if (-not (Test-Path $McpParent)) {
        New-Item -ItemType Directory -Path $McpParent -Force | Out-Null
    }

    git clone $S2Repo $McpDir
    Push-Location $McpDir
    git checkout $S2Commit
    Write-Host "[OK]   Pinned to commit $S2Commit" -ForegroundColor Green

    # Detect Python 3
    $PyCmd = $null
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $PyVer = & python --version 2>&1
        if ($PyVer -match "Python 3\.") {
            $PyCmd = "python"
        }
    }
    if (-not $PyCmd -and (Get-Command python3 -ErrorAction SilentlyContinue)) {
        $PyCmd = "python3"
    }

    if (-not $PyCmd) {
        Write-Host "[ERROR] Python 3 not found. Install Python 3.10+ and re-run." -ForegroundColor Red
        Pop-Location
        exit 1
    }

    Write-Host "[INSTALL] Creating Python virtual environment..." -ForegroundColor Cyan
    & $PyCmd -m venv .venv
    & .\.venv\Scripts\pip install --quiet -r requirements.txt
    Write-Host "[OK]   Semantic Scholar MCP server installed" -ForegroundColor Green
    Pop-Location
}

# -------------------------------------------------------
# Step 3: Verify Node.js
# -------------------------------------------------------
if (Get-Command node -ErrorAction SilentlyContinue) {
    $NodeVer = & node --version
    Write-Host "[OK]   Node.js found: $NodeVer" -ForegroundColor Green
    $Major = [int]($NodeVer -replace 'v(\d+)\..*', '$1')
    if ($Major -lt 18) {
        Write-Host "[WARN] Node.js $NodeVer is below the minimum (v18). Upgrade recommended." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARN] Node.js not found. PubMed MCP server requires Node.js 18+." -ForegroundColor Yellow
    Write-Host "       Install from: https://nodejs.org/" -ForegroundColor Yellow
}

# -------------------------------------------------------
# Step 4: Print next steps
# -------------------------------------------------------
$S2Python = Join-Path $McpDir ".venv\Scripts\python.exe"
$S2Run = Join-Path $McpDir "run.py"

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Add MCP server configuration to ~/.claude.json"
Write-Host "   See: $RepoDir\setup\examples\claude-json-snippet.json"
Write-Host ""
Write-Host "   For the Semantic Scholar server, use these absolute paths:"
Write-Host "     command: $S2Python" -ForegroundColor White
Write-Host "     args:    [`"$S2Run`"]" -ForegroundColor White
Write-Host "   NOTE: In JSON, use double backslashes (\\) for Windows paths."
Write-Host ""
Write-Host "2. Add permissions to ~/.claude/settings.json"
Write-Host "   See: $RepoDir\setup\examples\settings-snippet.json"
Write-Host ""
Write-Host "3. Obtain API keys (see docs/api-keys.md):"
Write-Host "   - NCBI API key (recommended): https://www.ncbi.nlm.nih.gov/account/"
Write-Host "   - Semantic Scholar key (optional): https://www.semanticscholar.org/product/api"
Write-Host ""
Write-Host "4. Test installation:"
Write-Host "   python $RepoDir\setup\test-apis.py"
Write-Host ""
Write-Host "5. Use the skill in any project:"
Write-Host "   Type /conducting-literature-review in Claude Code"
Write-Host ""
Write-Host "=== Installation complete ===" -ForegroundColor Cyan
