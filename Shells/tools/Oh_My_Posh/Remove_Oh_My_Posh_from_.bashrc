 Remove Oh My Posh from .bashrc
If you want to revert to the default Bash prompt, follow these steps:

Remove the Oh My Posh Configuration Line:

Use the sed command to automatically remove the Oh My Posh line from your .bashrc:
 
 
sed -i '/oh-my-posh --init --shell bash --config ~\/jandedobbeleer.omp.json/d' ~/.bashrc
Apply the Changes:

Source the .bashrc file again to revert to the default prompt:
 
 
source ~/. rc
(Optional) Remove Oh My Posh Binary:

If you also want to remove Oh My Posh from your system entirely:
 
 
sudo rm /usr/local/bin/oh-my-posh
