modern-docker-ui
├── src
│   ├── assets
│   │   ├── fonts
│   │   └── styles
│   │       ├── base.qss
│   │       └── theme.qss
│   ├── components
│   │   ├── __init__.py
│   │   ├── buttons.py
│   │   ├── dialogs.py
│   │   ├── navigation.py
│   │   └── containers.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── docker.py
│   │   └── settings.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── docker_service.py
│   │   └── image_service.py 
│   ├── utils
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   └── helpers.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── tabs
│   │       ├── __init__.py
│   │       └── tag_view.py
│   ├── __init__.py
│   ├── app.py
│   └── main.py
├── tests
│   ├── __init__.py
│   ├── test_docker_service.py
│   └── test_models.py
├── .gitignore
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt