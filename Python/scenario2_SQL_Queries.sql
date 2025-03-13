-- Total Number of requests.

select count(*) as no_of_request 
from access_logs;

-- Number of unique IP Addresses.

select Count(Distinct(ip_address)) as unique_ipaddress 
from access_logs;

-- TOP 10 most frequent IP addresses.

select ip_address,count(ip_address) as frequent_ipaddress
from access_logs
group by ip_address
order by frequent_ipaddress desc
limit 10;

-- Top 10 most requested URL paths.

select url_path, count(url_path) as paths
from access_logs
group by url_path
order by paths desc
limit 10;

-- Busiest hour of the day(based on number of requests)

select extract(hour from date_time) as busy_hour,count(*) as no_of_requests
from access_logs
group by busy_hour
order by no_of_requests desc
limit 1;