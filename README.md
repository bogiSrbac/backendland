# backendland
game
enter in directory with docker-compose.yml file
run next command:
  docker-compose up -d --build
  docker-compose run app python manage.py createsuperuser //after you create superusers
  docker-compose run app python receiver2.py
  open http://127.0.0.1:8000/hocus/
  
