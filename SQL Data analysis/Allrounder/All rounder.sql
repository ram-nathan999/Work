

SELECT a.matches, a.batsman, a.runs, a.strike_rate, a.average,
 b.overs, b.wickets, b.economy, a.boundary_percent
FROM batting_stats AS a
JOIN bowling_stats AS b ON a.batsman = b.bowler
WHERE a.runs > 500 AND a.strike_rate > 125 AND b.wickets >
150 AND a.boundary_percent > 15
ORDER BY a.runs DESC 
LIMIT 20;


create view bowling_allrounder as
SELECT a.matches, a.bowler, a.wickets,a.economy,a.strike_rate, a.average,
 b.runs, b.average, b.strike_rate
FROM bowling_stats AS a
JOIN batting_stats AS b ON a.bowler=b.batsman
WHERE b.runs > 500 AND b.strike_rate > 100 and a.wickets>300 and a.economy < 8 and a.average < 30
ORDER BY a.wickets DESC
limit 20
