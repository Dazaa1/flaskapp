import sqlite3                    # For connecting to a SQLite database
from datetime import datetime    

import click                     # Used for command-line commands in Flask
from flask import current_app, g  # `current_app` gives access to the running app, `g` stores data for one request

# This function returns a connection to the database
def get_db():
    # Check if there is already a database connection stored in `g`
    if 'db' not in g:
        # If not, create a new connection using the path stored in app config
        # `current_app` lets us access the app's config even though we don't have the app object directly
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],   # Get the database file path from config
            detect_types=sqlite3.PARSE_DECLTYPES  # Helps SQLite understand data types like datetime
        )

        # This makes the rows behave like dictionaries
        # So instead of accessing columns by index (e.g., row[0]), we can use keys (e.g., row["name"])
        g.db.row_factory = sqlite3.Row

    # Return the database connection (reuses it if already created in this request)
    return g.db

# This function is used to close the database connection after the request is done
def close_db(e=None):
    # Remove the connection from `g` (and get it at the same time)
    db = g.pop('db', None)

    # If there was a connection, close it
    if db is not None:
        db.close()

    
def init_db():
    # new connection
    db = get_db()

    # exectute
    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf8'))


# creating a command line that runs init_db()
@click.command()
def init_db_command():
    init_db()
    click.echo('Initialized the database')

# tells how to handle timestamps we convert them to datetime.datetime
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
