pip install ../requirements.txt
python local.py collectstatic
python local.py makemigrations
python local.py migrate
