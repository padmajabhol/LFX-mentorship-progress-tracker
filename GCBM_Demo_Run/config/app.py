# import OS module
import os
#import JSON module
import json
#import glob
import glob
#import rasterio
import rasterio as rst

import pathlib

# folder containing classifiers
path = "/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/classifiers"

# folder containing disturbances
path1 = "/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances"

# folder containing miscellaneous files
path2 = "/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/miscellaneous"

# get list of all files and directories in the specified directory
dir_list = os.listdir(path)
dir_list1 = os.listdir(path1)
dir_list2 = os.listdir(path2)

# config provider

Rasters = []
cellLatSize = []
cellLonSize = []

## find absolute path of all the .tiff files in the classifier, disturbance and misc directory and store them in Rasters list
for root, dirs, files in os.walk(os.path.abspath(path)):
    for file in files:
        fp = os.path.join(root, file)
        Rasters.append(fp)

for root, dirs, files in os.walk(os.path.abspath(path1)):
    for file in files:
        fp1 = os.path.join(root, file)
        Rasters.append(fp1)

for root, dirs, files in os.walk(os.path.abspath(path2)):
    for file in files:
        fp2 = os.path.join(root, file)
        Rasters.append(fp2)

## loop through all the absolute file path stored in Rasters, denoted by nd and perform raster operation to find the resolution of the images(cellLatSize and cellLonSize) and store them all in cellLatSize and CellLonSize lists
    for nd in Rasters:
        img = rst.open(nd)
        t = img.transform
        x = t[0]
        y = -t[4]
        cellLatSize.append(x)
        cellLonSize.append(y)

## verify all the elements in the lists are identical, if that is so, store them in the below variables that shall be passed to the config provider        

result = all(element == cellLatSize[0] for element in cellLatSize)
if (result):
    cellLat = x
    cellLon = y
    blockLat = x*400
    blockLon = y*400
    tileLat = x*4000
    tileLon = y*4000
else:
    print("Corrupt files")

    
dictionary ={
    "Providers": {
        "SQLite": {
            "path": "../input_database/gcbm_input.db",
            "type": "SQLite"
        },
        "RasterTiled": {
            "layers": [

            ],
            "blockLonSize": blockLon,
            "tileLatSize": tileLat,
            "tileLonSize": tileLon,
            "cellLatSize": cellLat,
            "cellLonSize": cellLon,
            "blockLatSize": blockLat,
            "type": "RasterTiledGDAL",
            "library": "moja.modules.gdal"
        }
    }
}


# used a for loop to loop through all the files in a particular folder and sliced the file names as required ---> for disturbance folder

lst = []
for ob in dir_list1:
    d = dict()
    d["name"] = ob[:-10] # slice 10 characters from the end of a string
    d["layer_path"] = "../layers/tiled/" + ob 
    d["layer_prefix"] = ob[:-5]
    # add the list of files in the existing list lst
    lst.append(d)
    # assign the list "lst" to a particular item in the give dictionary
dictionary["Providers"]["RasterTiled"]["layers"] = lst

# repeat the same for classifier folder

for ob in dir_list:
    d = dict()
    d["name"] = ob[:-10] 
    d["layer_path"] = "../layers/tiled/" + ob
    d["layer_prefix"] = ob[:-5]

    lst.append(d)
dictionary["Providers"]["RasterTiled"]["layers"] = lst

# for miscellaneous folder

for ob in dir_list2:
    d = dict()
    d["name"] = ob[:-10] 
    d["layer_path"] = "../layers/tiled/" + ob
    d["layer_prefix"] = ob[:-5]

    lst.append(d)
dictionary["Providers"]["RasterTiled"]["layers"] = lst

json_object = json.dumps(dictionary, indent = 4)

with open("provider_config.json", "w") as outfile:
     outfile.write(json_object)



#modules_cbm.json

dictionary2 = {
    "Modules": {
        "CBMBuildLandUnitModule": {
            "order": 1,
            "library": "moja.modules.cbm"
        },
        "CBMSequencer": {
            "order": 2,
            "library": "moja.modules.cbm"
        },
        "CBMDisturbanceListener": {
            "enabled": True,
            "order": 3,
            "library": "moja.modules.cbm",
            "settings": {
                "vars": [

                ]
            }
        },
        "CBMDisturbanceEventModule": {
            "enabled": True,
            "order": 4,
            "library": "moja.modules.cbm"
        },
        "CBMTransitionRulesModule": {
            "enabled": True,
            "order": 5,
            "library": "moja.modules.cbm"
        },
        "CBMLandClassTransitionModule": {
            "enabled": True,
            "order": 6,
            "library": "moja.modules.cbm"
        },
        "CBMGrowthModule": {
            "enabled": True,
            "order": 7,
            "library": "moja.modules.cbm"
        },
        "CBMDecayModule": {
            "enabled": True,
            "order": 8,
            "library": "moja.modules.cbm",
            "settings": {
                "extra_decay_removals": False
            }
        },
        "CBMAgeIndicators": {
            "enabled": True,
            "order": 9,
            "library": "moja.modules.cbm"
        },
        "TransactionManagerAfterSubmitModule": {
            "order": 10,
            "library": "internal.flint"
        }
    }
}

# repeat the same process that we used to generate the provider_config.json file, though modules_cbm.json only requires disturbance files

lst2 = []
for ob in dir_list1:
    d = dict()
    d = ob[:-10]
    lst2.append(d)
    # print(d)
dictionary2["Modules"]["CBMDisturbanceListener"]["settings"]["vars"] = lst2
# print(dictionary)

json_object2 = json.dumps(dictionary2, indent = 4)

with open("modules_cbm.json", "w") as outfile:
     outfile.write(json_object2)


# the rest of the files mostly contain boiler plate code and hence are easy to handle since they don't depend on the inputs

## localdomain.json

dictionary3 ={
    "Libraries": {
        "moja.modules.cbm": "external",
        "moja.modules.gdal": "external"
    },
    "LocalDomain": {
        "start_date": "2010/01/01",
        "end_date": "2021/01/01",
        "landUnitBuildSuccess": "landUnitBuildSuccess",
        "simulateLandUnit": "simulateLandUnit",
        "sequencer_library": "moja.modules.cbm",
        "sequencer": "CBMSequencer",
        "timing": "annual",
        "type": "spatial_tiled",
        "landscape": {
            "provider": "RasterTiled",
            "num_threads": 4,
            "tiles": [
                {
                    "x": -106,
                    "y": 55,
                    "index": 12674
                }
            ],
            "x_pixels": 4000,
            "y_pixels": 4000,
            "tile_size_x": 1.0,
            "tile_size_y": 1.0
        }
    }
}

json_object3 = json.dumps(dictionary3, indent = 4)

with open("localdomain.json", "w") as outfile:
    outfile.write(json_object3)

## pools_cbm

dictionary4 = {
	"Pools": {
		"AboveGroundFastSoil": 0.0,
        "AboveGroundSlowSoil": 0.0,
        "AboveGroundVeryFastSoil": 0.0,
        "Atmosphere": 0.0,
        "BelowGroundFastSoil": 0.0,
        "BelowGroundSlowSoil": 0.0,
        "BelowGroundVeryFastSoil": 0.0,
        "BlackCarbon": 0.0,
        "CH4": 0.0,
        "CO": 0.0,
        "CO2": 0.0,
        "DissolvedOrganicCarbon": 0.0,
        "HardwoodBranchSnag": 0.0,
        "HardwoodCoarseRoots": 0.0,
        "HardwoodFineRoots": 0.0,
        "HardwoodFoliage": 0.0,
        "HardwoodMerch": 0.0,
        "HardwoodOther": 0.0,
        "HardwoodStemSnag": 0.0,
        "MediumSoil": 0.0,
        "NO2": 0.0,
        "Peat": 0.0,
        "Products": 0.0,
        "SoftwoodBranchSnag": 0.0,
        "SoftwoodCoarseRoots": 0.0,
        "SoftwoodFineRoots": 0.0,
        "SoftwoodFoliage": 0.0,
        "SoftwoodMerch": 0.0,
        "SoftwoodOther": 0.0,
        "SoftwoodStemSnag": 0.0	
    }
}


json_object4 = json.dumps(dictionary4, indent = 4)

with open("pools_cbm.json", "w") as outfile:
    outfile.write(json_object4)

## modules_output

dictionary5 = {
	"Modules": {
        "WriteVariableGeotiff": {
            "enabled": True,
            "order": 11,
            "library": "moja.modules.gdal",
            "settings": {
                "items": [
                    {
                        "data_name": "Age",
                        "enabled": True,
                        "variable_data_type": "Int16",
                        "on_notification": "OutputStep",
                        "variable_name": "age"
                    },
                    {
                        "pool_name": [
                            "SoftwoodMerch",
                            "SoftwoodFoliage",
                            "SoftwoodOther",
                            "HardwoodMerch",
                            "HardwoodFoliage",
                            "HardwoodOther"
                        ],
                        "data_name": "AG_Biomass_C",
                        "enabled": True,
                        "variable_data_type": "float",
                        "on_notification": "OutputStep"
                    },
                    {
                        "pool_name": [
                            "SoftwoodMerch",
                            "SoftwoodFoliage",
                            "SoftwoodOther",
                            "SoftwoodCoarseRoots",
                            "SoftwoodFineRoots",
                            "HardwoodMerch",
                            "HardwoodFoliage",
                            "HardwoodOther",
                            "HardwoodCoarseRoots",
                            "HardwoodFineRoots",
                            "AboveGroundVeryFastSoil",
                            "BelowGroundVeryFastSoil",
                            "AboveGroundFastSoil",
                            "BelowGroundFastSoil",
                            "MediumSoil",
                            "AboveGroundSlowSoil",
                            "BelowGroundSlowSoil",
                            "SoftwoodStemSnag",
                            "SoftwoodBranchSnag",
                            "HardwoodStemSnag",
                            "HardwoodBranchSnag"
                        ],
                        "data_name": "Total_Ecosystem_C",
                        "enabled": True,
                        "variable_data_type": "float",
                        "on_notification": "OutputStep"
                    },
                    {
                        "pool_name": [
                            "SoftwoodMerch",
                            "SoftwoodFoliage",
                            "SoftwoodOther",
                            "SoftwoodCoarseRoots",
                            "SoftwoodFineRoots",
                            "HardwoodMerch",
                            "HardwoodFoliage",
                            "HardwoodOther",
                            "HardwoodCoarseRoots",
                            "HardwoodFineRoots"
                        ],
                        "data_name": "Total_Biomass_C",
                        "enabled": True,
                        "variable_data_type": "float",
                        "on_notification": "OutputStep"
                    },
                    {
                        "pool_name": [
                            "AboveGroundVeryFastSoil",
                            "BelowGroundVeryFastSoil",
                            "AboveGroundFastSoil",
                            "BelowGroundFastSoil",
                            "MediumSoil",
                            "AboveGroundSlowSoil",
                            "BelowGroundSlowSoil",
                            "SoftwoodStemSnag",
                            "SoftwoodBranchSnag",
                            "HardwoodStemSnag",
                            "HardwoodBranchSnag"
                        ],
                        "data_name": "Dead_Organic_Matter_C",
                        "enabled": True,
                        "variable_data_type": "float",
                        "on_notification": "OutputStep"
                    },
                    {
                        "pool_name": [
                            "BelowGroundVeryFastSoil",
                            "BelowGroundSlowSoil"
                        ],
                        "data_name": "Soil_C",
                        "enabled": True,
                        "variable_data_type": "float",
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots"
                            ],
                            "from": [
                                "Atmosphere"
                            ]
                        },
                        "data_name": "NPP",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "to": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "from": [
                                    "Atmosphere"
                                ]
                            },
                            {
                                "subtract": True,
                                "from": [
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ],
                                "flux_source": "annual_process"
                            }
                        ],
                        "data_name": "NEP",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "flux_source": "annual_process",
                                "from": [
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ]
                            }
                        ],
                        "data_name": "Decomp_Releases",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "to": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "from": [
                                    "Atmosphere"
                                ]
                            },
                            {
                                "subtract": True,
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "to": [
                                    "Products"
                                ],
                                "flux_source": "disturbance"
                            },
                            {
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "subtract": True,
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ]
                            }
                        ],
                        "data_name": "NBP",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "to": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "from": [
                                    "Atmosphere"
                                ]
                            },
                            {
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "subtract": True,
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ]
                            },
                            {
                                "subtract": True,
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "to": [
                                    "Products"
                                ],
                                "flux_source": "disturbance"
                            }
                        ],
                        "data_name": "Delta_Total_Ecosystem",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "to": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "from": [
                                    "Atmosphere"
                                ]
                            },
                            {
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "subtract": True,
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ]
                            },
                            {
                                "subtract": True,
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "to": [
                                    "Products"
                                ],
                                "flux_source": "disturbance"
                            },
                            {
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "subtract": True,
                                "to": [
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ]
                            }
                        ],
                        "data_name": "Delta_Total_Biomass",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots"
                                ],
                                "to": [
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ]
                            },
                            {
                                "from": [
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "subtract": True,
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO",
                                    "Products"
                                ]
                            }
                        ],
                        "data_name": "Delta_Total_DOM",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CO2",
                                "CH4",
                                "CO"
                            ],
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots",
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Total_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CO2",
                                "CH4",
                                "CO"
                            ],
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots"
                            ]
                        },
                        "data_name": "Total_Biomass_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CO2",
                                "CH4",
                                "CO"
                            ],
                            "from": [
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Total_DOM_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CO2"
                            ],
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots",
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Total_CO2_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CO"
                            ],
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots",
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Total_CO_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "to": [
                                "CH4"
                            ],
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots",
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Total_CH4_Emissions",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": [
                            {
                                "to": [
                                    "CO2",
                                    "CH4",
                                    "CO"
                                ],
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "AboveGroundVeryFastSoil",
                                    "BelowGroundVeryFastSoil",
                                    "AboveGroundFastSoil",
                                    "BelowGroundFastSoil",
                                    "MediumSoil",
                                    "AboveGroundSlowSoil",
                                    "BelowGroundSlowSoil",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ]
                            },
                            {
                                "flux_source": "disturbance",
                                "from": [
                                    "SoftwoodMerch",
                                    "SoftwoodFoliage",
                                    "SoftwoodOther",
                                    "SoftwoodCoarseRoots",
                                    "SoftwoodFineRoots",
                                    "HardwoodMerch",
                                    "HardwoodFoliage",
                                    "HardwoodOther",
                                    "HardwoodCoarseRoots",
                                    "HardwoodFineRoots",
                                    "SoftwoodStemSnag",
                                    "SoftwoodBranchSnag",
                                    "HardwoodStemSnag",
                                    "HardwoodBranchSnag"
                                ],
                                "to": [
                                    "Products"
                                ]
                            }
                        ],
                        "data_name": "Ecosystem_Removals",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    },
                    {
                        "variable_data_type": "float",
                        "flux": {
                            "flux_source": "disturbance",
                            "from": [
                                "SoftwoodMerch",
                                "SoftwoodFoliage",
                                "SoftwoodOther",
                                "SoftwoodCoarseRoots",
                                "SoftwoodFineRoots",
                                "HardwoodMerch",
                                "HardwoodFoliage",
                                "HardwoodOther",
                                "HardwoodCoarseRoots",
                                "HardwoodFineRoots"
                            ],
                            "to": [
                                "AboveGroundVeryFastSoil",
                                "BelowGroundVeryFastSoil",
                                "AboveGroundFastSoil",
                                "BelowGroundFastSoil",
                                "MediumSoil",
                                "AboveGroundSlowSoil",
                                "BelowGroundSlowSoil",
                                "SoftwoodStemSnag",
                                "SoftwoodBranchSnag",
                                "HardwoodStemSnag",
                                "HardwoodBranchSnag"
                            ]
                        },
                        "data_name": "Bio_To_DOM_From_Disturbances",
                        "enabled": True,
                        "on_notification": "OutputStep"
                    }
                ],
                "output_path": "..\\output"
            }
        },
         "CBMAggregatorLandUnitData": {
            "enabled": True,
            "order": 12,
            "library": "moja.modules.cbm",
            "settings": {
                "reporting_classifier_set": "reporting_classifiers"
            }
        },
       "CBMAggregatorSQLiteWriter": {
            "enabled": True,
            "order": 13,
            "library": "moja.modules.cbm",
            "settings": {
                "databasename": "..\\output\\gcbm_output.db"
            }
        }
	}
}

json_object5 = json.dumps(dictionary5, indent = 4)

with open("modules_output.json", "w") as outfile:
    outfile.write(json_object5)

## internal_variables

dictionary6 ={
    "Variables": {
        "spatialLocationInfo": {
            "flintdata": {
                "type": "SpatialLocationInfo",
                "library": "internal.flint",
                "settings": {}
            }
        },
        "simulateLandUnit": True,
        "is_decaying": True,
        "spinup_moss_only": False,
        "run_peatland": False,
        "peatlandId": -1,
        "is_forest": True,
        "run_moss": False,
        "run_delay": False,
        "landUnitBuildSuccess": True,
        "regen_delay": 0,
        "age": 0,
        "tileIndex": 0,
        "blockIndex": 0,
        "cellIndex": 0,
        "LandUnitId": -1,
        "landUnitArea": 0,
        "classifier_set": {},
        "localDomainId": 0,
        "LocalDomainId": 1,
        "age_class": 0,
        "historic_land_class": "FL",
        "current_land_class": "FL",
        "unfccc_land_class": "UNFCCC_FL_R_FL"
    }
}

json_object6 = json.dumps(dictionary6, indent = 4)

with open("internal_variables.json", "w") as outfile:
    outfile.write(json_object6)


