from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData

db_string = "postgresql+psycopg2://postgres:1234567@localhost:5432/batch2db"

db = create_engine(db_string)


meta = MetaData(db)

# create a Table
films_table = Table(
    'films_exp',
    meta,
    Column('title', String),
    Column('director', String),
    Column('year', String)
)

with db.connect() as conn:
    films_table.create()
    insert_statement =films_table.insert().values(
        title="Doctor Strange",
        director="Rohit Shetty",
        year="2016"
    )
    conn.execute(insert_statement)
    
#Read

# below code is written by github copilot

# with db.connect() as conn:
#     select_statement = films_table.select()
#     result_set = conn.execute(select_statement)
#     for r in result_set:
#         print(r)
        