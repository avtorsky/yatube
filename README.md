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
* SQLite 3.32.3

## Changelog
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
* `source venv/bin/activate` initiates virtual environment
* `pip install -r requirements.txt` installing all dependencies

## Deploy
* `python3 manage.py runserver` initiates an HTTP server

## Contact
__GitHub:__ <a href="https://github.com/avtorsky" target="_blank">https://github.com/avtorsky</a>
