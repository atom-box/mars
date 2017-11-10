-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- Evan Genest  November 8, 2017
-- Udacity: "Intro to Relational Databases"

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS games;

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\dt;
\c template1;
\c tournament;
-- kind of worried about needing or not needing a \c line here

CREATE TABLE games (
	playerID integer,
	round integer,
	game serial
);

CREATE TABLE players (
	name text,
	cumulativePts integer,
	playerID serial	
);

INSERT INTO players values(
	'Nadal', 0
);

INSERT INTO players values(
	'Zidane', 0
);
INSERT INTO players values(
	'Genest-Balfour', 11
);


INSERT INTO players values(
	'Montfils', 0
);
