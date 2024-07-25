create view Anchor_batsmen as 
select *
from batting_stats
where runs > 5000 and average >30 and strike_rate > 120 
order by runs desc
limit 15;


create view aggresive as 
select * 
from batting_stats
where runs > 3000 and average > 20 and strike_rate > 130 and
boundary_percentage >= 15
order by runs desc
limit 15;


create view mid as 
select * 
from batting_stats
where runs > 5000 and average > 20 and running_percentage >= 45
order by average desc
limit 20;


create view finisher as 
select *
from batting_stats
where runs > 5000 and strike_rate > 130 and boundary_percent >= 15 order by boundaries desc
