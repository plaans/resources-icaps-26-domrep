#!/bin/bash

job_name=$1
timeout=$2
output=$3
command=$4

printf -v timeout_slurm "%d-%02d:%02d:%02d" \
        "$(((timeout+30)/86400))" \
        "$(((timeout+30)%86400/3600))" \
        "$(((timeout+30)%3600/60))" \
        "$(((timeout+30)%60))"

sbatch <<EOF
#!/bin/bash

#SBATCH --job-name=${job_name}
#SBATCH --partition=cpuintel
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=${timeout_slurm}
#SBATCH --output=${output}

##SBATCH --test-only

${command}

EOF