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
    QUERY_W = """
    CREATE VIEW w AS                                                                                 
    SELECT matches.winner_id, count(*)::smallint as wins
    FROM matches GROUP BY winner_id;
    """
    QUERY_L = """
        CREATE VIEW l AS                                                                            
        SELECT matches.loser_id, count(*)::smallint as losses
        FROM matches GROUP BY loser_id;
    """
    QUERY_PW = """
        CREATE VIEW pw AS 
        SELECT players.name, players.player_id, W.wins 
        FROM players LEFT JOIN W 
        ON players.player_id = W.winner_id;
    """
    QUERY_PWL = """
        CREATE VIEW pwl AS 
        SELECT PW.name, PW.player_id, PW.wins, L.losses 
        FROM PW LEFT JOIN L 
        ON PW.player_id = L.loser_id;   
    """
    QUERY_PWL2 = """
        CREATE VIEW pwl2 AS 
        SELECT name, player_id, 
        CASE 
            WHEN wins ISNULL
                THEN 0
            ELSE
                wins END,
        CASE 
            WHEN losses ISNULL
                THEN 0
            ELSE
                losses END
        FROM PWL;  
    """
    QUERY_S = """
        CREATE VIEW s AS 
        SELECT player_id, wins + losses AS STARTS 
        FROM pwl2; 
    """
    QUERY_INWM = """
        SELECT pwl2.player_id,
        pwl2.name, pwl2.wins,
        s.starts 
        FROM pwl2 JOIN s 
        ON pwl2.player_id =s.player_id;
    """

    c.execute(QUERY_W)
    c.execute(QUERY_L)
    c.execute(QUERY_PW)
    c.execute(QUERY_PWL)
    c.execute(QUERY_PWL2)
    c.execute(QUERY_S)
    c.execute(QUERY_INWM)
    theStuff = c.fetchall() #c.fetchall()
    h.rollback()
    h.close()
    return theStuff
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the plyer's unique id (assigned by the database)
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
    #check for presence of prerequisite VIEWS
    try:
        c.execute("SELECT * FROM pwl2;") # arbitrary view call
    except:
        playerStandings() # creates views if not already present
        h = connect() # subtle bug! function PLAYERSTANDINGS exits by closing handle
        c = h.cursor() # creates a cursor for the QUERY's below
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


reportMatch(1,2)
reportMatch(3,4)
reportMatch(1,3)
reportMatch(2,4)


print( "Player standings has: ") 
print( playerStandings() )
print( "The first mystery L is: ") 
listOfTuples = playerStandings()
print( listOfTuples[0][0], listOfTuples[0][2], listOfTuples[0][3])
print("Fixed?")
print( listOfTuples[0][0], int(listOfTuples[0][2]), str(listOfTuples[0][3]) ) 

print( "Swiss pairings has: ") 
# print( swissPairings() )
print( "That was fun.")
