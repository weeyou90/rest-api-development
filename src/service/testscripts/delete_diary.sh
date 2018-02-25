if [ $# -eq 1 ] 
then
	i=$1
else 
	i=1
fi


echo "Sending invalid post inputs:"

curl localhost:8080/diary/delete -X POST -H "Content-Type: application/json" -d '{"token":"abc"}'

echo "\n\nSending correct post inputs:"
echo deleting $i

curl localhost:8080/diary/delete -X POST -H "Content-Type: application/json" -d '{"token":"6bf00d02-dffc-4849-a635-a21b08500d61", "id": '$i'}'

echo "\n"
