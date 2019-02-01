# SET UP OSG CONNECT TO TRANSFER FILES
# NOT MEANT TO ACTUALLY BE RUN

# Vist https://globus.rcc.uchicago.edu
# Login with you UChicago credentials
# Click "Endpoints"
# Click " + add Globus Connect Personal endpoint
# Click Generate Setup Key

# On la2:
cd ~
wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
gunzip -c globusconnectpersonal-latest.tgz | tar -xf -
cd globusconnectpersonal-2.3.6
./globusconnectpersonal -setup <key from globus.rcc>
./globusconnectpersonal -start &

# If this does not work for you, please backup your .bashrc and .bash_profile and
# copy the defaults from /etc/skel, log out completely, log back in and try
# again.




