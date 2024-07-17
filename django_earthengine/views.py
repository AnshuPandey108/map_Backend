from rest_framework.decorators import api_view
from rest_framework.response import Response
from .authenticate_gee import authenticate_earth_engine
import ee
import geemap
import os

# Function to initialize Google Earth Engine
def initialize_gee():
    try:
        ee.Initialize()
        print("Google Earth Engine initialized successfully!")
    except ee.EEException as e:
        print("Google Earth Engine initialization failed:", e)

# Initialize Google Earth Engine when the module is loaded
initialize_gee()

@api_view(['POST'])
def process_coordinates(request):
    # Print the path to the Google Application Credentials for debugging
    print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    
    data = request.data
    coordinates = data.get('coordinates')
    
    if not coordinates:
        return Response({'error': 'No coordinates provided'}, status=400)

    north, south, east, west = coordinates['north'], coordinates['south'], coordinates['east'], coordinates['west']
    roi = ee.Geometry.Rectangle([west, south, east, north])

    try:
        # Initialize map centered on the average of provided coordinates
        Map = geemap.Map(center=[(north + south) / 2, (east + west) / 2], zoom=10)
        
        # Add ROI layer
        Map.addLayer(roi, {}, 'Region of Interest')
        
        # Add satellite basemap
        Map.add_basemap('SATELLITE')
        
        # Save map as HTML file
        image_path = os.path.join('static', 'images', 'downloaded_image.html')
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))
        
        Map.to_html(outfile=image_path, title='Downloaded Image')
        
        print("Map saved as HTML successfully!")
        return Response({'image_url': image_path})
    
    except Exception as e:
        print("Error processing coordinates:", e)
        return Response({'error': 'Failed to process coordinates', 'details': str(e)}, status=500)
