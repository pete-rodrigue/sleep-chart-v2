sleep 8
export DISPLAY=":0"
sleep 2
cd ~/Desktop/scripts/sleep_chart
sleep 1
python3 run.py
sleep 2
imvr figure.jpeg -f
