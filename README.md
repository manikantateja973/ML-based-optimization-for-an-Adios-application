# ML based optimization for an ADIOS application
This project deals with the deployment of HPC application on top of Hermes in the cloud to collect metadata needed to perform PCA analysis to determine the best cache eviction policies and data placement strategies. It shows the installtion of WRF, LAMMPS and OpenFOAM with ADIOS2 configurations and the deployment of these using Jarvis-cd.
This repository is divided into three sections for each of the HPC application and then the data collected for the LAMMPS when integrated with COEUS-ADAPTER. 

* [WRF](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/tree/main/WRF)
* [LAMMPS](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/tree/main/LAMMPS)
* [OpenFOAM](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/tree/main/OpenFOAM)

# Dependencies
This project requires the following dependencies to be installated.

## Hermes 
Hermes is a heterogeneous-aware, multi-tiered, dynamic, and distributed I/O buffering system that aims to significantly accelerate I/O performance.
Installation of Hermes can be done using:

[Hermes](https://github.com/HDFGroup/hermes/blob/master/README.md)

Note: The latest version of the Hermes has to installed for smooth integration with Coeus-adapter

## Jarvis-cd 
Jarvis-cd is the orchestration and deployment software used for this project to deploy and execute HPC applications. You can find the installation of this software here:

[Jarvis-cd](https://github.com/grc-iit/jarvis-cd/)


## Coeus-adapter
COEUS Hermes Adios Engine is an adapter which connects ADIOS to Hermes through the use of the ADIOS plugins interface.

[Coeus-adapter](https://github.com/grc-iit/coeus-adapter)
## Future work
* Deployment of other HPC applications using Jarivs
* Refinement of data collection as a singular log file from Coeus-adapter
* Building and ML model to perform PCA analysis on the metadata collected
