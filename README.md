# Running Tracker
Code to extract, process, plot and save your running data through your workouts

## Getting started
1. To get started you need raw running data. To get it I'm using my Samsung Health app, and "Fitness Syncer" to download the data as a raw csv file. All you really need however is a csv file with your data as you run. The csv should have date, time offset, heartrate, distance and speed columns. As of now the code asumes that the columns are named "Date (US)", "Time Offset", "Distance in Meters", "Heart Rate", "Speed (mps)". Dont worry if your csv has more values, pandas takes care of that. Make sure that all the values are recorded at the sime time offset.
2. Once you have your files you should add them to a folder named "datasets" inside the directory where you want all the data to be processed and saved (It doesn't have to be the same as the one where you download this repo)
3. Clone this repo and change the path file string in "extract.py" so that it points to the directory where you have the "datasets" folder.
4. Run "extract.py". You'll se a bunch of options. If its the first time you run the code select option 1 to process all the data. It should process all your files. If you add more files later you can select option 1 again and it should only process the new files and add them to the json file with all the data.
5. If you want to add VO2Max data (Samsung health calculates it for every run but its not part of the extracted csv) you can run option 2
6. Options 3 and 4 will plot the graphs with your data
