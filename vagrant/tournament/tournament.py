#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

"""To Do:
todo: do a self join with left side mandatory (Left join?)
ASSUME: client will run the SQL before the Python.  You must too. 
 """

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # I plan to use this within the other routines
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = connect()
    c = db.cursor()
    QUERY = 'delete from games;'
    c.execute( QUERY )
    db.commit()
    db.close()
    """Remove all the match records from the database."""


def deletePlayers():
    db = connect()
    print("Here we are, trying to delete players.")
    c = db.cursor()
    QUERY = 'delete from players;'
    c.execute( QUERY )
    db.commit()
    db.close()
    """Remove all the player records from the database."""


def countPlayers():
    handleBarMoustache = connect()
    swearer = handleBarMoustache.cursor()
    QUERY = 'select count(*) from players;'
    swearer.execute( QUERY )
    x = swearer.fetchall()
    handleBarMoustache.close()
    return  int(x[0][0])  

    """Returns the number of players currently registered."""


def registerPlayer(name):
    # TO DO TO DO
    # SERIAL NUMBER needs resettability: 
    # 1, 2, 3, 19, 20 , 21.   Huh!?
   HAN_SOLO = connect() 
   c = HAN_SOLO.cursor()
   QUERY = "insert into players (name) values ('"+ name +"' );"
   c.execute( QUERY )
   HAN_SOLO.commit()
   HAN_SOLO.close()

   """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    h = connect()
    c = h.cursor()
    QUERY = """
        select playerid, count(*) as wins from games where success= 'true'  group by playerid order by wins desc;
     """
    c.execute( QUERY )
    theStuff = c.fetchall()
    return theStuff
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    h = connect()
    c = h.cursor()

    c.execute("""
        INSERT INTO games (playerID, success)
        VALUES (%s, %s);
        """,
        (loser , 'n'))
    c.execute("""
        INSERT INTO games (playerID, success)
        VALUES (%s, %s);
        """,
        (winner, 'y'))
    h.commit()
    h.close()
    return
 
 
def swissPairings():

    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

print( "Let's start! ")
print("ASSUME: client will run the SQL before the Python.  You must too. ")

deleteMatches()
deletePlayers()
print( 'After deleting there are ' , countPlayers() , ' players!') 
registerPlayer("Sealtest Milk")
registerPlayer("Sparty")
registerPlayer("Buckminster Fuller")
registerPlayer("Vishnubotla")
registerPlayer("Larry Ross III")
registerPlayer("Pinto")
print( 'After registering there are ' , countPlayers() , ' players!') 
reportMatch(3,2)
reportMatch(3,4)
reportMatch(6,5)
reportMatch(3,4)
reportMatch(1,2)
reportMatch(6,5)
reportMatch(3,2)
reportMatch(3,4)
reportMatch(1,5)
reportMatch(3,4)

print( "Player standings has: ") 
print( playerStandings() )
print( "That was fun.")
