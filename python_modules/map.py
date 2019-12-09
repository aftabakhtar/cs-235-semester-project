"""
This module will handle tasks related to the creation and processing of
google maps object creation.

Still underconstruction.
"""

#imports
import gmplot
import os

def drawMarkers(latitude_list, longitude_list, city, country):
    """
    latitude_list - list: [lat_1, lat_2, lat_3, ...]
    longitude_list - list: [long_1, long_2, long_3, ...]

    """
    location =  city + ", " + country

    gmap = gmplot.GoogleMapPlotter.from_geocode(location)
    gmap.draw(os.getcwd())
    print(os.getcwd())
