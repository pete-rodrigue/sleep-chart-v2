# sleep-chart-v2
A new and improved version of the sleep chart that pulls data from air table.

I run this on a raspberry pi 4. The show_chart.sh gets run by .bashrc on the pi. Then show_chart.sh waits for the pi to boot up and runs the run.py python file. That run.py file gets my sleep data from an airtable base and saves a .jpeg file with the graph of my sleep data. Then show_chart.sh opens the image in full screen on the pi's display. 

![image](https://github.com/user-attachments/assets/1dae39e8-518d-4ca9-90d3-babf94cf923c)

