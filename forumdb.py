# "Database code" for the DB Forum.

import datetime, psycopg2
BASE1 = 'forum'


db = psycopg2.connect(dbname = BASE1)
c = db.cursor()
print "Hey", datetime.datetime.now() , " !!!"
query = "insert into posts values('Lou ', null,88  );" # works
c.execute(query) # works
db.close()


#"""Return all posts from the 'database', most recent first."""

def get_posts():
	# todo always give the same select.  fetchall or something
	print("Top of get_posts executed.")
	return [("Harry Potter", datetime.datetime.now() )]

#"""Add a post to the 'database' with the current timestamp."""
def add_post(content):
	db = psycopg2.connect(dbname = BASE1)
	c = db.cursor()
	print("Top of add_post executed.")
	c.execute('insert into posts values(null, null;')
	db.commit()
	db.close()
