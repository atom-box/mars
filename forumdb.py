# "Database code" for the DB Forum.

import datetime, psycopg2

db = psycopg2.connect(dbname = 'forum')
c = db.cursor()
query = 'insert into posts values(null, null  );'


c.execute(query)




#"""Return all posts from the 'database', most recent first."""

def get_posts():
	# todo always give the same select.  fetchall or something
	print("Top of get_posts executed.")
	return [("Harry Potter", datetime.datetime.now() )]

#"""Add a post to the 'database' with the current timestamp."""
def add_post(content):
	print("Top of add_post executed.")
	c.execute('insert into posts values(null, ;')

