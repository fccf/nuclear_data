
import os
from distutils import spawn
import numpy as np

# global Parameters
default_fendl_path = './fendl'
default_matxs_path = './xs'
default_fendl_url  = 'https://www-nds.iaea.org/fendl/data/neutron/fendl31d-neutron-matxs.zip'


class fendl(object):
    """fendl library."""
    def __init__(self, fendl_path = None, matxs_path = None):
        self._fendl_path = default_fendl_path
        self._matxs_path = default_matxs_path
        self._nuclide_list = []
        if fendl_path is not None:
            self._fendl_path = fendl_path
        if matxs_path is not None:
            self._matxs_path = matxs_path
        #get nuclide_list from matxs_path
        #self._nuclide_list = sorted(os.listdir(self._matxs_path))

    def download(self):
        """
        download Fendl 3.1d
        """
        print('Downloading Fendl 3.1d data to '+self._fendl_path)
        os.system("wget "+default_fendl_url)
        print('Extracting Data')
        os.system("unzip fendl31d-neutron-matxs.zip -d {}".format(self.fendl_path))
        os.system("rm fendl31d-neutron-matxs.zip")

    def make_matxs(self):
        """
        make matxs by bbc
        """
        bbcinput = open("bbcinput",'w')
        bbcinput.write('-1 1 0 0 1')
        bbcinput.close()
        xsfiles = sorted(os.listdir(self._fendl_path))
        for filename in xsfiles:
            # move the text file to current directory and call it text
            path = '{}/{}'.format(self._fendl_path, filename)
            os.system("cp {} text".format(path))
            # get name of nuclide to call new matxs file
            f = open("text", 'r')
            line = f.readline()
            name = line.split('*')[1][9:].strip()
            f.close()
            # run bbc to get matx file
            if spawn.find_executable('bbc') == None:
                print("No bbc executable found.")
            os.system("bbc")
            # move matx file to new name
            os.system("mv matxs {}/{}".format(self._matxs_path,name))
            # remove extra files created
            os.system("rm index text")

    def neutron_group(self):
        "neutron group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[0])
        f.close()
        return ng

    def gamma_group(self):
        "gamma group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[1])
        f.close()
        return ng

    def group_number(self):
        "energy group number"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        ng = int(line.split()[1]) + int(line.split()[0])
        f.close()
        return ng

    def nuclide_list(self):
        nuclide_list = sorted(os.listdir(self._matxs_path))
        return nuclide_list

    def nuclide_number(self):
        nuclide_list = sorted(os.listdir(self._matxs_path))
        nn = len(nuclide_list)
        return nn

    def neutron_group_structure(self):
        "neutron energy group structure"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 8):
            line = f.readline()
        lines = ''
        for i in range(9, 44):
            line = f.readline()
            lines = lines + line
        ngs = map(eval,lines.split()[1:])
        f.close()
        return ngs

    def gamma_group_structure(self):
        "gama energy group structure"
        any_file = os.listdir(self._fendl_path)[0]
        f = open('{}/{}'.format(self._fendl_path, any_file), "r")
        for i in range(0, 44):
            line = f.readline()
        lines = ''
        for i in range(45, 52):
            line = f.readline()
            lines = lines + line
        ggs = map(eval,lines.split()[1:])
        f.close()
        return ggs

    def print_information(self):
        "print fendl "
        print('nuclide number:',self.nuclide_number())
        print("neutron group number",self.neutron_group())
        print("neutron group structure",self.neutron_group_structure())
        print("gamma group number",self.gamma_group())
        print("gamma group structure",self.gamma_group_structure())
        print("group number",self.group_number())
        print('nuclides:',self.nuclide_list)
