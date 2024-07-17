import ee

def authenticate_gee():
    try:
        credentials = ee.ServiceAccountCredentials(
            email='earth-engine-editor@anshu-2002.iam.gserviceaccount.com',
            key_file='C:/Users/Asus/Desktop/map_image_project/Backend/keys/anshu-2002-95bc3e330cec.json'
        )
        ee.Initialize(credentials)
        print("Authentication successful!")
        
        # Try to access a public dataset
        try:
            image = ee.Image('USGS/SRTMGL1_003')
            print(f"Successfully accessed a public dataset.")
            print(f"Image ID: {image.id().getInfo()}")
            print(f"Image Bands: {image.bandNames().getInfo()}")
            print(f"Image Properties: {image.propertyNames().getInfo()}")
        except Exception as e:
            print(f"Error accessing public dataset: {str(e)}")
        
    except Exception as e:
        print(f"Authentication failed: {str(e)}")

if __name__ == '__main__':
    authenticate_gee()