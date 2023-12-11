This directory shows the installation of WRF version 4.5.1(which is the required version for ADIOS2) and the jarvis scripts written for deployment using Jarvis-cd pipelines.

## Installation
Refer to this repository to install the WRF version 4.5.1 along with all the dependecies

https://github.com/grc-iit/jarvis-cd/wiki/7.5.-WRF

## Jarvis Scripts
Each HPC application needs its own jarvis script as the input parameters vary for each. Here is the Jarvis script for WRF version 4.5.1
```python

"""
This module provides classes and methods to launch the Wrf45 application.
Wrf45 is ....
"""
from jarvis_cd.basic.pkg import Application
from jarvis_util import *


class Wrf45(Application):
    """
    This class provides methods to launch the Wrf application.
    """

    def _init(self):
        """
        Initialize paths
        """
        pass

    def _configure_menu(self):
        """
        Create a CLI menu for the configurator method.
        For thorough documentation of these parameters, view:
        https://github.com/scs-lab/jarvis-util/wiki/3.-Argument-Parsing

        :return: List(dict)
        """
        return [
            {
                'name': 'nprocs',
                'msg': 'Number of processes',
                'type': int,
                'default': 1,
            },
            {
                'name': 'ppn',
                'msg': 'The number of processes per node',
                'type': int,
                'default': None,
            },
            {
                'name': 'wrf_location',
                'msg': 'The location of wrf.exe',
                'type': str,
                'default': None,
            },
            {
                'name': 'wrf_output',
                'msg': 'The location of output file',
                'type': str,
                'default': None,
            },

        ]

    def _configure(self, **kwargs):
        """
        Converts the Jarvis configuration to application-specific configuration.
        E.g., OrangeFS produces an orangefs.xml file.

        :param kwargs: Configuration parameters for this pkg.
        :return: None
        """
        self.update_config(kwargs, rebuild=False)
        output_location = self.config['wrf_output']
        if output_location[-1] != '/':
            output_location += '/'
        output_location += 'wrfout_d01_2019-11-26_12:00:00'
        print(output_location)
        replacement = [("wrfout_d01_2019-11-26_12:00:00", output_location)]
        self.copy_template_file(f'{self.pkg_dir}/config/adios2.xml',
                                f'{self.config["wrf_location"]}/adios2.xml', replacement)

    def start(self):
        """
        Launch an application. E.g., OrangeFS will launch the servers, clients,
        and metadata services on all necessary pkgs.

        :return: None
        """
        Exec('wrf.exe',
             MpiExecInfo(nprocs=self.config['nprocs'],
                         ppn=self.config['ppn'],
                         hostfile=self.jarvis.hostfile,
                         env=self.mod_env,
                         cwd=self.config['wrf_location']))

        pass

    def stop(self):
        """
        Stop a running application. E.g., OrangeFS will terminate the servers,
        clients, and metadata services.

        :return: None
        """
        pass

    def clean(self):
        """
        Destroy all data for an application. E.g., OrangeFS will delete all
        metadata and data directories in addition to the orangefs.xml file.

        :return: None
        """
        pass

```
## Jarvis config folder
Each jarvis package needs have a configuration folder "config" which stored the ```adios2.xml``` and other necessary files. In WRF's case it also stores the ```namelist.input``` file
The ```adios2.xml``` configures the WRF for ADIOS2 configuration and ```namelist.input``` decides parameters like frames per output, output location,etc. 


[adios2.xml](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/blob/main/WRF/config/adios2.xml)

[namelist.input](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/blob/main/WRF/namelist.input)
