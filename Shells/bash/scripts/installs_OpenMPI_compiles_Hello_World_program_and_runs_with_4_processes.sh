echo '#!/bin/ 
# Setting up and running MPI with OpenMPI on Ubuntu as root without venv

# Install necessary dependencies
apt install -y openmpi-bin openmpi-common libopenmpi-dev

# Create and navigate to project directory
mkdir -p /root/mpi_openmpi_helloworld && cd /root/mpi_openmpi_helloworld

# Create C program for MPI Hello World
cat > hello_world.c << EOF
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);
    printf("Hello world from processor %s, rank %d out of %d processors\\n", processor_name, world_rank, world_size);
    MPI_Finalize();
    return 0;
}
EOF

# Compile the MPI program
mpicc -o hello_world hello_world.c

# Run the compiled program with 4 processes, allowing root user execution, with oversubscribe to bypass slot limitations
OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 mpirun --oversubscribe -np 4 ./hello_world
' > /root/installs_OpenMPI_compiles_Hello_World_program_and_runs_with_4_processes.sh && chmod +x /root/installs_OpenMPI_compiles_Hello_World_program_and_runs_with_4_processes.sh && /root/installs_OpenMPI_compiles_Hello_World_program_and_runs_with_4_processes.sh
