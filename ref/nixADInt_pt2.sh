#/bin/bash
###############################################################################
 #
 # Part 2 of the *nix AD script.  SHOULD BE RUN FROM ADMIN USER
 #
 # Author: Mitchell Thompson
##

# Add sudo to domain admins
echo "%DOMAIN_Admins ALL=(ALL) ALL" >> /etc/sudoers

# Map the user share 
echo "Enter the server name"
read serverName

sudo apt-get install libpam-mount

echo "<volume user=\"*\"\nfstype=\"cifs\"\nserver=\"$serverName\"\npath=\"home/%
(DOMAIN_USER)\"\nmountpoint=\"~/H:_%(DOMAIN_USER)\"\n/>" 

echo "<volume user=\"*\"\nfstype=\"cifs\"\nserver=\"$serverName\"\npath=\"home/%(DOMAIN_USER)\"\nmountpoint=\"~/H:_%(DOMAIN_USER)\"\n/>" >> /etc/security/pam_mount.conf.xml

# Apply the user profile template
echo "session required pam_mkhomedir.so skel=/home/template/ umask=0022" >> etc/pam.d/common-session
