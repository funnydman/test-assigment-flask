# Test assignment

## Technology Stack
 * python v3.7 
 * Docker v17.04
 * Docker-compose v1.21
 * Flask 1.0.3

### Run locally with docker

> Pre-installed docker and docker-compose assumed. No more setup is needed
```bash
docker-compose up
```

### Run without docker

1) Install necessary packages 
```bash
sudo apt-get update
sudo apt-get install -y wkhtmltopdf

```
2) Configure pipenv

```bash
pipenv install
pipenv shell
```
3) Specify your DATABASE creds in `src/main/settings/conf.py`

4) Run application
```bash
flask run
```

### Deploy in production
```bash
docker-compose -f docker-compose-prod.yml up
```

### Run tests 
```bash
python -m unittest tests/*.py
```
