# Define the password and remote host variables
PASSWORD='123456'
REMOTE_HOST='192.168.1.193'

# Ensure the .ssh directory exists
mkdir -p /root/.ssh

# Add the remote host's key to known_hosts to prevent host key verification failure
ssh-keyscan -H $REMOTE_HOST >> /root/.ssh/known_hosts

# Copy the .bashrc file to the remote host
sshpass -p "$PASSWORD" scp /root/.bashrc ubuntu@$REMOTE_HOST:/home/ubuntu/.bashrc_temp

# Move the .bashrc_temp to the correct location and source it
sshpass -p "$PASSWORD" ssh ubuntu@$REMOTE_HOST "echo $PASSWORD | sudo -S mv /home/ubuntu/.bashrc_temp /root/.bashrc && sudo cp /root/.bashrc /home/ubuntu/.bashrc && source ~/.bashrc"

