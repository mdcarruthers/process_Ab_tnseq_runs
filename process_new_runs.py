# process_nwe_runs.py
# (C) Larry Gallagher 2016
#
# For auto processing of A.b. tn-seq run data

import os, re
from subprocess import call

# PARAMETERS and CONSTANTS -----------------------------------------------------
home_dir = r'/home/lg/'
storage_dir = r'/home/manoil-data/lg/Tn-seq_Ab/'
working_dir = r'/home/lg/work_Ab/'
tnseq_program_dir = r'/home/lg/Tn-seq-1.1.1/python/'
# ------------------------------------------------------------------------------

def move_fastq_files():
    cwd = os.getcwd()
    os.chdir(home_dir)
    dirlist = os.listdir('.')
    dirpatt = re.compile(r'^\d*-?\d+_S\d+')
    fqfilepatt = re.compile(r'^\d*_?(.+)_S\d+.*((\.fastq)|(\.fq))(\.gz)?')
    for rundir in dirlist:
        if (os.path.isdir(rundir) and dirpatt.match(rundir)):
            # it is a directory with name of the expected pattern; process it.
            dirname = None
            m = re.match(r'^(\d{6}-\d+)_S\d', rundir)
            if m:
                dirname = m.group(1)
            else:
                m = re.match(r'^(\d{6})_S\d', rundir)
                if m:
                    dirname = m.group(1)
            if not dirname:
                print "Could not parse directory name, " + rundir
                continue
            print "Copying directory " + rundir + " to storage location..."
            args = ['cp', '-r', '-u', rundir + '/', storage_dir]
            call(args)
            os.chdir(rundir)
            itemdirlist = os.listdir('.')
            for item in itemdirlist:
                m = re.search(fqfilepatt, item)
                if m:
                    sample = m.group(1)
                    extension = m.group(2) + m.group(5)
                    newname = dirname + '_' + sample + extension
                    destination = working_dir + newname
                    print "   executing command: mv " \
                          + item + " " + destination
                    args = ['mv', item, destination]
                    call(args)
            os.chdir(home_dir)
            args = ['rmdir', rundir + r'/']
            call(args)  # will see error if dir is not empty
            # in future, perhaps add exception handling for this call(args)
    os.chdir(cwd)

def process_samples():
    cwd = os.getcwd()
    os.chdir(working_dir)
    dirlist = os.listdir('.')
    sample_pattern = re.compile(r'^(\d{6}-?\d*_.+)((\.fastq)|(\.fq))(\.gz)?')
    for item in dirlist:
        # check that it's a sample file:
        m = sample_pattern.search(item)
        if m:
            print 'Processing sample: ', item
            # unzip if necessary
            if m.group(5):
                print '  unzipping...'
                args = ['gzip', '-d', item]
                call(args)
            
