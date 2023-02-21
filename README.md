Name: Filming locations

The aim: to get the HTML map that will show the location where the movies were shot.

In this module such libraries were used:
- argparse;
- from geopy.geocoders (Nominatim);
- folium (plugins);
- geopy.distance (geodesic);
- pandas;
- re.

 There are 4 functions:
 
     1) read_and_analyze_file: this function reads the file and returns dataframe with clean data;
     2) alculating_the_distances: this function calculates the distance between points in the dataframe locations.
     3) create_map: this function creates the map with the unique features using folium library(additionally: MiniMap, Fullscreen, LayerControl)
     4) main_function: using argparse library fo the module`s work.

Launching (from command line):

    >>> python task2.py 2000 49.83826 24.02324 locations.list
    
Output:

HTML map with the unique features that shows the locations of the films.

![image](https://user-images.githubusercontent.com/92580268/153600019-241fc20a-946f-4e1e-aef2-b42f13177c58.png)

 
 




