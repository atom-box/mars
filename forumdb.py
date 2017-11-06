# "Database code" for the DB Forum.

import datetime, psycopg2
BASE1 = 'forum'


db = psycopg2.connect(dbname = BASE1)
c = db.cursor()
print "Hey", datetime.datetime.now() , " !!!"

# uncommen t to clear:
"""
content = "');  delete from posts; --"
c.execute("insert into posts values('%s')" % content)
db.commit()
"""

db.close()


#"""Return all posts from the 'database', most recent first."""

def get_posts():
	# todo always give the same select.  fetchall or something
	db = psycopg2.connect(dbname = BASE1)
	c = db.cursor()
	print("Top of get_posts executed.")
	c.execute( 'select content, time from posts order by time desc;' )
	multiComments = c.fetchall()
	db.close()
	return multiComments

#"""Add a post to the 'database' with the current timestamp."""
def add_post(content):
	db = psycopg2.connect(dbname = BASE1)
	c = db.cursor()
	c.execute("insert into posts values(%s)", (content,) )
	db.commit()
	db.close()
	print "Exited add post succesfully. "
