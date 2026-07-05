# Kenopsia Core v0.2.0 Overlay

This overlay adds the v0.2.0 assessment foundation.

## Install overlay into your repo

PowerShell:

```powershell
$Repo = "C:\Git\kenopsia-core"
$Zip  = "$HOME\Downloads\kenopsia-core-v0.2.0-overlay.zip"
$Temp = Join-Path $env:TEMP "kenopsia-core-v0.2.0-overlay"

Remove-Item $Temp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive $Zip -DestinationPath $Temp -Force
Copy-Item "$Temp\kenopsia-core-v0.2.0-overlay\*" $Repo -Recurse -Force

Set-Location $Repo
git status
```

Linux/macOS:

```bash
REPO="$HOME/Git/kenopsia-core"
ZIP="$HOME/Downloads/kenopsia-core-v0.2.0-overlay.zip"
TEMP="/tmp/kenopsia-core-v0.2.0-overlay"

rm -rf "$TEMP"
unzip -q "$ZIP" -d "$TEMP"
rsync -av "$TEMP/kenopsia-core-v0.2.0-overlay/" "$REPO/"

cd "$REPO"
git status
```

## Validate

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pytest tests/test_assessment_engine_v020.py
python scripts/run_v020_assessment.py --out output
```

## Suggested commit

```bash
git add .
git commit -m "Add v0.2.0 assessment foundation"
git tag v0.2.0
```
