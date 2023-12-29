from sqlalchemy import create_engine, Column, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'Subject'

    SubCode = Column(Text, primary_key=True, unique=True, nullable=False)
    Name = Column(Text, nullable=False)

# Create an SQLite database engine
engine = create_engine('sqlite:///database.db')

# Bind the engine to the Base class
Base.metadata.bind = engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the Subject table
subjects_data = [
    {'SubCode': 'SUB1', 'Name': 'Subject 1'},
    {'SubCode': 'SUB2', 'Name': 'Subject 2'},
    {'SubCode': 'SUB3', 'Name': 'Subject 3'},
]

for subject_data in subjects_data:
    subject = Subject(**subject_data)
    session.add(subject)

# Commit the changes to the database
session.commit()

# Close the session
session.close()

print("Data inserted into the Subject table.")
