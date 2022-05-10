import rasterio as rst
from rasterio.plot import show


fp = '/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/miscellaneous/initial_age_moja.tiff'
# z = r'fp'

img = rst.open(fp)

# nodata
print("nodata: ",img.nodata)

# cellLatSize, cellLonSize ---> resolution
t = img.transform
x = t[0]
y = -t[4]
print("cellLatSize: ", x)
print("cellLonSize: ", y)

# blockLatSize, blockLonSize ---> 400 blocks per cell
print("blockLatSize: ", x*400)
print("blockLonSize: ", y*400)

## tileLatSize. tileLonSize ---> 10 tiles per block
print("tileLatSize: ", x*4000)
print("tileLonSize: ", y*4000)


