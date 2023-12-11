# Installation of LAMMPS using various installation mechanisms
## On Ares
When you are on Ares, you should ideally find the lammps application already installed as a module. To see if there is a lammps module in ares run the below command:

```linux
module spider lammps
#module -r spider '.*lammps*.'
```
To load the module use. (Note that this loads the default lammps version)
```linux
module load lammps
```
## Using spack
You can view the lammps in list of provided packages in spack using:
```linux
spack list lammps
```
To list the details of lammps(version, description, dependencies, etc.)
```linux
spack info lammps
```
 To install lammps with adios2 dependency using spack
```linux
spack install lammps+adios
```
## Building from source
You can download the source and the documentation as a tarball
```linux 
mkdir Build_lammps
cd Build_lammps
wget -c https://download.lammps.org/tars/lammps-stable.tar.gz
tar -xzvf lammps*.tar.gz
````
Now change the directory to the LAMMPS distribution directory that just got uncompressed
```linux
cd /path/to/lammps 
mkdir build; cd build  # create and use a build directory
```

### Building LAMMPS with ADIOS2
#### Using CMake
We are going to install LAMMPS with ADIOS2 using CMake. Note that LAMMPS requires CMake version 3.10 or later. You can check your cmake version using:
```linux
cmake --version
```
In order to build lammps with adios2, the adios2 library need to be on your system or be downloaded and built. Then, you need to tell LAMMPS where it is found on your system.
```linux
# This can be done by providing the adios2 installation directory in PATH variable
export PATH=/path/of/adios2:$PATH
#This is ADIOS2 installed path in my system: ~/spack/opt/spack/linux-ubuntu22.04-skylake/gcc-11.4.0/adios2-2.9.0-fsrkmnhkjp4ozmq5fsy2ryeaqcuuzhu
```
One important thing to note here is that if you have ADIOS2 built either with or without MPI then the same has to be matched while building LAMMPS.
```linux
#if ADIOS2 was built with MPI 
cmake ../cmake -D PKG_ADIOS=yes -D BUILD_MPI=yes  
#if ADIOS2 was built without MPI then
#cmake ../cmake -D PKG_ADIOS=yes -D BUILD_MPI=no
```
Now the build files would been written to your build folder.
Now compile them using:
```linux
make 
#make -j N
```
If the compilation is successful, you should see a library ```liblammps.a``` and the LAMMPS executable ```lmp``` inside the build folder.

Now you can either use LAMMPS by running the executable using from this directory using:
```linux 
./lmp
````
Or, you can install the LAMMPS executable into your system with:
```linux
make install #copies compiled files into installation location
```
## Usage
In order to show the usage of lammps with adios2, we can use either ```dump atom/adios``` or ```dump custom/adios``` commands.
What these commands do is that these dump a snapshot of atom coordinates every N timesteps in ADIOS-bases "BP" file format, or using a different I/O solutions in adios to a stream that can be read on-line by another program.
Here is the syntax for each:
```linux
dump ID group-ID atom/adios N file.bp
dump ID group-ID custom/adios N file.bp args
```
Example usages:
Save the below file as ```lj_fluid.in```
```linux
# create a Lennard-Jones fluid
units lj
atom_style atomic
lattice fcc 0.8442
region box block 0 20 0 20 0 20
create_box 1 box
create_atoms 1 box
mass 1 1.0
velocity all create 1.44 87287 loop geom
pair_style lj/cut 2.5
pair_coeff 1 1 1.0 1.0 2.5
neighbor 0.3 bin
neigh_modify delay 0 every 20 check no

# define a group of atoms
group fluid type 1

# dump atom coordinates every 100 timesteps to atoms.bp
dump adios1 fluid atom/adios 100 atoms.bp

# dump custom quantities every 50 timesteps to custom.bp
dump adios2 fluid custom/adios 50 custom.bp id type x y z vx vy vz

# run the simulation for 1000 timesteps
run 1000
```
Then run lammps by giving this input file as argument as shown:
```linux
lmp -in lj_fluid.in
```
If this is successful, you should see the below files in the current directory:
```
custom.bp
atoms.bp
```
Note that a file ```adios2_config.xml``` with specific configuration settings is expected in the current working directory. If the file is not present, LAMMPS will create a minimal default file.

# Jarvis script for LAMMPS
```python
"""This is a module for LAMMPS app"""
from jarvis_cd.basic.pkg import Application
from jarvis_util import *


class Lammps(Application):
    """
    This class provides methods to launch the Ior application.
    """
    def _init(self):
        """
        Initialize paths
        """
        self.input_file = f'{self.pkg_dir}/config/lj_fluid.in'
        #self.lmp_output = f'{self.pkg_dir}/config'

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
                'name': 'lmp_location',
                'msg': 'The location of lammps executable',
                'type': str,
                'default': None,
            },
            {
                'name': 'lmp_output',
                'msg': 'The location of output file/s',
                'type': str,
                'default': None,
            },
            {
                'name':'input_file',
                'msg': 'Input file',
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
        #lmp_output = f'{self.pkg_dir}/config'
        pass

    def start(self):
        """
        Launch an application. E.g., OrangeFS will launch the servers, clients,
        and metadata services on all necessary pkgs.

        :return: None
        """
        Exec(f'lmp -in lj_fluid.in', #-log {self.lmp_output}',
             MpiExecInfo(nprocs=self.config['nprocs'],
                         ppn=self.config['ppn'],
                         hostfile=self.jarvis.hostfile,
                         env=self.mod_env,
                         #pipe_stdout='{self.lmp_output}/lj_fluid.out',
                         cwd=self.config['lmp_location']))

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
        output_dir = self.config['lmp_output'] + "*"
        print(f'Removing {output_dir}')
        Rm(output_dir)
```
# Jarvis config folder
Each jarvis package needs have a configuration folder "config" which stored the adios2.xml and other necessary files. In LAMMPS's case it also stores the ```adios2_config.xml```

[config folder](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/blob/main/LAMMPS/config/adios2_config.xml)

# Metadata 
The metadata is collected by running the application on varying processes using coeus-adapter is stored in this directory

[metadata](https://github.com/manikantateja973/Build-an-ML-based-optimization-for-an-Adios-application/tree/main/Metadata)
