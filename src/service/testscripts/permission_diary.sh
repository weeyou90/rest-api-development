echo "Sending invalid post inputs:"

curl localhost:8080/diary/permissions -X POST -H "Content-Type: application/json" -d '{"token":"2"}'

echo "\n\nSending correct post inputs:"

curl localhost:8080/diary/permissions -X POST -H "Content-Type: application/json" -d '{"token":"6bf00d02-dffc-4849-a635-a21b08500d61", "id": 2, "public": true}'

echo "\n"
