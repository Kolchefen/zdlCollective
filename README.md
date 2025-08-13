# zdlcollective.com

This is my portfolio website repo

## Installation

To set up the project run the following:

```bash
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Create dev docker environment
```bash
# Start development environment
docker-compose up -d

# Stop development environment  
docker-compose down

# View logs
docker-compose logs web

# Restart after code changes (if needed)
docker-compose restart web

# Check container status
docker-compose ps
```

## DB management
To create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
``` 


## License

[MIT](https://choosealicense.com/licenses/mit/)
