# kijiji.ca Parser API
## Installation
You need to setup some .env files

**db_creds.env**
```
MONGO_INITDB_DATABASE=scraper
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin
```

**Build docker images**
```
docker-compose build
```

## Run application
```
docker-compose up
```