import sqlalchemy
import os
import dotenv

# DO NOT CHANGE THIS TO BE HARDCODED. ONLY PULL FROM ENVIRONMENT VARIABLES.
dotenv.load_dotenv()
DB_USER: str = os.environ.get("POSTGRES_USER")
DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
DB_PORT: str = os.environ.get("POSTGRES_PORT")
DB_NAME: str = os.environ.get("POSTGRES_DB")

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}")