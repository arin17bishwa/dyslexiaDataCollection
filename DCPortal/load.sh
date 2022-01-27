pip install -r ../requirements.txt
mkdir -p media media_cdn static static_cdn
python local.py collectstatic
python local.py makemigrations
python local.py migrate
