create view wicket_takers as
SELECT *
FROM bowling_stats
WHERE (best_figures LIKE '3%' OR best_figures LIKE '4%' OR best_figures LIKE '5%')
 AND wickets >500 
AND strike_rate > 22
 AND bowledandlbw_percent > 20;


create view eonomy as
select * 
from bowling_stats
where overs > 100 and average <= 23 and economy <= 7.5 order by wickets desc
limit 20;
