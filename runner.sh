python3 -m venv ./.venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Starting Autobrew"
if [ $1 == "uat" ]
then
        nohup python3 -u ./main.py "uat" > brew.log &
        echo "running UAT"
else
        nohup python3 -u ./main.py > brew.log &
        echo "running prod"
fi
echo "Autobrew started"
