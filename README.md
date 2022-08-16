# News service

## Local deploy

requirements: python 3.10

```
virtualenv -p $(which python3.10) env
source env/bin/activate
pip install -r requirements.txt
python main.py
```

## Docker deploy

```
docker-compose build
docker-compose up
```

URL: http://0.0.0.0:8080

## Test

```
pytest
```
