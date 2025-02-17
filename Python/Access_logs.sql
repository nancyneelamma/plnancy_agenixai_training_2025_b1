CREATE TABLE access_logs(
	id SERIAL PRIMARY KEY,	
	ip_address VARCHAR(20) NOT NULL,
	date_time TIMESTAMP NOT NULL,
	http_method VARCHAR(10),
	url_path TEXT,
	status_code INT,
	referer TEXT,
	user_agent TEXT,
	browser TEXT,
	os TEXT
);
