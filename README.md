# My portfolio using Django
My portfolio deployed on Railway using Django Framework and PostgreSQL database. Self-design UI/UX using Figma and Bootstrap 5.

Note: You might feel this similar to my older GitHub [uyenbhku.github.io](https://github.com/uyenbhku/uyenbhku.github.io). It is simply because I made this one based on that repo.

### Visit it here: [uyenbhku.onrender.com](https://uyenbhku.onrender.com/)

## Current features: 
- Simple GUI
- Add/Change/Remove new projects showcase from local
- Receive contact request from users
- Administrator page [NEW]: add features to change visible information easier

## Upcoming features:
- Embed Computer Vision and AI-powered tools/projects I (partially) created during my school years.
- Apply data science tools
- A few more..

### RUN APP LOCALLY

Create or activate an existing (virtual environment)[https://docs.python.org/3/library/venv.html] 
```bash
# Create a new virtual env
python -m venv /path/to/new/virtual/environment
# e.g: Activate an existing virtual environment on Windows
source env/Scripts/activate
```

Run these commands on demand

- `python manage.py runserver` : run server on localhost:8000/
- `python manage.py collectstatic` : process staticfiles for deployment
- `python manage.py test` : conduct unit test
- `python manage.py createsuperuser` : create admin user 
- `python manage.py migrate` : update database