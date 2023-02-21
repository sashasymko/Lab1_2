"""
Project for lab1_2
"""
import argparse
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from geopy.distance import geodesic
import pandas as pd
import re


def read_and_analyze_file(path) -> dict:
    """
    :param path_to_dataset: path to data
    :return: df with needed info
    Retuns dataframe with clean data.
    >>> len(read_and_analyze_file('locations.list'))
    10000
    """
    data = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line[0] == '"':
                components = line.strip().split('\t')
                components = [i for i in components if i != '']
                if "{" in components[0] or '}' in components[0]:
                    delete_brackets = re.sub(r'\{.*\}', '', components[0]).strip(' "')
                    components[0] = delete_brackets
                movie_name = components[0].split(' (')[0].strip('"')
                year = components[0].split(' (')[1].strip(')')
                new_list = [movie_name, year, components[1]]
                data.append(new_list)
    df = pd.DataFrame(data, columns=["Movie", "Year", "Place of Filming"])
    df = df.iloc[:10000]
    return df


def calculating_the_distances(df, year, lat, long):
    """
    Calculating the distances between points in the dataframe locations.
    >>> len(calculating_the_distances(read_and_analyze_file("locations.list"), '1960', '49.83826', '24.02324'))
    19
    """
    geo_loc = Nominatim(user_agent='distances', timeout=5)
    list_of_cords = []
    mask = df['Year'] == year
    df_year = df[mask]
    for value in df_year['Place of Filming']:
        try:
            location = geo_loc.geocode(value)
            list_of_cords.append([location.latitude, location.longitude])
        except AttributeError:
            continue
    given_coordinates = [lat, long]
    df_year = df_year.iloc[:len(list_of_cords)]
    distances = []
    for elem in list_of_cords:
        distance = geodesic(tuple(given_coordinates),
                            tuple(elem)).km
        distances.append(distance)
    df_year["coordinates"] = list_of_cords
    df_year["distance_from_point"] = distances
    return df_year


def create_map(df, lat, long):
    """
    Creating a map with unique features.
    """
    map = folium.Map(tiles="Stamen Terrain", location=[lat, long], zoom_start=15)
    feature_group = folium.FeatureGroup(name="Close films")
    for index, row in df.iterrows():
        latitude = row['coordinates'][0]
        longitude = row['coordinates'][1]
        feature_group.add_child(folium.Marker(location=[latitude, longitude], popup=row['Place of Filming'],
                                              icon=folium.Icon(icon='needed_film', color="green")))
    map.add_child(feature_group)
    plugins.ScrollZoomToggler().add_to(map)
    feature_group_2 = folium.FeatureGroup(name="Starting location")
    feature_group_2.add_child(folium.Marker(location=[lat, long], popup="Current location",
                                            icon=folium.Icon(color="cadetblue", icon='blue')))
    map.add_child(feature_group_2)
    plugins.Fullscreen(position="topright").add_to(map)
    mini_map = plugins.MiniMap(toggle_display=True)
    map.add_child(mini_map)
    map.add_child(folium.LayerControl())
    map.save('map.html')


def main_function():
    """
    The main fuction to push everything.
    Creates HTML-file.
    """
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('year', type=str, help='The year')
    parser.add_argument('latitude', type=str, help='The latitude')
    parser.add_argument('longitude', type=str, help='The longitude')
    parser.add_argument('dataset', type=str, help='The path to a file')
    args = parser.parse_args()
    first_df = read_and_analyze_file(args.dataset)
    second_df = calculating_the_distances(first_df, args.year, args.latitude, args.longitude)
    create_map(second_df, args.latitude, args.longitude)

main_function()