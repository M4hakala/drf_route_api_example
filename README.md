# Requirements
- python 3.7+
- virtualenv
- Django 3.0
- Django rest framework

# Docker environment

## Production

### Build
```bash
$ docker-compose -f docker-compose.prod.yml build --force-rm --no-cache --pull
```

### Running
```bash
$ docker-compose -f docker-compose.prod.yml up -d --remove-orphans
```

## Development

### Build
```bash
$ docker-compose build --force-rm --no-cache --pull
```

## Running
```bash
$ docker-compose up -d --remove-orphans
```

# Local environment

## Virtual environment installation
```bash
$ virtualenv -p pytho3.7 venv
```

## Virtual environment activation 
```bash
$ source venv/bin/activate
```

## Dependencies installation
```bash
$ pip install -r requirements.txt
```
and for development and testing:
```bash
$ pip install -r requirements.dev.txt
```

## Support for django-admin command 
For proper work of django-admin command we need to export few environment variables:
```bash
$ source init_local_env_var.sh
```

## Migrations
```bash
$ django-admin migrate
```

## Running
```bash
$ python manage.py runserver 0.0.0.0:5000
```

## Testing
While API is running
```bash
$ python manage.py test
```

## Superuser creation
```bash
$ echo "from django.contrib.auth.models import User; User.objects.create_superuser('superuser', 'superuser@example.com', 'password')" | django-admin shell
```

