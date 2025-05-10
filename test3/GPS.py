from machine import UART, Pin
from utime import sleep
import math, random

# UART Setup for GPS
uart = UART(0, 9600)
uart.init(9600, bits=8, parity=None, stop=1, rx=1, tx=0)


def convert_to_decimal(coord, direction):
    degrees = int(coord / 100)
    minutes = coord - (degrees * 100)
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def gps_to_xy(lat, lon, ref_lat=0, ref_lon=0):
    """
    Convert GPS coordinates (latitude, longitude) to XY coordinates
    using a simple equirectangular projection.
    
    Args:
        lat (float): Latitude in degrees
        lon (float): Longitude in degrees
        ref_lat (float): Reference latitude (origin) in degrees
        ref_lon (float): Reference longitude (origin) in degrees
        
    Returns:
        tuple: (x, y) coordinates in meters from the reference point
    """
    # Earth radius in meters
    EARTH_RADIUS = 6371000
    
    # Convert degrees to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    ref_lat_rad = math.radians(ref_lat)
    ref_lon_rad = math.radians(ref_lon)
    
    # Calculate the x coordinate (longitude)
    x = EARTH_RADIUS * (lon_rad - ref_lon_rad) * math.cos((lat_rad + ref_lat_rad) / 2)
    
    # Calculate the y coordinate (latitude)
    y = EARTH_RADIUS * (lat_rad - ref_lat_rad)
    
    return (x, y)

def xy_to_gps(x, y, ref_lat=0, ref_lon=0):
    """
    Convert XY coordinates back to GPS coordinates (latitude, longitude)
    
    Args:
        x (float): X coordinate in meters
        y (float): Y coordinate in meters
        ref_lat (float): Reference latitude (origin) in degrees
        ref_lon (float): Reference longitude (origin) in degrees
        
    Returns:
        tuple: (latitude, longitude) in degrees
    """
    # Earth radius in meters
    EARTH_RADIUS = 6371000
    
    # Convert reference point to radians
    ref_lat_rad = math.radians(ref_lat)
    ref_lon_rad = math.radians(ref_lon)
    
    # Calculate latitude
    lat_rad = y / EARTH_RADIUS + ref_lat_rad
    
    # Calculate longitude
    lon_rad = x / (EARTH_RADIUS * math.cos((lat_rad + ref_lat_rad) / 2)) + ref_lon_rad
    
    # Convert back to degrees
    lat = math.degrees(lat_rad)
    lon = math.degrees(lon_rad)
    
    return (lat, lon)

def approx_distance(lat1, lon1, lat2, lon2):
    """ this gives an approximate distance (two gps point) and was calculated considering
the polar region.
"""
    lat_scale = 111319.9
    lon_scale = 111319.9 * math.cos(math.radians(lat1))
    dx = (lon2 - lon1) * lon_scale
    dy = (lat2 - lat1) * lat_scale
    return dx, dy, math.sqrt(dx**2 + dy**2)

def read_data():
        x = uart.read()
        if x is not None:
            try:
                x=x.decode("utf-8")
                #print(x)
                value=x.split(",")
                if(value[0]=="$GPRMC" and value[2]=='A'):
                    error=False
                    time=value[1]
                    lat=value[3]
                    lon=value[5]
                    speed=value[7]
                    heading=value[8]
                    lat_dir=value[4]
                    lon_dir=value[6]
                    
                    #Display(spmph)
                    #print(speed,value[2])
                    lat=convert_to_decimal(float(lat),lat_dir)
                    lon=convert_to_decimal(float(lon),lon_dir)
                    return([lat,lon,speed,heading])
            except UnicodeError:
                print('Unicode Error occured')
                return  None


def get_compass_direction_simple(heading_deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(heading_deg / 45) % 8
    return directions[index]


