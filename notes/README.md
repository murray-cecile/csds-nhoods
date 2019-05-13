### README

What do I need to document?

* process of combining ~13,500 files
    - approach 1: by state
    - approach 2: by uid
* round 2 submission:
    - scripts that get executed: 1 shell script, 1 python script
    - script that writes condor job submission
* format of matrix file

### Step 0: Sort the data by 2-digit user id

Initially, the data came in 500 compressed csv files. I took these csv files and sorted them into 256 compressed csv files, each containing all of the observations with the same two hexadecimals at the beginning of the user ID. This ensured that all observations for a unique user ID would be contained within the same file. 

nohup bzcat /home/jsaxon/LiveRampReduce/0-4]??.csv.bz2 | awk '{print >> "sorted/u_"substr($1,6,2)".csv" }' &

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

### Managing failed jobs in step 1

Not all of these jobs ran successfully the first time, so I wrote a couple of scripts to identify these jobs and resubmit them:

1. manage-jobs.sh: 
    * This script finds empty csv.bz2 files in the relevant subdirectories, extracts the user IDs that failed,  dumps them into a temporary text file where I can examine them, and creates a new submission script to resubmit those jobs. 
    * I did this by state, so manage-jobs expects the two-digit state FIPS code as an argument.

2. find-missing.sh and find_missing_jobs.py
    * Some jobs failed to return an empty csv, so manage-jobs.sh wouldn't pick them up. The Python script crawls the directory and checks for the existence of all 13,500 expected user ID-state combinations and dumps the ones it doesn't find into a text file.
    * find-missing.sh then takes that text file and uses it to create a new submission script to resubmit those jobs.

### Step 2: Combining files

The next step is to combine the state-level user ID files. I created two ways to do this: by state, and by user ID. In the first case, all 256 csv files corresponding to a particular state are concatenated; in the second, all 51 states for a given user ID are concatenated. I ran this process locally on the main node, using nohup.

At this stage, I dropped observations where the accuracy value was greater than 500 (indicating that the location estimate was precise to a radius larger than 500 meters).

* concatenate_states.py: wraps user IDs up by state. It takes a user ID and an optional two-digit state FIPS as an argument and loops through all of the files, appending them into one large file. If no two-digit state FIPS is provided, it will loop through all 51 by default, but these files are usually too big to use.

* concatenate_jobs.py: wraps up states by user ID (preferred). It takes optional state FIPS codes, optional user IDs, and optional characters to be appended to the resulting filename (e.g. to denote which states/user IDs it contains).

python concatenate_jobs.py -st 17 27 55 -uids 00 -suff _ILMNWI

### Step 3: Creating the visits matrix

Next, I computed users' home locations and visit frequencies to other locations in 256 parallelized jobs. Each user ID file contains all observations of the set of users whose identifiers begin with a specific two-digit hexidecimal, so a user's entire location history is included in a single file. The components for these jobs are as follows:

* locate-homes.sh, a bootstrap script for installing Python and geopandas and executing the Python script that performs the data manipulation
* miniconda.sh, condarc: for installing Python 3.7.1 and geopandas on the worker node
* locate_homes.py: the Python script that performs the data manipulation
* input data files:
    - timezones
    - data file

The process for computing home and visit location frequencies is as follows:
 
