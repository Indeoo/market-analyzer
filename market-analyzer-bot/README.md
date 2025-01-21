RUN DB:
docker run --name analyzer-container \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -p 5433:5432 \
  -d postgres