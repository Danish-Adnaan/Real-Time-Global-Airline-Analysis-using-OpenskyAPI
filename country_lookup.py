import os
import geopandas as gpd
from shapely.geometry import Point

world = gpd.read_file(os.path.join(os.path.dirname(__file__), "countries.geojson"))
world_sindex = world.sindex

def get_country(lat, lon):
    if lat is None or lon is None:
        return None
    point = Point(lon, lat)
    possible_matches_index = list(world_sindex.intersection(point.bounds))
    possible_matches = world.iloc[possible_matches_index]
    for _, row in possible_matches.iterrows():
        if row['geometry'].contains(point):
            return row["name"]
    return None

