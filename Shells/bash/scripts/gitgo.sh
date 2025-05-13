#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Function definitions for 'down' and 'gitoken' if they are aliases
# If 'down' and 'gitoken' are commands or aliases in your environment, you can remove these functions
down() {
    echo "Running 'down' command..."
    # Replace with the actual commands that 'down' should execute
}

gitoken() {
    echo "Running 'gitoken' command..."
    # Replace with the actual commands that 'gitoken' should execute
}

# Run 'down' command
down

# Remove the existing 'study2' directory
rm -rf /mnt/c/Users/micha/Downloads/study2

# Remove the .bashrc file
rm -f /mnt/c/Users/micha/Shells/bash/.bashrc

# Clone the repository into 'study2' directory
git clone https://github.com/Michaelunkai/study2.git /mnt/c/Users/micha/Downloads/study2

# Change directory to the cloned repository
cd /mnt/c/Users/micha/Downloads/study2

# Synchronize files from '/mnt/c/study/' to current directory, excluding problematic files
rsync -avh --delete \
    --exclude='.git' \
    --exclude='Shells/bash/.bashrc' \
    --exclude='windows/server/PS/Permits_traffic_on_TCP_port_80_to_the_server_with_firewall_rule' \
    --exclude='windows/server/PS/Testing_DNS_resolution' \
    --exclude='windows/server/PS/Verify_Auditing_Policy_and_enable_it' \
    --exclude='windows/server/PS/_Configure_Windows_Defender_Firewall_to_allow_inbound_RDP_traffic_on_port_3389' \
    --exclude='windows/server/PS/_Configure_the_server_to_automatically_install_Windows_updates' \
    --exclude='windows/server/PS/_Diagnose_Network_Issues_on_Windows' \
    --exclude='windows/server/PS/_setup_DHCP_server' \
    --exclude='windows/server/PS/add_user_to_active_directory' \
    --exclude='windows/server/PS/check_dns_server_settings_an_Set_DNS_server_addresses' \
    --exclude='windows/server/PS/configure_windows_updates' \
    --exclude='windows/server/PS/create_new_active_directory_user_and_group' \
    --exclude='windows/server/PS/create_the_primary_DNS_zone_add_a_host_record' \
    --exclude='windows/server/PS/deploy_Active_Directory_Lightweight_Directory_Services_(AD_LDS)_for_lightweight_directory_access_and_directory-enabled_application_support' \
    --exclude='windows/server/PS/disable_unused_services' \
    --exclude='windows/server/PS/implement_Active_Directory_Federation_Services_(AD_FS)__for_single_sign-on_(SSO)_and_identity_federation_across_different_applications' \
    --exclude='windows/server/PS/install_&&_Configuring_DHCP_Server' \
    --exclude='windows/server/PS/install_&_configure_Active_Directory_Certificate_Services_role.txt' \
    --exclude='windows/server/PS/install_active_directory_domain,_create_domain_controller_and_install_dns' \
    --exclude='windows/server/PS/install_and_enable_remote_desktop' \
    --exclude='windows/server/PS/install_windows_backup_server' \
    --exclude='windows/server/PS/liner for user account management' \
    --exclude='windows/server/PS/liner_to_Harden_a_Windows_Server_installation_in_powershell' \
    --exclude='windows/server/PS/list_all_users' \
    --exclude='windows/server/PS/selected_server_roles_and_features' \
    --exclude='windows/server/PS/set_powerplan_to_high_performance' \
    --exclude='windows/server/PS/setup_windows_backup_server,_and_create_a_backup' \
    --exclude='windows/server/active_directory/' \
    --exclude='windows/server/active_directory/A_forest_in_Active_Directory' \
    --exclude='windows/server/active_directory/Add_Debian_or_Ubuntu_Linux_Device_to_Windows_Active_Directory' \
    --exclude='windows/server/active_directory/Advanced_Setup_of_hMailServer_E-Mail_Server_Active_Directory_Authentication' \
    --exclude='windows/server/active_directory/Enabling_LDAP_Active_Directory_Authentication_in_Apache_Guacamole' \
    --exclude='windows/server/active_directory/Installing_Active_Directory_Domain_Services_(AD_DS)' \
    --exclude='windows/server/active_directory/Organizational_Units_(OUs)_and_Group_Policy' \
    --exclude='windows/server/active_directory/Troubleshooting_Active_Directory_Account_Lockouts' \
    --exclude='windows/server/active_directory/User_Management' \
    --exclude='windows/server/active_directory/Web_Based_Active_Directory_Management_with_ManageEngine_ADManager_Plus' \
    --exclude='windows/server/active_directory/install_&_configure_Active_Directory_Certificate_Services_role' \
    --exclude='windows/setups/' \
    --exclude='windows/setups/How_to_Install_PHP_for_Windows_Internet_Information_Services_(IIS)' \
    --exclude='windows/setups/Install_Chocolatey_on_Windows' \
    --exclude='windows/setups/Install_FreshRSS_-_RSS_Feed_Aggregator_-_on_Windows' \
    --exclude='windows/setups/Install_Hyper-V_on_Windows_10_or_11' \
    --exclude='windows/setups/Installing_Drupal_on_Windows' \
    --exclude='windows/setups/Installing_WebIssues_Bug_and_Enhancement_Tracker_on_Windows' \
    --exclude='windows/setups/Installing_and_Setting_Up_SSL_for_Subsonic_on_Windows' \
    --exclude='windows/setups/Set_Up_a_Static_Route_on_Windows' \
    --exclude='windows/setups/Setup_GoAccess_(CowAxess)_Web_Log_Analyzer_on_Windows' \
    --exclude='windows/setups/Setup_an_Official_Windows_10_VM_in_Under_10_Minutes' \
    --exclude='windows/setups/enable_telnet' \
    --exclude='windows/telnet/' \
    --exclude='windows/telnet/Use_Telnet_for_Fun_(Telehack)' \
    --exclude='windows/usfull/' \
    --exclude='windows/usfull/Shave_~3GB_From_Windows_OS_Drive' \
    --exclude='windows/usfull/Testing_Upgrading_Windows_10_to_Windows_11_In-Place' \
    --exclude='windows/usfull/make_terminal_app_work_as_admin_by_default' \
    --exclude='windows/usfull/speed_up_google_chrome_in_windows11' \
    --exclude='windows/web/' \
    --exclude='windows/web/Portable_Web_Server_Using_lighttpd_in_windows' \
    --exclude='windows/web/Web_Based_File_Management_with_PHP_and_Tiny_File_Manager_in_windows' \
    /mnt/c/study/ .

# Remove specific files that should not be pushed
rm -rf programming/python/apps/youtube/Playlists/substoplaylist/d.py /mnt/c/Users/micha/Shells/bash/.bashrc

# Stage all changes
git add -A

# Commit changes with a message; ignore error if there's nothing to commit
git commit -m "Auto commit" || true

# Run 'gitoken' command to set up Git authentication
gitoken

# Set up the remote origin, or update it if it already exists
git remote add origin https://github.com/Michaelunkai/study2.git 2>/dev/null || \
git remote set-url origin https://github.com/Michaelunkai/study2.git

# Pull latest changes from 'main' branch with rebase and autostash to handle any conflicts
git pull --rebase --autostash origin main || true  # Continue even if pull fails

# Run 'gitoken' again in case authentication is needed after pull
cat /mnt/c/backup/windowsapps/Credentials/github/accessToken.txt

# Force push changes to the 'main' branch
git push --force --set-upstream origin main

# Run 'down' command again
down

# Remove the 'study2' directory as cleanup
rm -rf /mnt/c/Users/micha/Downloads/study2

echo "All changes have been successfully pushed to the repository."
cmd.exe /c start chrome https://github.com/Michaelunkai/study2
