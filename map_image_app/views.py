from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .authenticate_gee import authenticate_earth_engine
from google.cloud import storage
import ee
import uuid

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
        # Example: Get a Landsat image and clip it to the ROI
        image = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_044034_20140318')  # Example Landsat image
        clipped_image = image.clip(roi)

        # Export the image to Google Cloud Storage
        task_id = f"task-{uuid.uuid4()}"
        task = ee.batch.Export.image.toCloudStorage(
            image=clipped_image,
            description=task_id,
            bucket='your-bucket-name',
            fileNamePrefix=task_id,
            scale=30,
            region=roi.getInfo()['coordinates']
        )
        task.start()

        # Wait for the task to complete
        task_status = task.status()['state']
        while task_status in ['READY', 'RUNNING']:
            task_status = task.status()['state']

        if task_status != 'COMPLETED':
            return Response({'error': f'Task failed with state: {task_status}'}, status=500)

        # Generate a signed URL for the client to download the image
        storage_client = storage.Client()
        bucket = storage_client.bucket('your-bucket-name')
        blob = bucket.blob(f"{task_id}.tif")
        url = blob.generate_signed_url(expiration=3600)  # URL valid for 1 hour

        return Response({'message': 'Coordinates processed successfully', 'url': url})
    except Exception as e:
        return Response({'error': f'Failed to process coordinates: {str(e)}'}, status=500)
