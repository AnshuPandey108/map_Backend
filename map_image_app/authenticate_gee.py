import ee

def authenticate_earth_engine():
    try:
        credentials = ee.ServiceAccountCredentials(
            email='earth-engine-editor@anshu-2002.iam.gserviceaccount.com',
            key_file='C:/Users/Asus/Desktop/map_image_project/Backend/keys/anshu-2002-95bc3e330cec.json'
        )
        ee.Initialize(credentials)
        print("Authentication successful!")
    except ee.EEException as e:
        print(f"Authentication failed: {str(e)}")
