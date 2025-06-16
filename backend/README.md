# Gym Management Backend

## Testing with PostgreSQL

This project uses a PostgreSQL database for testing to emulate the production environment.

### Prerequisites

- Docker and Docker Compose
- Python 3.8+

### Setting Up the Test Database

1. Start the test database container:
   ```bash
   docker-compose -f ../docker-compose.test.yml up -d
   ```

2. Reset the test database (this will drop and recreate it):
   ```bash
   python -m scripts.test_db reset
   ```

### Running Tests

Run the test suite with:

```bash
pytest
```

### Tearing Down

When you're done testing, you can stop and remove the test containers:

```bash
docker-compose -f ../docker-compose.test.yml down -v
```

## Development

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```
