#!/bin/bash
#SBATCH --job-name=cv_scope    # Job name
#SBATCH --partition=shared-gpu
#SBATCH --gres=gpu:pascal:1                    # Number of GPUs
#SBATCH --ntasks=1
#SBATCH --mem=30G                     # Job memory request
#SBATCH --cpus-per-task=16
#SBATCH --time=05:00:00               # Time limit hrs:min:sec
#SBATCH --output=/home/users/k/klug/logs/scope/cv_keras_scope_%j.log   # Standard output and error log


module load Anaconda3

source /home/users/k/klug/.bashrc

cd /home/users/k/klug/scope
export PYTHONPATH=$(pwd)

conda activate scope

ulimit -S -n 131072 # setting "soft" limit number of file descriptor per processes
ulimit -S -u 1546461 # setting soft limit number of processes per user

srun python scope/cross_validate.py -c experiment_configs/outcome_scope/yggdrasil.json