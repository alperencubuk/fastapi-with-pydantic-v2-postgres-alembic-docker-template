# FastAPI (with Pydantic v2) Postgres Alembic Docker Template

---

### Requirements:

```
docker
docker-compose
```

### Run:

```
cp config/.env.example config/.env
docker-compose up --build -d
```

### Migration:

```
docker-compose exec api alembic revision --autogenerate
docker-compose exec api alembic upgrade head
```

### Test:

```
docker exec -it api pytest
```

### Coverage:

```
docker exec -it api coverage run -m pytest
docker exec -it api coverage report
```

### Docs:

```
localhost:8000/docs
```

### Endpoints:

```http request
POST   /boilerplate                     # boilerplate create
GET    /boilerplate                     # boilerplate list
GET    /boilerplate/{boilerplate_id}    # boilerplate get
PATCH  /boilerplate/{boilerplate_id}    # boilerplate update
DELETE /boilerplate/{boilerplate_id}    # boilerplate delete

GET    /                                # health check
```

---
