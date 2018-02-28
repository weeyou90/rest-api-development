
echo "GET diary\n"
curl localhost:8080/diary

echo "\nPOST diary\n"
curl localhost:8080/diary -X POST -H "Content-Type: application/json" -d '{"token": "6bf00d02-dffc-4849-a635-a21b08500d61"}'

echo "\n"
