# Run
Clone the repository and start the services:
```sh
git clone https://github.com/pecimuth/synthia.git
cd synthia
docker-compose up
```

Create the database schema:
```sh
docker exec synthia_backend_1 flask recreate-database
```

The API server is available on `localhost:5000/apidocs`. The frontend listens on `localhost:4200`.
