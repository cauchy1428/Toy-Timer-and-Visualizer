# Time Tracker and Visualizer
A toy-level timer built with Python.
The project allows you to easily track your study or working time
and visualize it in a calendar heatmap format.

<img src=".\pic\visualize.png"> 

## Features
- Start and stop the timer by running `Tracker.py`
- Track cumulative durations for the current week and month
- Record daily durations throughout the year
- Visualize the recorded data as a calendar heatmap using `Visualizer.py`

## Requirements

Required Python packages:
* pandas
* plotly
* plotly_calplot

You can install these packages using pip:

```sh
pip install pandas plotly plotly_calplot
```

## Usage

1. **Start the Timer:** Run `Recorder.py` for the first time to start timing.
2. **Stop the Timer:** Run `Recorder.py` again to stop timing.
3. **View Statistics:** When stopping the timer, the script prints cumulative durations for the week and month.
4. **Visualize Data:** Run `Visualizer.py` to generate a calendar heatmap showing recorded daily durations.

## How It Works
- If `start_time.json` is not detected, record the start time.
- Otherwise, calculate the time difference and update daily, weekly, and monthly durations. Then delect `start_time.json`.

## Visualization
Visualizer.py` uses `plotly_calplot` to create a heatmap representation of daily recorded times.

## Project Structure
```
.
├── Tracker.py
├── Visualizer.py
├── data/
│   ├── start_time.json # 
│   ├── date_time_.json
│   ├── monthly_weekly_total.json
├── README.md
```

Please delete the `data` folder before using this project - it's
just my test data in there.

## Known Issues
When visualizing a calendar heatmap using `plotly_calplot`,
in order to maintain a complete rectangular shape for the heatmap,
the package includes some dates from the previous year before the start of each year
and some dates from the following year after the end of each year.
Hovering the mouse over these dates display strange things.

<img src=".\pic\bug.png"> 

Don't try to run this across time zones - who knows what might happen:D

## Author's Words
I'd be very happy if this project helps you.

Please feel free to contact me at: <ynhan@zju.edu.cn>