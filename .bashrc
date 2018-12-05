alias ls='ls --color=auto'

source ~/.bashrc_secrets

export R_LIBS_USER=~/tools/Rlib

# common folder
export FRIDGE=/Fridge/users/giovanni

# Miniconda3 
export PATH=~/tools/miniconda/bin:$PATH

export PYTHONPATH=$FRIDGE/projects/rumc/scripts

# nodejs
export NODEJS_HOME=~/tools/node-v8.9.2
export PATH=$NODEJS_HOME/bin:$PATH

# fsl
FSLDIR=/home/giovanni/tools/fsl
. ${FSLDIR}/etc/fslconf/fsl.sh
PATH=${FSLDIR}/bin:${PATH}
export FSLDIR PATH

# freesurfer
export FREESURFER_HOME=/usr/local/freesurfer_6.0.1
export LOCAL_DIR=$FREESURFER_HOME/local
export SUBJECTS_DIR=$FREESURFER_HOME/subjects
export FSFAST_HOME=$FREESURFER_HOME/fsfast
export MINC_BIN_DIR=$FREESURFER_HOME/mni/bin
export MINC_LIB_DIR=$FREESURFER_HOME/mni/lib
export MNI_DATAPATH=$FREESURFER_HOME/mni/data
export MNI_DIR=$FREESURFER_HOME/mni
export PERL5LIB=$MINC_LIB_DIR/perl5/5.8.5
export FSF_OUTPUT_FORMAT=nii.gz
export PATH=$FREESURFER_HOME/bin:$FSFAST_HOME/bin:$MINC_BIN_DIR:$PATH

#New AFNI path december  2016
## This is basically a copy of /etc/afni/afni.sh, without sourcing the users prefs
## !! note that there is no separate bin/ models/ folder, all is in one. 
#where AFNI is installed
AFNI_INSTALLDIR=/usr/local/afni
# add the AFNI binary path to the search path
PATH=${AFNI_INSTALLDIR}:${PATH}
# Location of the plugins
AFNI_PLUGINPATH=${AFNI_INSTALLDIR}
# Location of the timseries models (also plugins)
AFNI_MODELPATH=${AFNI_INSTALLDIR}
# Location of the talairach daemon database
AFNI_TTATLAS_DATASET=/usr/share/afni/atlases
#
# Runtime checks
#
# Suppress warning for missing mpeg output
AFNI_IMSAVE_WARNINGS=NO
export PATH AFNI_PLUGINPATH AFNI_MODELPATH AFNI_IMSAVE_WARNINGS AFNI_TTATLAS_DATASET
# ln -s /usr/lib/x86_64-linux-gnu/libgsl.so  /home/giovanni/tools/lib/libgsl.so.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/giovanni/tools/lib

# ANTS
export PATH=~/tools/ants:$PATH

# custom code (ctags)
export PATH=~/tools/bin:$PATH

# custom firefox
export PATH=~/tools/bin/firefox:$PATH

# hide conda and venv
PS1='[\u@\h:\w]\$ '

# use all colors in MATE terminal
TERM=xterm-256color

alias flywheel="fw login $FLYWHEEL_TOKEN"