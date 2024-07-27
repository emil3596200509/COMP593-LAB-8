"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.

"""
import os
import sqlite3
from faker import Faker
from random import random, choice

# Determine the path of the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'social_network.db')

def main():
    create_relationships_table()
    populate_relationships_table()
  

def create_relationships_table():
    """Creates the relationships table in the DB"""
    with sqlite3.connect(db_path) as con:
        cur = con.cu()
        relationship_table = """
        CREATE TABLE IF NOT EXISTS relationships
        (
            id INTEGER PRIMARY KEY, 
            person1_id INTEGER NOT NULL,
            person2_id INTEGER NOT NULL,
            relationship_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            FOREIGN KEY (person1_id) REFERENCES people (id),
            FOREIGN KEY (person2_id) REFERENCES people (id)
        );
       """
        cur.execute(relationship_table)
        con.commit()

def populate_relationships_table():
    """Adds 100 random relationships to the DB"""
    with sqlite3.connect(db_path) as con:
        cur = con.cur()
        add_relationship = """
        INSERT INTO relationships
        (
            person1_id,
            person2_id,
            relationship_type,
            start_date
        )
        VALUES (?, ?, ?, ?);
        """
        fake = Faker()
        con.execute("BEGIN TRANSACTION")
        person1_id = fake.random_int(min=1, max=100)
        person2_id = fake.random_int(min=1, max=100)
        while person1_id == person2_id:
                person2_id = fake.random_int(1, 100)
        relationship_type = choice(['Friend', 'Spouse', 'Girlfriend'])
        start_date = fake.date_between(start_date='-50y', end_date='today')
        new_relationship = (person1_id, person2_id, relationship_type, start_date)
        cur.execute(add_relationship, new_relationship)
        con.commit()

if __name__ == '_main_':
   main()