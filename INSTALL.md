# Kenopsia Core v0.2.1 Install

```bash
cd ~/Git

rm -rf kenopsia-core kenopsia-core-v0.2.1

unzip -o ~/Downloads/kenopsia-core-v0.2.1.zip -d ~/Git

mv kenopsia-core-v0.2.1 kenopsia-core
cd ~/Git/kenopsia-core

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

./scripts/validate.sh
./scripts/run.sh

xdg-open reports/kenopsia-report.html
```
