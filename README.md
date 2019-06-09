### Run locally with docker

> Pre-installed docker and docker-compose assumed. No more setup is needed
```bash
docker-compose up
```

### Run without docker

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
