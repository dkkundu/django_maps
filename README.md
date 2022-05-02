# __DJMAPS__
[![django-version](https://img.shields.io/badge/django-3.2-green)](https://www.djangoproject.com)
[![python-version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org)
[![postgresql-version](https://img.shields.io/badge/postgresql-12.3-orange)](https://www.postgresql.org)
[![Coverage](https://jenkins.tiger-park.com/coverage/DJMAPS)](https://jenkins.tiger-park.com/job/DJMAPS/cobertura)
[![GH-Actions](https://github.com/Tiger-Park-Limited/DJMAPS/workflows/DJMAPS_CI/badge.svg)](https://github.com/Tiger-Park-Limited/DJMAPS/actions)
[![Jenkins_CI](https://jenkins.tiger-park.com/buildStatus/icon?job=DJMAPS&subject=Jenkins)](https://jenkins.tiger-park.com/job/DJMAPS)

###### _A Django Project._

# __Template features:__
- User Model with Profile (using Email address as username)
- Local Settings (to separate Dev/Production environments)
- Logging enabled (timely rotated daily at midnight)
- Log entries viewable under Django Admin, reusable anywhere  
- Import_Export plug-in (csv,xls,xlsx,json,etc import/export)
- Django REST Framework with API endpoints and view sets
- Django-Cors-Headers to work with Cross Origin Resource Sharing in REST API
- Django-filter for dynamic queryset filtering from url parameters
- Django-cleanup (auto removal of unused/unlinked files and images)
- Celery integration using RabbitMQ (can also use Redis)
- Test Driven Development (TDD on all written codes)
- Testing using coverage, and linting with flake8
- GitHub Actions CI, as well as Jenkins CI/CD with Docker
- Prometheus Monitoring with Model / Middleware metrics
- ...more features will be added regularly, stay tuned!

# __Usage:__
> _This document will be using the following as an input variable: `<variable>`. Please input your own value, i.e. `<project_name>` --> My-Project_
>
> _Please make sure `git`, `python`, `postgresql` and `rabbitmq` is installed in the system._
>
> _NOTE for Windows users: Please use `Git Bash` for the following steps_

1. ### Prepare project directory
    - Make your project directory (must be the same name as your github repository name)
    - Work from the project directory as current directory using `cd`.
    - Create a virtual environment using `python`. (Test via `python -V`. Must be python 3.6+)
    - `Activate` the virtual environment. (Windows: `source venv/Scripts/activate`)
    - Install `Django` using `pip`.
    ```shell script
    mkdir <project_name> && cd $_
    python -m venv venv
    source venv/bin/activate
    # Windows: source venv/Scripts/activate
    python -m pip install --upgrade pip
    ```

2. ### Install Django and startproject
    - Install `Django` v3 using `pip` within your `venv`
    - Download the __[template.zip](https://github.com/Tiger-Park-Limited/TPL_Django/archive/template.zip)__. _(Please save as template.zip in your project directory)_
    - Start your project using `django-admin` and the template.
    ```shell script
    pip install django
    # download the template.zip linked above
    django-admin startproject \
        --template template.zip \
        --extension py,md,yml,example \
        --name Dockerfile,Jenkinsfile \
        <project_name> .
    pip install -r requirements.txt
    rm -f template.zip
    ```
    > _NOTE: `<project_name>` must be the exact same name as your project repository name. The period `.` at the end of `django-admin` starts the project in the current directory._

3. ### Create Database and User
    - Using `psql`, create a `user` with encrypted `password`.
    - Create a `database` for your project.
    - Give privileges to the `user` for the `database`.
    - Alter `user` to allow for `test database` creation.
    ```shell script
    psql -U postgres
    # psql console 
    CREATE USER <project_name>_user WITH ENCRYPTED PASSWORD '<password>';
    CREATE DATABASE <project_name>_db;
    GRANT ALL PRIVILEGES ON DATABASE <project_name>_db TO <project_name>_user;
    ALTER USER <project_name>_user CREATEDB;
    \q
    ```

4. ### Configure the project
    - Create folders for `logs`, and `media`.
    - Copy `local_settings.example` to `local_settings.py`.
    - Update `local_settings.py` with proper `settings`, including `database`.
    ```shell script
    mkdir -p logs && mkdir -p media/uploads
    cp examples/local_settings.example <project_name>/local_settings.py
    
    nano <project_name>/local_settings.py
    # edit local_settings.py
    DB_NAME = '<project_name>_db'
    DB_USER = '<project_name>_user'
    DB_PASS = '<password>'
    ```

5. ### Run the project
    - Run `makemigrations` and `migrate`.
    - Run `tests` and `linting` to assure nothing is broken.
    - Create superuser to access the admin panel.
    - Run django `server` to view the project or application.
    - Generate `coverage` reports locally.
    ```shell script
    python manage.py makemigrations
    python manage.py migrate
    python manage.py test && flake8
    python manage.py createsuperuser
    python manage.py runserver
    
    # coverage reports
    coverage run manage.py test
    coverage xml -o coverage.xml
    coverage report
    ```
   > _NOTE: Browse to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site. Admin site is at url [/manage](http://127.0.0.1:8000/manage) changed from default to keep the project secure. Admin url can be changed in `settings.py` --> `ADMIN_URL`_

6. ### Git setup with actions
    - Setup GitHub actions workflow.
    - `Initialize` your project with `git`.
    - Make first `commit`.
    - Add to remote `git` link.
    - `Push` your project to `git`.
    - Make `release` branch and `push`.
    ```shell script
    # setup actions workflow
    mkdir -p .github/workflows
    cp examples/github_ci.example .github/workflows/github_ci.yml
    
    # setup github
    git init
    git add .
    git commit -m "initialize project"
    git branch -M main
    git remote add origin git@github.com:Tiger-Park-Limited/<project_name>.git
    git push -u origin main
    
    # setup release branch
    git checkout -b release
    git push -u origin release
    git checkout main  # back to dev branch, happy coding!
    ```
