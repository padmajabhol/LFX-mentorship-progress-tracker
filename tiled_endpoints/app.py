# import OS module
import os
import json

import glob
 
# Get the list of all files and directories
path = "/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/tiled_endpoints/tiled"
dir_list = os.listdir(path)

# path1 = 'tiled_endpoints/tiled'

# file_list = []

p = dir_list

k = [w[:-5] for w in dir_list]

dictionary ={
    "Providers": {
        "SQLite": {
            "path": "../input_database/gcbm_input.db",
            "type": "SQLite"
        },
        "RasterTiled": {
            "layers": [
    
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

lst = []
for ob in p:
    d = dict()
    d["name"] = ob[:-10] 
    d["layer_path"] = "../layers/tiled/" + ob
    # for x in [w[:-5] for w in p]:
    d["layer_prefix"] = ob[:-5]

    lst.append(d)
    # print(d)
dictionary["layers"] = lst 
# print(dictionary)

json_object = json.dumps(dictionary, indent = 4)

with open("provider_config.json", "w") as outfile:
     outfile.write(json_object)
