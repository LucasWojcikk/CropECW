# Crop ECW With Python

This project was developed in Python to optimize the cropping of an ECW image into multiple pieces using a shapefile of a polygon.


## Technologies Used

-   Python - [Downlaod](https://www.python.org/downloads/)


## Dependencies

- QGIS 3.26.2 - [Download](https://download.osgeo.org/qgis/windows/)
- GDAL 3.5.1
- Geopandas 1.0.1
- os (standard Python library)
- glob (standard Python library)


## How to Run the Project ✅

### 1. Install Prerequisites

First, install Python and QGIS. Currently, I use GDAL through QGIS due to complications encountered when trying to install GDAL separately.

### 2. Folder Structure

Create the following folder structure:

[![](https://mermaid.ink/img/pako:eNp1kO9qwjAUxV-l3M-1JPZPNIPB1DfYPs0MydprW2yakiZsrvjui7aT6VgC4d7zO_cE7gC5LhA4lEZ2VfCyeRBt4M8G-4PVXTCbPY7C01ZAiS0a2ez2uinQCHg742DlSe_eR5F6dRq4wPVvOL_C8V2N8_TsqWSHVzyBuQe1kiWqnXa2c_beEG8x_9jt6wZvctfj139zJ_B_7mS4yYUQFBol68KvaTj7BNgKlY_lviykOQgQ7cn7pLP6-djmwK1xGILRrqyA72XT-851hbS4qaXftbqqnWxftVY_I74FPsAn8DSJUsbmS5aRJGNkyZIQjsBpSqKE-JstKcsoS08hfF0CSLRIsjimjKbpIl4QGp--ARFajDc?type=png)](https://mermaid.live/edit#pako:eNp1kO9qwjAUxV-l3M-1JPZPNIPB1DfYPs0MydprW2yakiZsrvjui7aT6VgC4d7zO_cE7gC5LhA4lEZ2VfCyeRBt4M8G-4PVXTCbPY7C01ZAiS0a2ez2uinQCHg742DlSe_eR5F6dRq4wPVvOL_C8V2N8_TsqWSHVzyBuQe1kiWqnXa2c_beEG8x_9jt6wZvctfj139zJ_B_7mS4yYUQFBol68KvaTj7BNgKlY_lviykOQgQ7cn7pLP6-djmwK1xGILRrqyA72XT-851hbS4qaXftbqqnWxftVY_I74FPsAn8DSJUsbmS5aRJGNkyZIQjsBpSqKE-JstKcsoS08hfF0CSLRIsjimjKbpIl4QGp--ARFajDc)

(This structure above represents a process for cropping two ECW files. If you are cropping only one, you only need to create one subfolder)

### 3. Install Libraries

Open the OSGeo4W Shell and install the necessary libraries:

	- pip install GDAL==3.5.1
	- pip install geopandas==1.0.1

### 4. Run the Code

Navigate to the project directory and run the script:

  Example:
  
	- cd C:\Users\Lucas Wojcik\Documents\GitHub\CropECW
	- python main.py

When prompted, provide the path to the general folder. The code will process the crop and save the images in the `image_output` folder.


## 📌 Important Notes 📌

- The image output format is GeoTIFF, which includes metadata. In my case, I needed to extract the metadata to a separate TFW file for importing into GStarCAD.
- I used LZW compression to reduce the file size by 50%. -
- If you need to keep the ECW format, you can convert from GeoTIFF to ECW using QGIS or Global Mapper. Note that Global Mapper is not free.
- Inside the `shape` folder, you must include the following 8 types of files, which are generally generated automatically when exporting a shapefile:  `file.shp`, `file.cpg`, `file.dbf`, `file.prj`, `file.sbn`, `file.sbx`, `file.shx`, `file.xml`.


## ⚠️ Known Issues

- I encountered some incompatibilities between GDAL and Geopandas, which is why I use specific versions and run the code through OSGeo4W Shell. To resolve these incompatibilities, you would need to compile GDAL locally, but since I already have QGIS installed, I did not explore this option.

## ⏭️ Next Steps
- Implement an interface that utilizes the native file explorer to obtain necessary folder paths for execution.
- Implement a loading screen for the process.
- Error validation.
