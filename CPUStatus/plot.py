#!/usr/bin/python3

from subprocess import Popen, PIPE
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline
import re
import time
from time import gmtime, strftime
import math
from signal import signal, SIGINT


def onInt(signal_received, frame):
    print("Shutting down...")
    WritePlots()
    exit(0)

times = []
temperatures = None
frequences = None
filename = None


def Init():
    global temperatures
    global frequences
    global filename

    out, err = Popen("./script.sh", shell=True, stdout=PIPE).communicate()
    out = out.decode().split('Frequency:')

    temp = re.findall(r'Core \d{1,}: .*°C ', out[0])
    freq = re.findall(r'[\d\.]{1,} [GM]', out[1])

    temperatures = [[] for _ in range(len(temp))]
    frequences = [[] for _ in range(len(freq))]
    filename = strftime("%Y-%m-%d %H:%M:%S", gmtime())


def WritePlot(x, ylist, namelist, label):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for i in range(len(ylist)):
        fig.add_scatter(secondary_y=True, x=x, y=ylist[i],
                    marker_color='rgb(%d, %d, %d)' % (abs(math.sin(i*math.pi/5)) * 255, abs(math.cos(i*math.pi/9)) * 255, (i*33)%255), name=namelist[i])

    
    fig.update_layout(
        legend=go.layout.Legend(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=20,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )

    fig.update_layout(
        title=go.layout.Title(
            text=label,
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Time",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text=label,
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )
            )
        )
    )
    plotly.offline.plot(fig, filename=filename+label+".html", auto_open=False)


def WritePlots():
    WritePlot(times, temperatures, range(len(temperatures)), "Temperature")
    WritePlot(times, frequences, range(len(frequences)), "Frequency")



signal(SIGINT, onInt)
Init()

if len(temperatures)  is 0 or len(frequences) is 0:
    print("Failed to detect cpu")
    exit(0)

cnt = 1
while True:
    if len(temperatures[0]) > 100000:
        print("Creting new file")
        Init()

    out, err = Popen("./script.sh", shell=True, stdout=PIPE).communicate()
    times.append(strftime("%H:%M:%S", gmtime()))
    out = out.decode().split('Frequency:')

    temp = re.findall(r'Core \d{1,}: .*°C ', out[0])
    freq = re.findall(r'[\d\.]{1,} [GM]', out[1])

    for i in range(len(temp)):
        temperatures[i].append(float((re.search(r'\+[\d\.]{1,}', temp[i]))[0]))

    for i in range(len(freq)):
        ghz = re.search(r'G', freq[i])
        cpu_freq = float(re.search(r'[\d\.]{1,} ', freq[i])[0])
        if ghz is not None:
            cpu_freq *= 1000
        frequences[i].append(cpu_freq)
    WritePlots() if (cnt%13) is 0 else None
    cnt += 1
    time.sleep(2)

