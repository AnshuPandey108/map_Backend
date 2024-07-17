from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .authenticate_gee import authenticate_earth_engine
import ee  # Import the ee module here

@api_view(['POST'])
def process_coordinates(request):
    # Call the authentication function to initialize Google Earth Engine
    authenticate_earth_engine()

    # Further processing logic here
    data = request.data
    coordinates = data.get('coordinates')
    if not coordinates:
        return Response({'error': 'No coordinates provided'}, status=400)

    north, south, east, west = coordinates['north'], coordinates['south'], coordinates['east'], coordinates['west']
    roi = ee.Geometry.Rectangle([west, south, east, north])  # Use ee.Geometry here

    try:
        # Your Earth Engine processing code here
        # Initialize map, add layers, etc.
        
        return Response({'message': 'Coordinates processed successfully'})
    except Exception as e:
        return Response({'error': f'Failed to process coordinates: {str(e)}'}, status=500)
