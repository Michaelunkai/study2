#!/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=output.txt
#SBATCH --ntasks=1
#SBATCH --time=01:00
#SBATCH --partition=debug

echo "Hello, SLURM!"
