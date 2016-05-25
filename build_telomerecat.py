#! /usr/bin/env python
import sys
import traceback
import tempfile
import os
import subprocess
import shutil

#Ensure that the environment has the required python packages
try:
    import argparse
    import pandas
    import parabam
    import pysam
    import numpy
    import PyInstaller
    import sklearn
    import scipy

except ImportError as exep:
    sys.stdout.write(\
                "##ERROR## Attempt to build telomerecat with missing package")
    traceback.print_exception(*sys.exc_info())

def build_telomerecat(project_path, temp_dir_path):
    spec_file_path = create_spec_file(project_path,temp_dir_path)
    run_pyinstaller(project_path,spec_file_path)
    shutil.rmtree(temp_dir_path)

def create_spec_file(project_path, temp_dir_path):
    os_info,spec_file_path = tempfile.mkstemp(suffix=".spec",dir=temp_dir_path)
    spec_template_path = os.path.join(\
                        os.path.dirname(__file__),"telomerecat.spec.template")
    with open(spec_file_path,"w") as spec_file_obj:
        with open(spec_template_path,"r") as spec_template_obj:
            insert = True
            for line in spec_template_obj:
                spec_file_obj.write(line)
                if insert:
                    relevant_dir = os.path.join(project_path,"telomerecat")
                    spec_file_obj.write("telomerecat_dir = '%s'\n" \
                                                        % (relevant_dir,))
                    insert = False
    return spec_file_path

def run_pyinstaller(project_path, spec_path):
    call = ["pyinstaller","--clean","--onefile","--distpath=./","%s"\
                                                             % (spec_path,)]
    return_code = subprocess.call(call)
    return return_code

if __name__ == "__main__":

    project_path = sys.argv[1]
    temp_dir_path = tempfile.mkdtemp(dir=".")
    build_telomerecat(project_path,temp_dir_path)

