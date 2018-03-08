#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DBNAME = "tournament"


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	#db = psycopg2.connect(database = DBNAME)
	db = connect()
	c = db.cursor()
	c.execute("delete from matches;")
	db.commit()
	db.close()
	#return posts



def deletePlayers():
	"""Remove all the player records from the database."""
	#db = psycopg2.connect(database=DBNAME)
	db = connect()
	c = db.cursor()
	c.execute("delete from players;")
	db.commit()
	db.close()



def countPlayers():
	"""Returns the number of players currently registered."""
	#db = psycopg2.connect(database=DBNAME)
	db = connect()
	c = db.cursor()
	c.execute("select * from players;")
	result1 = c.fetchall()
	print(result1)
	#print(len(result1))
	#print(type(result1))## this is a list	
	#print(result1)##empty list	
	count = len(result1)
	#print(count)
	#print(count[0])
	db.close()
	return (count)



def registerPlayer(name):
	"""Adds a player to the tournament database.
  
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
  
	Args:
	  name: the player's full name (need not be unique).
	"""
	#db = psycopg2.connect(database=DBNAME)
	db = connect()
	c = db.cursor()
	#param_name = name
	c.execute("INSERT INTO players (player_name) VALUES (%s);", (name,))
	db.commit()
	db.close()



def playerStandings():
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
	#db = psycopg2.connect(database = DBNAME)
	db = connect()
	c = db.cursor()
	c.execute("select * from standings")
	result = c.fetchall()
	#print(result)
	db.close()
	return(result)

def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	db = connect()
	c = db.cursor()
	c.execute("insert into matches(winner_id, loser_id) values(%s,%s)",(winner, loser))
	#c.execute("INSERT INTO players (player_name) VALUES (%s);", (name,))
	db.commit()
	db.close()
 
 
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
	rankings = playerStandings()
	item = 0
	pairings = []
	while item < len(rankings):
		id1 = rankings[item][0]
		name1 = rankings[item][1]
		id2 = rankings[item + 1][0]
		name2 = rankings[item+1][1]
		match_pair = (id1, name1, id2, name2)
		pairings.append(match_pair)
		item += 2

	return (pairings)	

