seed:
	python3 main.py seed

scrape:
	python3 main.py scrape

query:
	python3 main.py query

display:
	python3 main.py display $(filter-out display,$(MAKECMDGOALS))

%:
	@:
