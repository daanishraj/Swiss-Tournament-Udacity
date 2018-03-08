-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;
create database tournament;
\c tournament;

drop view if exists standings;
drop view if exists wins_table;
drop view if exists losses_table;
drop table if exists players;
drop table if exists matches;


create table players(player_id serial, player_name text);
create table matches(match_id serial, winner_id int, loser_id int);	

--create the views we need
create view wins_table as
	select player_id, player_name, count(winner_id) as num_wins
	from players left join matches
	on player_id = winner_id
	group by player_id, player_name;


create view losses_table as
	select player_id, player_name, count(loser_id) as num_losses
	from players left join matches
	on players.player_id = matches.loser_id
	group by player_id, player_name;

--create view standings
create view standings as
select wins_table.player_id, wins_table.player_name, wins_table.num_wins, (wins_table.num_wins + losses_table.num_losses) as num_matches
from wins_table, losses_table
where wins_table.player_id = losses_table.player_id
order by wins_table.num_wins desc


