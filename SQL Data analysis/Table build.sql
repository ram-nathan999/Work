Create table match_runs as
SELECT batsman, match_runs,
 DENSE_RANK() OVER(PARTITION BY batsman ORDER BY match_runs DESC) AS score_rank,
 ROUND(AVG(match_runs)OVER(PARTITION BY batsman),2) AS Avg_score,
 SUM(CASE WHEN match_runs > 50 THEN 1 ELSE 0 END) OVER (PARTITION BY batsman ) AS fifties,  SUM(CASE WHEN match_runs > 100 THEN 1 ELSE 0 END) OVER (PARTITION BY batsman ) AS centuries,
 MAX(match_runs)OVER(PARTITION BY batsman) AS highest_score
FROM (
 SELECT DISTINCT id, batsman, SUM(batsman_runs) AS match_runs
 FROM balls
 GROUP BY id, batsman
 ) AS subquery;


CREATE TABLE batting_stats AS
SELECT
 balls.batsman,
 COUNT(DISTINCT id) AS matches,
 SUM(batsman_runs) AS runs,
 COUNT(ball) AS balls,
 ROUND(CASE WHEN COUNT(ball) > 0 THEN (SUM(batsman_runs) * 100.0 / COUNT(ball)) END,2) AS strike_rate, ROUND(AVG(match_runs.match_runs),2) AS average,
 MAX(match_runs.match_runs) as highest_score,
 SUM(CASE WHEN batsman_runs = 4 OR batsman_runs = 6 THEN 1 ELSE 0 END) AS boundaries,
 ROUND(CASE WHEN SUM(batsman_runs) > 0 THEN ((SUM(CASE WHEN batsman_runs = 1 THEN 1 WHEN batsman_runs = 2 THEN 2 WHEN batsman_runs = 3 THEN 3 ELSE 0 END) * 100.0) / SUM(batsman_runs)) END,2) AS running_percentage FROM
balls
JOIN match_runs
on balls.batsman = match_runs.batsman
GROUP BY
balls.batsman
ORDER BY
runs DESC;

 CREATE TABLE match_figures AS
SELECT bowler,runs,wickets,
 wickets||'-'|| runs as match_figure
 FROM (
 SELECT DISTINCT id, bowler, SUM(total_runs)as runs,SUM(wicket) as wickets
 FROM balls
 GROUP BY id, bowler
 ) AS subquery;

create table bowling_stats as
SELECT
 COUNT(DISTINCT id) AS matches,
 balls.bowler,
 CEIL(COUNT(ball) / 6) AS overs,
 SUM(total_runs) AS runs,
 SUM(wicket) AS wickets,
 MAX(match_figures.match_figure) as best_figures,
 COUNT(match_figures.wickets > 4) as four_wickets,
 COUNT(match_figures.wickets > 5) as five_wickets,
 ROUND(CASE WHEN SUM(wicket) > 0 THEN SUM(total_runs)*1.0/ SUM(wicket) ELSE NULL END,2) AS average,
 ROUND(CASE WHEN SUM(wicket) > 0 THEN COUNT(ball)*1.0/ SUM(wicket) ELSE NULL END,2) AS strike_rate, SUM(CASE WHEN dismissal ='bowled' or dismissal ='lbw' THEN 1 ELSE 0 END) as bowled_lbw,
 SUM(CASE WHEN dismissal ='caught' or dismissal ='caught and bowled' THEN 1 ELSE 0 END) as catch_out FROM
balls
JOIN match_figures
ON balls.bowler=match_figures.bowler
GROUP BY
balls.bowler
ORDER BY
wickets DESC;
