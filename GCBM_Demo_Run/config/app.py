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

# provider_config.json

# for ob in dir_list:
#     fp1 = r'ob'
#     img = rst.open(fp1)
#     print(img.nodata)

# fp1 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/classifiers/Classifier1_moja.tiff'

# fp2 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/classifiers/Classifier2_moja.tiff'

# fp3 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2011_moja.tiff'

# fp4 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2012_moja.tiff'

# fp5 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2013_moja.tiff'

# fp6 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2014_moja.tiff'

# fp7 = r'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2015_moja.tiff'

# fp8 = f'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2016_moja.tiff'

# fp9 = f'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/disturbances/disturbances_2018_moja.tiff'

# fp10 = f'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/miscellaneous/initial_age_moja.tiff'

# fp11 = f'/home/padmajabhol/Desktop/Code/GitHub/LFX-mentorship-progress-tracker/GCBM_Demo_Run/layers/tiled/miscellaneous/mean_annual_temperature_moja.tiff'



# img1 = rst.open(fp1)
# img2 = rst.open(fp2)


# t = img1.transform
# x1 = t[0]
# y1 = -t[4]

# t2 = img2.transform
# x2 = t2[0]
# y2 = -t2[4]
# print(x1,y1)

Rasters = []

# for thisFile in os.listdir(path):
#     # fN, fE = os.path.splitext(thisFile)
#     # if fE.upper() == '.tiff':
#     # fp = f'thisFile'
#     # img = rst.open(fp)
#     # x = img.nodata
#     d = dict()
#     d = thisFile

#     Rasters.append(d)
#         # Rasters.append(thisFile)

# print(Rasters)




for filepath in pathlib.Path(path).glob('**/*'):
    ab = filepath.absolute()
    print(filepath.absolute())
    fp = r'filepath.absolute(1)'
    img = rst.open(fp)
    print(img.nodata)
    Rasters.append(ab)
    # print(Rasters)




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

# lst2 = []
# e = dict()
# e["cell"] = 1
# lst2.append(e)
# dictionary["Providers"]["RasterTiled"] = lst2
# dictionary["Providers"]["RasterTiled"]["layers"] = lst

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


