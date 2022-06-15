To run the simulation, 
 - navigate to https://github.com/moja-global/FLINT.Cloud/pull/111 or clone my forked repo and switch to `gcbm_api` branch https://github.com/padmajabhol/FLINT.Cloud/tree/gcbm_api
 
 To run the GCBM REST API:
 1. Navigate to the required folder: 
  ```
   cd FLINT.Cloud/local/rest_api_gcbm
  ```
 2. Run:
  ```
    docker build --build-arg BUILD_TYPE=RELEASE --build-arg NUM_CPU=4 -t gcbm-api .
  ```
 3. Run: 
 ```
    docker run --rm -p 8080:8080 gcbm-api
  ```

 To run the endpoints and to start a new GCBM simulation:
 
 Unzip `GCBM_New_Demo_Run` and open a terminal inside the folder and run the following curl commands:
 
 1. Create a new simulation (the default title of the simulation is `simulation`, here the title `run4` is used): 
     ```
        curl -d "title=run4" -X POST http://localhost:8080/gcbm/new
    ````

 2. Upload the input files: </br>
    ```
        curl -F disturbances='@disturbances/disturbances_2011_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2012_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2013_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2014_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2015_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2016_moja.tiff' \
            -F disturbances='@disturbances/disturbances_2018_moja.tiff' \
            -F classifiers='@classifiers/Classifier1_moja.tiff' \
            -F classifiers='@classifiers/Classifier2_moja.tiff' \
            -F db='@db/gcbm_input.db' \
            -F miscellaneous='@miscellaneous/initial_age_moja.tiff' \
            -F miscellaneous='@miscellaneous/mean_annual_temperature_moja.tiff' \
            -F title="run4" \
            http://localhost:8080/gcbm/upload

    ```
    
  3. To start the simulation, run:
     ```
         curl -d "title=run4" -X POST http://localhost:8080/gcbm/dynamic
     ```
     This should take a maximum of 20-25 minutes to finish running and even less depending on your system. The end terminal message should be `SQLite insert complete`.
    
   
   4. To download the input, run the following curl command 3-5 minutes after the simulation has finished running:
      ```
         curl -d "title=run4" -X POST http://localhost:8080/gcbm/download -L -o run4.zip
      ```
