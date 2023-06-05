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

metadata_obj = sqlalchemy.MetaData()
user = sqlalchemy.Table("user", metadata_obj, autoload_with=engine)
deposit = sqlalchemy.Table("deposit", metadata_obj, autoload_with=engine)
expense = sqlalchemy.Table("expense", metadata_obj, autoload_with=engine)
category = sqlalchemy.Table("category", metadata_obj, autoload_with=engine)
budget = sqlalchemy.Table("budget", metadata_obj, autoload_with=engine)
item = sqlalchemy.Table("item", metadata_obj, autoload_with=engine)