from sqlalchemy import create_engine
from models import Base

# Create database
engine = create_engine('sqlite:///tarot.db')
Base.metadata.create_all(engine)

print("Database created successfully!") 