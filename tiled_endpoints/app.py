
# import OS module
import os
import json

import glob
 
# Get the list of all files and directories
path = "/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/tiled_endpoints/tiled"
dir_list = os.listdir(path)

path1 = 'tiled_endpoints/tiled'

file_list = []

for path1, folders, files in os.walk(path1):
    for file in files:
        file_list.append(os.path.join(path1, file))

for filename in file_list:
    print(filename)

dictionary ={
    "Providers": {
        "SQLite": {
            "path": "../input_database/gcbm_input.db",
            "type": "SQLite"
        },
        "RasterTiled": {
            "layers": [
                dir_list
                # {
                #     "name": "disturbances_2012",
                #     "layer_path": "../layers/tiled/disturbances_2012_moja.tiff",
                #     "layer_prefix": "disturbances_2012_moja"
                # },
                # {
                #     "name": "disturbances_2011",
                #     "layer_path": "../layers/tiled/disturbances_2011_moja.tiff",
                #     "layer_prefix": "disturbances_2011_moja"
                # },
                # {
                #     "name": "disturbances_2015",
                #     "layer_path": "../layers/tiled/disturbances_2015_moja.tiff",
                #     "layer_prefix": "disturbances_2015_moja"
                # },
                # {
                #     "name": "disturbances_2014",
                #     "layer_path": "../layers/tiled/disturbances_2014_moja.tiff",
                #     "layer_prefix": "disturbances_2014_moja"
                # },
                # {
                #     "name": "disturbances_2018",
                #     "layer_path": "../layers/tiled/disturbances_2018_moja.tiff",
                #     "layer_prefix": "disturbances_2018_moja"
                # },
                # {
                #     "name": "disturbances_2016",
                #     "layer_path": "../layers/tiled/disturbances_2016_moja.tiff",
                #     "layer_prefix": "disturbances_2016_moja"
                # },
                # {
                #     "name": "Classifier2",
                #     "layer_path": "../layers/tiled/Classifier2_moja.tiff",
                #     "layer_prefix": "Classifier2_moja"
                # },
                # {
                #     "name": "initial_age",
                #     "layer_path": "../layers/tiled/initial_age_moja.tiff",
                #     "layer_prefix": "initial_age_moja"
                # },
                # {
                #     "name": "mean_annual_temperature",
                #     "layer_path": "../layers/tiled/mean_annual_temperature_moja.tiff",
                #     "layer_prefix": "mean_annual_temperature_moja"
                # },
                # {
                #     "name": "Classifier1",
                #     "layer_path": "../layers/tiled/Classifier1_moja.tiff",
                #     "layer_prefix": "Classifier1_moja"
                # },
                # {
                #     "name": "disturbances_2013",
                #     "layer_path": "../layers/tiled/disturbances_2013_moja.tiff",
                #     "layer_prefix": "disturbances_2013_moja"
                # }
            ],
            "blockLonSize": 0.1,
            "tileLatSize": 1.0,
            "tileLonSize": 1.0,
            "cellLatSize": 0.00025,
            "cellLonSize": 0.00025,
            "blockLatSize": 0.1,
            "type": "RasterTiledGDAL",
            "library": "moja.modules.gdal"
        }
    }
}

json_object = json.dumps(dictionary, indent = 4)

with open("provider_config.json", "w") as outfile:
     outfile.write(json_object)

 
# prints all files
# print(dir_list)