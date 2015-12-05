-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

DROP TABLE IF EXISTS players CASCADE;

DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE players (playerid SERIAL PRIMARY KEY, name TEXT);

CREATE TABLE matches (matchid SERIAL, 
	winner int references players(playerid), loser int references players(playerid));

CREATE VIEW win_num 
as SELECT players.playerid, players.name, 
CASE WHEN count(matches.winner) is NULL 
	THEN 0 ELSE count(matches.winner) END as wnum 
FROM matches right join players on matches.winner = players.playerid 
group by players.playerid ORDER BY wnum DESC;

CREATE VIEW wins 
as SELECT players.playerid, 
	CASE WHEN count(matches.winner) is NULL THEN 0 ELSE count(matches.winner) END as wnum 
FROM matches right join players on matches.winner = players.playerid 
group by players.playerid;

CREATE VIEW loses 
as SELECT players.playerid, 
	CASE WHEN count(matches.loser) is NULL THEN 0 ELSE count(matches.loser) END as lnum 
FROM matches right join players on matches.loser = players.playerid 
group by players.playerid;
