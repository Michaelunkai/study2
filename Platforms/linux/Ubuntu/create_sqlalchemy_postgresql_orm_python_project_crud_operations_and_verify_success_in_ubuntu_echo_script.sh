#!/bin/ 

# Script name: create_sqlalchemy_postgresql_orm_python_project_crud_operations_and_verify_success_in_ubuntu_echo_script.sh
# Description: This script sets up Python, installs SQLAlchemy and PostgreSQL, sets up an ORM project, performs CRUD operations, and verifies successful execution.

# Create project directory in /home/ubuntu
mkdir -p /home/ubuntu/my_orm_project
cd /home/ubuntu/my_orm_project

# Install Python and pip if not already installed
sudo apt install -y python3 python3-pip

# Install SQLAlchemy and PostgreSQL driver
pip3 install SQLAlchemy psycopg2-binary

# Install PostgreSQL if not installed
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to PostgreSQL user and create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
EOF

# Echo Python ORM script (main.py) to the file
echo 'from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL setup
engine = create_engine("postgresql+psycopg2://myuser:mypassword@localhost/mydatabase", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, nickname={self.nickname})>"

# Create tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create new users
user1 = User(name="john", fullname="John Doe", nickname="johnny")
user2 = User(name="jane", fullname="Jane Smith", nickname="janie")

# Add records to the session
session.add(user1)
session.add(user2)
session.commit()

# Read Operations
all_users = session.query(User).all()
print("All Users:")
for user in all_users:
    print(user)

john = session.query(User).filter_by(name="john").first()
print("\nFiltered User:")
print(john)

# Update Operation
john.nickname = "john_the_great"
session.commit()
print("\nUpdated User:")
print(session.query(User).filter_by(name="john").first())

# Delete Operation
session.delete(user2)
session.commit()

print("\nUsers after deletion:")
for user in session.query(User).all():
    print(user)' > /home/ubuntu/my_orm_project/main.py

# Run the Python script
 3 /home/ubuntu/my_orm_project/main.py

# Verification to check if the setup was successful
if [ $? -eq 0 ]; then
    echo "Setup and script execution were successful."
else
    echo "There was an error during the setup or script execution."
fi
