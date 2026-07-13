git clone <GraphGuard>

cd GraphGuard

python3.11 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

git clone https://github.com/IDEA-Research/GroundingDINO.git third_party/GroundingDINO

cd third_party/GroundingDINO
pip install -e . --no-build-isolation

# Download checkpoint
# Place groundingdino_swint_ogc.pth inside checkpoints/