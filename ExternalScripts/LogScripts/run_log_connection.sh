python3 -c "import requests"> /dev/null 2>&1
if [ $? -eq 1 ]
then
	pip3 install requests
fi

python3 ./FurhatLogConnection.py $1
