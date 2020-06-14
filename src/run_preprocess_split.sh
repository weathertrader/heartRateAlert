#!/bin/bash
#

echo $PWD
echo "split files begin"
split -l 1000 data/endomondoHR_proper.json

i = 0
echo "split files done"

for entry in x*
do
  ((i=i+1))
  if ((i < 10)); then
    file_name="data/gps_tracks_subset_by_activity_00${i}.txt"
  elif ((i >=10 && i < 100)); then
    file_name="data/gps_tracks_subset_by_activity_0${i}.txt"
  else
    file_name="data/gps_tracks_subset_by_activity_${i}.txt"
  fi
  mv "$entry" "$file_name"
done

echo "rename files done"
