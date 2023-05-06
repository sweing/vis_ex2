create environment:
python -m venv vis_ex2

activate environment 
source vis_ex2/bin/activate

pip install -r requirements.txt

run:
FLASK_APP=app.py flask run
