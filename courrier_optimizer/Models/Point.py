class Point:
    def __init__(self, name:str, latitude:float, longitude:float):
        self.name = name
        lat = float(latitude)
        lon = float(longitude)
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError(f"Invalid GPS coordinates: latitude={latitude}, longitude={longitude}. Both latitude and longitude must be valid GPS coordinates (latitude between -90 and 90, longitude between -180 and 180).")
        self.latitude = lat
        self.longitude = lon

    def __str__(self):
        return f"Point(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"

