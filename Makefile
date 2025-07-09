# "Clean" the DB:
# Adds the 'total_count' and 'positive_count' entries in the database 
# (for all entry.date != today) to the "oldest" entry in the database
# for that ticker
#
# Recommended usage: Having multiple days worth of "scrapes" or "seeds" in the DB
clean:
	python3 main.py clean

# "Seeds" the DB:
# Scrapes for the previous t-6 to t-1 days worth of data and adds in a single entry
# per ticker
#
# Recommended usage: DB is data-less
seed:
	python3 main.py seed

# "Scrapes" comments/posts made today
#
# Recommended usage: Only when there's historical data in the DB
scrape:
	python3 main.py scrape

# "Queries" the data and creates a results.csv file
#
# Recommended usage: After calling "scrape" (need data for t)
query:
	python3 main.py query

# "Displays" the data (top 50 ranked by 'score')
# Can also provide a specific TICKER to see values for (make display TICKER)
#
# Recommended usage: After calling "query" (and only after calling "query")
display:
	python3 main.py display $(filter-out display,$(MAKECMDGOALS))
%:
	@:
