build:
	docker build -t capstone-dashboard .

run:
	docker run -p 80:8080 -dit --name dashboard capstone-dashboard