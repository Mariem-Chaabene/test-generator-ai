from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

<<<<<<< HEAD
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/test_generator_ai"

engine = create_engine(DATABASE_URL)

=======
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/your_db"

engine = create_engine(DATABASE_URL)
>>>>>>> cf32ac958a1882f8fe246d0cb3a200946693257e
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()