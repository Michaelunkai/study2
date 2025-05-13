# modern-docker-ui

This project is a complete overhaul of the user interface and design for the existing Docker management tool. The goal is to provide a smooth and professional appearance, enhancing user experience and usability.

## Project Structure

```
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
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/modern-docker-ui.git
   cd modern-docker-ui
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Alternatively, you can use pip:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.