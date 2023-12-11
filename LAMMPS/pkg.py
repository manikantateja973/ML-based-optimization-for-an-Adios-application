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
