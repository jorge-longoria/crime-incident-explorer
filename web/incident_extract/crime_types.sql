select distinct 
	crime_type 
from crime_incidents 
where to_char(date, 'yyyy') = '2016' 
order by crime_type;
