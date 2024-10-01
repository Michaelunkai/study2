import os
import re

# Mapping of common module names to their corresponding pip package names
module_to_pip = {
    "tkinter": "tk",
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "pd": "pandas",
    "np": "numpy",
    "scipy": "scipy",
    "mpl": "matplotlib",
    " ": "py ",
    "pytz": "pytz",
    "sklearn": "scikit-learn",
    "pkg_resources": "setuptools",
    "google.protobuf": "protobuf",
    "pytest": "pytest",
    "dateutil": " -dateutil",
    "cryptography": "cryptography",
    "django": "django",
    "flask": "flask",
    " alchemy": " alchemy",
    "requests": "requests",
    "lxml": "lxml",
    "pytesseract": "pytesseract",
    "cv2": "opencv- ",
    "openpyxl": "openpyxl",
    "pymongo": "pymongo",
    "psycopg2": "psycopg2-binary",
    "pymy ": "pymy ",
    "gevent": "gevent",
    "gunicorn": "gunicorn",
    "celery": "celery",
    "redis": "redis",
    "pytest_cov": "pytest-cov",
    "colorama": "colorama",
    "jinja2": "jinja2",
    " parse": " parse",
    "pywin32": "pywin32",
    "zope.interface": "zope.interface",
    "pyserial": "pyserial",
    "wx": "wx ",
    "xlrd": "xlrd",
    "docutils": "docutils",
    "feedparser": "feedparser",
    "h5py": "h5py",
    "pyparsing": "pyparsing",
    "pandas_gbq": "pandas-gbq",
    "twisted": "twisted",
    "paramiko": "paramiko",
    " ": " ",
    "simplejson": "simplejson",
    "pytest_mock": "pytest-mock",
    "jsonschema": "jsonschema",
    "mpl_toolkits.basemap": "basemap",
    "Image": "image",
    "html2text": "html2text",
    "pyodbc": "pyodbc",
    "cv": "opencv- ",
    "graphviz": "graphviz",
    "requests_html": "requests-html",
    "snowflake.connector": "snowflake-connector- ",
    "tflearn": "tflearn",
    "pyTigerGraph": "pyTigerGraph",
    "pydot": "pydot",
    "py ": "py ",
    "pyttsx3": "pyttsx3",
    "pdfkit": "pdfkit",
    "playsound": "playsound",
    "pycountry": "pycountry",
    "pydotplus": "pydotplus",
    "nltk": "nltk",
    "gensim": "gensim",
    "panda ": "panda ",
    "pygsheets": "pygsheets",
    "tabulate": "tabulate",
    "Pygame": "pygame",
    "scikit_image": "scikit-image",
    "pyAesCrypt": "pyAesCrypt",
    "pyppeteer": "pyppeteer",
    "PyQt5": "PyQt5",
    "pyusb": "pyusb",
    " _openstackclient": " -openstackclient",
    "cffi": "cffi",
    "flask_ alchemy": "Flask-SQLAlchemy",
    "flask_wtf": "Flask-WTF",
    "flask_migrate": "Flask-Migrate",
    "flask_restful": "Flask-RESTful",
    "Flask_JWT_Extended": "Flask-JWT-Extended",
    "flask_marshmallow": "Flask-Marshmallow",
    "aiohttp": "aiohttp",
    "aiomy ": "aiomy ",
    "asyncpg": "asyncpg",
    "databases": "databases",
    "aioredis": "aioredis",
    "aiohttp_security": "aiohttp-security",
    "aiohttp_session": "aiohttp-session",
    "pydantic": "pydantic",
    " alchemy_utils": "SQLAlchemy-Utils",
    "itsdangerous": "itsdangerous",
    "bcrypt": "bcrypt",
    "argon2": "argon2-cffi",
    "click": "click",
    "httplib2": "httplib2",
    "httpx": "httpx",
    "httpcore": "httpcore",
    "starlette": "starlette",
    "uvicorn": "uvicorn",
    "websockets": "websockets",
    "pypika": "pypika",
    " _jose": " -jose",
    "asgiref": "asgiref",
    "pygments": "pygments",
    "requests_toolbelt": "requests-toolbelt",
    "aiobotocore": "aiobotocore",
    "pymdown_extensions": "pymdown-extensions",
    "loguru": "loguru",
    "tenacity": "tenacity",
    "djangorestframework": "djangorestframework",
    "django_filter": "django-filter",
    "django_cors_headers": "django-cors-headers",
    "channels": "channels",
    "channels_redis": "channels-redis",
    "django_extensions": "django-extensions",
    "graphene_django": "graphene-django",
    "graphene": "graphene",
    "django_graphene_jwt": "django-graphql-jwt",
    "pyexcel_xlsx": "pyexcel-xlsx",
    "plotly_express": "plotly-express",
    "fastapi_users": "fastapi-users",
    "fastapi_utils": "fastapi-utils",
}

# List of standard library modules that don't require installation
standard_lib_modules = {
    "os", "sys", "re", "json", "subprocess", "sqlite3", "time", "datetime",
    "math", "random", "string", "itertools", "functools", "collections",
    "threading", "asyncio", "http", "socket", "pathlib", "shutil", "logging",
    "email", "html", "xml", "urllib", "http.client", "http.server", "ctypes"
}

def get_ _file_path():
    path = input("Please enter the path to the Python code file: ")
    if not os.path.isfile(path):
        print("Invalid file path. Please try again.")
        return get_ _file_path()
    return path

def extract_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expression to match import statements
    import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z0-9_.]+)', re.MULTILINE)
    imports = set(import_pattern.findall(content))
    
    return imports

def map_to_pip_packages(modules):
    pip_packages = set()
    for module in modules:
        if module in standard_lib_modules:
            continue
        pip_package = module_to_pip.get(module, module)
        pip_packages.add(pip_package)
    return pip_packages

def generate_pip_command(pip_packages):
    if not pip_packages:
        return "No valid modules found on PyPI."
    pip_command = f"pip install {' '.join(pip_packages)}"
    return pip_command

def main():
     _file_path = get_ _file_path()
    modules = extract_imports( _file_path)
    pip_packages = map_to_pip_packages(modules)
    pip_command = generate_pip_command(pip_packages)
    print(f"Generated pip install command:\n{pip_command}")

if __name__ == "__main__":
    main()
