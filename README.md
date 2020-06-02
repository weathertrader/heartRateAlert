
# RaceCast 

Create a live leaderboard from gps streaming 

Inline-style: 
![alt text](example.png "hover text")

## Table of Contents
1. [Installation](README.md#installation)
1. [Preprocessing](README.md#preprocessing)
1. [Streaming](README.md#streaming)
1. [Run Instructions](README.md#Run-instructions)
1. [Scripts](README.md#Scripts)
1. [To do](README.md#To-do)
1. [References](README.md#References)

## Installation

Clone the repo and enter the directory.  

```git clone git@github.com:weathertrader/heartRateAlert.git

cd heartRateAlert
```

Create the python environment and change to it

```conda env create -f environment.yml

conda activate env_gis
```

## Preprocessing 

First download the FitRec dataset `endomondoHR_proper.json` from [this website](https://sites.google.com/eng.ucsd.edu/fitrec-project/home) and move it the `data` directory.
Since the data file is too big to process all at once, we first need to split it up
according the number of cores we wish to stream.  You will need to `cd` into the `data` directory
and `split` the original text file into smaller partitions.

```
cd data
split -l 20000 endomondoHR_proper.json
mv xaa gps_tracks_0.txt 
mv xab gps_tracks_1.txt 
mv xac gps_tracks_2.txt 
mv xad gps_tracks_3.txt 
mv xae gps_tracks_4.txt 
mv xaf gps_tracks_5.txt 
mv xag gps_tracks_6.txt 
mv xah gps_tracks_7.txt 
mv xai gps_tracks_8.txt 
```
Process the data by exectuting the following `bash` script, which in turn will 
call a python script over all of the input files with command line arguments as the input and output data file

```
./src/preprocess.bsh

python src/data_preprocess.py data/gps_tracks_0.txt data/gps_tracks_processed_0.csv
etc ...
```

At this point the data is ordered by timestamp and you can verify with the following command from the cli 
```
head -n 30 gps_tracks_processed_0.csv
```

Now upload these files to S3 using the following command from the cli

```
aws sync command 
```

## Streaming

The data streamer is configured to run on multiple cores simultaneously and the data throughput can be tuned
according to number of cores simultaneously, a delay in starting up each individual core, and a delay on a per-line basis in reading and streaming data
These three command line arguments in order are `n_cores`, `core_delay`, and `line_delay`
From the EC2 cli run one of the following: 

```
python src/produce_stream.py 1 1 0.0

python src/produce_stream.py 8 10 0.001
```

## Run Instructions

Move the example.gpx file into the directory that contains files to process.

`mv example.gpx data/gpx/.`

Process the `gpx` file to geojson


```
python process_all_gpx_to_master.py --dir_gpx=data/gpx --dir_geojson=data/geojson
```

Plot the resulting data in a web browser 

```
python plot_master_geojson.py --dir_geojson=data/geojson
```

## Scripts 

read individual gpx , apply rdp, write to geojson, aggregate all to single with visit counts 
```
process_all_gpx_to_master.py
process_all_gpx_to_master.ipynb
```

plot master geojson tracks and recent individual tracks 
```
plot_master_geojson.py
plot_master_geojson.ipynb

```

## To do 

### Map
1. add junctions 
2. thin points
3. grab tracks via API instead of manually 
4. Fix the master geojson colormap so that saturation occurs at 10 
5. Add RAWS stations

### Track processing
- redo rdp algorithm on individual gpx  
- remove stopped data using speed_min 

## References 
https://github.com/remisalmon/Strava-to-GeoJSON/blob/master/strava_geojson.py
https://github.com/fhirschmann/rdp/blob/master/rdp/__init__.py
https://github.com/sebleier/RDP/blob/master/__init__.py




