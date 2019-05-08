### README

What do I need to document?

* round 1 submissions:
    - scripts that get executed in parallel: 1 shell script, 2 python scripts
    - script that writes condor job submission scripts
    - shell script to manage jobs that failed
    - shell script to find the jobs that were somehow missing
* process of combining ~13,500 files
    - approach 1: by state
    - approach 2: by uid
* round 2 submission:
    - scripts that get executed: 1 shell script, 1 python script
    - script that writes condor job submission
* format of matrix file

### Step 0: Sort the data by 2-digit user id


### Step 1: Spatial join mobile points to tract polygons

In this step, I take the mobile phone coordinates and join them to OpenStreetMap road buffers and to Census tract polygons. I do this in a series of approximately 13,500 parallelized jobs: one join per state times 51 states, times 256 two-digit hex user IDs. 

* batch_national_condor.py writes the Condor submission scripts 
    - arguments: state, jobs (user ids), filename of .submit file that it produces

* each job requires a number of inputs:
    - test-state.sh: a bootstrap script that runs everything, from setup/installation through Python scripts
    - miniconda.sh, condarc: for installing Python 3.7.1 and geopandas on the worker node
    - process_single_job.py: a Python script that performs the join and some related data cleaning
    - make_csv_exist.py: a Python script that returns an empty csv file when no points join
    - data files:
        - the compressed location data
        - a state-level roadways geojson file
        - US tracts geojson file

* Once we install Python and geopandas on the worker node, the process_single_job.py script does the following:
    - extracts Census tracts in the relevant state from the US tract file
    - creates a bounding box for that state from those tract polygons
    - reads in the roadways file and creates a buffer of 10 meters surrounding the roads
    - iterates through 100,000 rows of the compressed mobile phone location data, performing the following steps each time:
        1. drop observations where the location accuracy is 0
        2. drop observations that fall outside of the state bounding box
        3. convert the latitude and longitude fields in the data to Point class
        4. join these points to the tract polygons
        5. join the resulting data frame to the roadways buffers to denote which points fall on a major roadway
        6. append to an output file

* In some cases, especially in less-populous states, the input data file may not contain any points in a given state. In this case, the make_csv_exist.py script will create a csv file with a single line where each value is 0. The purpose of doing is to ensure that the worker node returns something if the job ran successfully, so that we can distinguish jobs that ran successfully but had no points inside a given state from jobs that failed. These dummy files are still distinguishable from files that contain data due to their tiny size, and they do not get incorporated in subsequent rounds because they contain only 0 values. 



