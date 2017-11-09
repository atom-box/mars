-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- Evan Genest  November 8, 2017
-- Udacity: "Intro to Relational Databases"


create database ashe;

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


