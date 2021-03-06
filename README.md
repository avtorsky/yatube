# Yatube

[About](#about) /
[Changelog](#changelog) /
[Environment](#environment) /
[Deploy](#deploy) /
[Contact](#contact)

## About
Networking service concept developed under the [Practicum](https://practicum.yandex.com/) online bootcamp with the following stack:
* Python 3.7.9
* Django 2.2.19
* Gunicorn 20.1.0
* PostgreSQL DBMS 12.11

## Changelog
Release 20220715:
* ci: swap config from uWSGI to Gunicorn as WSGI socket
* ci: upgrade from SQLite to PostgreSQL as DBMS in production
* fix(./yatube/yatube/settings.py): additional security improvements && Sentry setup

Release 20220503:
* ci: Nginx configuration && production build

Release 20220501:
* feat(./yatube/yatube/): add Django debug toolbar

Release 20220425:
* fix(./yatube/posts/): alter Post model, add unit testing for broken pixel in PostForm
* fix(./yatube/posts/): alter Follow model constraints

Release 20220424:
* fix(./yatube/posts/): MVT improvements after code review

Release 20220421:
* feat(./yatube/core/): error response custom routing
* feat(./yatube/posts/): media distribution cache setup && comments MVT configuration
* ci(./lintme.sh): linting && unit testing pipe setup

Release 20220410:
* fix(./yatube/): PEP8 linting && unit testing imporvements after code review

Release 20220407:
* feat(./yatube/about/): add unit testing for static views(100%)
* feat(./yatube/posts/): alter Post model, add unit testing for models(100%), urlpatterns(100%), views(98%) && forms(100%)
* feat(./yatube/users/): add unit testing for urlpatterns(100%), views(100%) && forms(100%)

Release 20220319:
* fix(./yatube/): db.sqlite3 config to .gitignore
* fix(./yatube/posts/): models.py immutable ordering && memory improvements

Release 20220317:
* feat(./yatube/): filebased.EmailBackend init
* feat(./yatube/about/): TemplateView pages setup
* feat(./yatube/core/): context_processors && css templatetags init
* feat(./yatube/posts/): profile, post_detail, post_create, post_edit views && routes setup
* feat(./yatube/users/): override auth templates

Release 20220222:
* fix(./yatube/posts/): admin.py PEP8 linting && models.py style improvements after code review

Release 20220219:
* feat(./yatube/posts/): static, templates markup && initial ORM setup

Release 20220212:
* fix(\_\_pycache\_\_): include all cache directories to .gitignore

Release 20220211:
* feat(./yatube/posts/): initial routing setup for posting module
* docs(./README.md): repository init, venv && Django setup

## Environment
Production build: https://yatube.avtorskydeployed.online

## Deploy
Initiate unit testing pipe, install all dependencies && stage an HTTP server

```bash
bash lintme.sh
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Declare DJANGO_KEY, HOSTS, ROOT && DB variables at .env file then proceed:

```bash
cd yatube
python3 manage.py migrate
python3 manage.py runserver
```

## Contact
__GitHub:__ <a href="https://github.com/avtorsky" target="_blank">https://github.com/avtorsky</a>
