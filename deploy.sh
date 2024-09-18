#!/bin/bash

#!/bin/bash

# Step 1: Start the Django development server using Poetry
echo "Starting Django server with Poetry..."
poetry run python manage.py runserver &

# Step 2: Start Tailwind watcher using Poetry
echo "Starting Tailwind CSS watcher with Poetry..."
poetry run python manage.py tailwind start

# Wait for both processes to finish
wait