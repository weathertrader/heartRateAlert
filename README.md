
# RaceCast 

Create a live leaderboard from gps streaming 

Inline-style: 
![alt text](example.png "hover text")

## Table of Contents
1. [Installation](README.md#installation)
1. [Preprocessing](README.md#preprocessing)
1. [Run Instructions](README.md#Run-instructions)
1. [Scripts](README.md#Scripts)
1. [To do](README.md#To-do)
1. [References](README.md#References)

## Installation

Clone the repo and enter the dictory.  

Create the python environment and change to it

`conda env create -f environment.yml`

`conda activate env_gis`

## Preprocessing 

First download the FitRec data from [this website](https://sites.google.com/eng.ucsd.edu/fitrec-project/home)

`mv example.gpx data/gpx/.`

Process the `gpx` file to geojson


```
python process_all_gpx_to_master.py --dir_gpx=data/gpx --dir_geojson=data/geojson
```

Plot the resulting data in a web browser 

```
python plot_master_geojson.py --dir_geojson=data/geojson
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




