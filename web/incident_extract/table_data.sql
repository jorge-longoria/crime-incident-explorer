select 
        report_number,
        crime_type,
        date,
        substring(lpad(time, 4, '0') from 1 for 2) 
        || ':' ||
        substring(lpad(time, 4, '0') from 3 for 2) as time,
        address 
from crime_incidents
where to_char(date, 'yyyy') = '2016' 
  and (crime_type = {0} OR {0} = '')
  and date >= {1}
  and date <= {2} 
order by 
        date, 
        cast(substring(lpad(time, 4, '0') from 1 for 2)  as integer),
        cast(substring(lpad(time, 4, '0') from 3 for 2)  as integer),
        crime_type,
        address
/* Remove limit in production. */
limit 100; 
