import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://txoytuiksvhssc:a7d9ca8df13af8faec463783b2c0cc3506b6ff348f6d2afec54af9a212abc09b@ec2-35-174-88-65.compute-1.amazonaws.com:5432/d4a91cto59cs85'

SQLALCHEMY_TRACK_MODIFICATIONS = False