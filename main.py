import os
import glob
import geopandas as gpd
from osgeo import gdal, osr

# Here the program asks for the general folder where the files are located.
# You can keep it fixed in the code or leave the input function to request every time it runs.
# general_folder_path = r'D:\ecw\example'
general_folder_path = input("Type the path of the general folder: ")

# Listing all folders within the directory
folder_list = os.listdir(general_folder_path)

# A loop that iterates through the found folders, creating variables named after the folders,
# including the shapefiles folder, output folder and the ECW file.
for folder in folder_list:
    folder_path = os.path.join(general_folder_path, folder)
    shape_path = os.path.join(folder_path, 'shape')
    output_folder = os.path.join(folder_path, 'image_output')
    ecw_file = glob.glob(os.path.join(folder_path, '*.ecw'))[0]

    print(f'CURRENT FOLDER: {folder_path} - ECW: {ecw_file}')

    # From the shapefiles folder path, it lists all the .shp files within the folder.
    shape_list = glob.glob(os.path.join(shape_path, '*.shp'))

    # Iterates over each .shp file found.
    for index, shp_file in enumerate(shape_list, start=1):

        # Load the shapefile.
        gdf = gpd.read_file(shp_file)

        # Initialize variables to store the extreme coordinates.
        x_min, y_min, x_max, y_max = float('inf'), float('inf'), float('-inf'), float('-inf')

        # Iterate over the polygons to obtain the coordinates.
        for _, row in gdf.iterrows():
            if row['geometry'].geom_type == 'Polygon':
                bounds = row['geometry'].bounds
                x_min = min(x_min, bounds[0])
                y_min = min(y_min, bounds[1])
                x_max = max(x_max, bounds[2])
                y_max = max(y_max, bounds[3])

        # Show the coordinates
        # print(f"Coordenadas mínimas: ({x_min}, {y_min})")
        # print(f"Coordenadas máximas: ({x_max}, {y_max})")

        # Check if the ECW file exists.
        if not os.path.exists(ecw_file):
            print(f"ECW file not found: {shp_file}")
            break

        # With GDAL, open the ECW to get its dimensions and set the correct projection.
        ds = gdal.Open(ecw_file)
        if ds is None:
            print(f'Error to open ECW: {ecw_file}')
            break

        # Define srs (EPSG:31982)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(31982)
        ds.SetProjection(srs.ExportToWkt())

        # Calculates cropping window, transforming geospatial coordinates into pixel coordinates
        x_min_pixel = int((x_min - ds.GetGeoTransform()[0]) / ds.GetGeoTransform()[1])
        x_max_pixel = int((x_max - ds.GetGeoTransform()[0]) / ds.GetGeoTransform()[1])
        y_min_pixel = int((y_max - ds.GetGeoTransform()[3]) / ds.GetGeoTransform()[5])
        y_max_pixel = int((y_min - ds.GetGeoTransform()[3]) / ds.GetGeoTransform()[5])

        # Name of the output image (The program saves both the TIFF file and its corresponding TFW file for the image,
        # as some software requires the TFW file).
        output_name = f"IMG_{index}"
        output_tif = os.path.join(output_folder, f"{output_name}.tif")
        output_tfw = os.path.join(output_folder, f"{output_name}.tfw")

        # Crops the image based on the shape coordinates
        # The LZW specification was used to make the TIF file lighter
        gdal.Translate(output_tif, ecw_file,
                       srcWin=[x_min_pixel, y_min_pixel, x_max_pixel - x_min_pixel, y_max_pixel - y_min_pixel],
                       format='GTiff', creationOptions=['COMPRESS=LZW'])

        print(f"Image cropped and saved as: {output_tif}")

        # Generate the TFW file with data of cropped image
        pixel_width = ds.GetGeoTransform()[1]
        pixel_height = abs(ds.GetGeoTransform()[5])
        upper_left_x = x_min
        upper_left_y = y_max

        tfw_contents = f"{pixel_width:.16f}\n0.0\n0.0\n{-pixel_height:.16f}\n{upper_left_x:.16f}\n{upper_left_y:.16f}"
        with open(output_tfw, 'w') as tfw_file:
            tfw_file.write(tfw_contents)

        print(f"TFW file saved as: {output_tfw}")