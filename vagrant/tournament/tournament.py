#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

"""To Do:
ToDo Per Udacity-reviewer-comments (11-18-2017) rewrite to have more normalized database.  Have two tables: players(id, name) and matches(match_id, winner_id, loser_id).  Add primary key to both.    
ToDo Per Udacity-reviewer-comments (11-18-2017) rewrite first four functions.   New tables are players(id, name) and matches(match_id, winner_id, loser_id).  Rewrite erase, addResult, and standings functions. 

 """

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # I plan to use this within the other routines
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    db = connect()
    c = db.cursor()
    QUERY = 'DELETE FROM matches;'
    c.execute( QUERY )
    db.commit()
    db.close()
    """Remove all the match records from the database."""


def deletePlayers():
    db = connect()
    c = db.cursor()
    QUERY = 'DELETE FROM players;'
    c.execute( QUERY )
    db.commit()
    db.close()
    """Remove all the player records from the database."""


def countPlayers():
    handleBarMoustache = connect()
    swearer = handleBarMoustache.cursor()
    QUERY = 'SELECT COUNT(*) FROM players;'
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
   QUERY = "insert into players (name) values (%s);"
   DATA = (name, )
   c.execute( QUERY, DATA )
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
        SELECT player_id, name, wins, starts as matches FROM players ORDER BY wins desc;
    """
    c.execute(QUERY)
 
    theStuff = c.fetchall()
    return theStuff
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of  matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    h = connect()
    c = h.cursor()
    QUERY1 = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);"
    DATA_WINNER = (winner,)
    DATA_LOSER = (loser,)
    c.execute(QUERY1, (DATA_WINNER, DATA_LOSER) )

    h.commit()
    h.close()
    return
 
 
def swissPairings():
    h = connect()
    c = h.cursor()
    QUERY0 = '''
    DROP VIEW IF EXISTS players2, players3;
    '''
    QUERY1 =  '''
        CREATE VIEW players2 AS 
        SELECT playerid, name, wins 
        FROM players ORDER BY wins DESC;
    '''    
    c.execute(QUERY1)



    QUERY2 =  '''
        CREATE VIEW players3 AS 
        SELECT playerid, name, wins, 
        row_number() OVER (ORDER BY wins DESC) 
        AS hay 
        FROM players  ;
    '''
    QUERY3 =  '''
        SELECT a.playerid, a.name, b.playerid, b.name
        FROM players3 as a, players3 AS b 
        WHERE a.hay+1 = b.hay AND (a.hay%2=1);
    '''
    c.execute( QUERY0 )    
    c.execute( QUERY1 )
    c.execute( QUERY2 )
    c.execute( QUERY3 )
    rawAll = c.fetchall()
    return rawAll
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
print("ASSUME: client will run the SQL before the Python.  Syntax: \i tournament.sql from the psql prompt, with db CLOSED. ")
registerPlayer("Bela Abzug")
registerPlayer("Wayne County")
registerPlayer("Warren")
registerPlayer("Shamu")
registerPlayer("123Alien")
registerPlayer("Mork & Mindy")


reportMatch(3,2)
reportMatch(3,4)
reportMatch(6,5)
reportMatch(3,4)
reportMatch(6,2)
reportMatch(6,1)
reportMatch(3,2)
reportMatch(3,1)
reportMatch(3,5)
reportMatch(3,4)

print( "Player standings has: ") 
print( playerStandings() )
print( "Swiss pairings has: ") 
print( swissPairings() )
print( "That was fun.")
