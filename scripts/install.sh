#!/usr/bin/env bash


ReplaceAnyTextOnLine(){
# ReplaceTextLine /textfile bob brian
#REMEMBER!! The & symbol can't be in any of the strings as SED is using it for separating. Can change it if need be
        egrep -i "$2" $1 >> /dev/null
        if [ $? -eq 0 ]; then
                sed -i "s&.*$2.*&$3&g" $1
                return 0
        else
                echo "$3" >> $1
                return 1
        fi

}


LOGO=$(cat <<-END

  _____  _  _   _        _      _____
 |  __ \(_)| \ | |      | |    / ____|
 | |__) |_ |  \| |  ___ | |_  | (___    ___  _ __  ___   ___  _ __   ___
 |  ___/| || . ` | / _ \| __|  \___ \  / __|| '__|/ _ \ / _ \| '_ \ / __|
 | |    | || |\  ||  __/| |_   ____) || (__ | |  |  __/|  __/| | | |\__ \
 |_|    |_||_| \_| \___| \__| |_____/  \___||_|   \___| \___||_| |_||___/


[49m[K[0m[24C[48;5;231m       [49m
[22C[48;5;231m   [48;5;188m [48;5;16m   [48;5;231m    [49m
[22C[48;5;231m  [48;5;16m  [48;5;149m  [48;5;155m [48;5;16m [48;5;102m [48;5;231m  [49m
[19C[48;5;231m      [48;5;16m     [48;5;231m   [49m
[8C[48;5;231m       [2C   [48;5;16m      [48;5;231m          [49m
[6C[48;5;231m    [48;5;16m    [48;5;231m     [48;5;16m  [48;5;149m   [48;5;16m  [48;5;231m      [48;5;16m  [48;5;231m    [49m
[5C[48;5;231m   [48;5;16m  [48;5;149m   [48;5;58m [48;5;16m       [48;5;149m   [48;5;16m        [48;5;149m  [48;5;16m  [48;5;231m   [49m
[5C[48;5;231m   [48;5;16m [48;5;58m [48;5;149m    [48;5;16m  [48;5;231m     [48;5;16m   [48;5;231m     [48;5;16m  [48;5;149m   [48;5;16m  [48;5;231m   [49m
[5C[48;5;231m   [48;5;16m       [48;5;231m   [48;5;16m      [48;5;188m [48;5;231m     [48;5;188m [48;5;16m    [48;5;231m       [49m
[4C[48;5;231m           [48;5;16m   [48;5;168m      [48;5;53m [48;5;16m   [48;5;231m      [48;5;16m      [48;5;59m [48;5;231m   [49m
[2C[48;5;231m    [48;5;102m [48;5;145m [48;5;231m     [48;5;16m   [48;5;168m           [48;5;16m  [48;5;231m    [48;5;16m  [48;5;168m     [48;5;16m  [48;5;231m   [49m
[48;5;231m   [48;5;16m   [48;5;168m [48;5;204m [48;5;16m   [48;5;231m  [48;5;16m [48;5;89m [48;5;168m             [48;5;16m  [48;5;102m [48;5;16m   [48;5;168m      [48;5;204m [48;5;16m [48;5;188m [48;5;231m  [49m
[48;5;231m   [48;5;16m [48;5;132m [48;5;168m    [48;5;52m [48;5;16m    [48;5;168m              [48;5;16m  [48;5;231m   [48;5;16m  [48;5;168m     [48;5;16m  [48;5;231m   [49m
[48;5;231m   [48;5;16m  [48;5;204m [48;5;168m  [48;5;16m   [48;5;231m  [48;5;16m [48;5;168m              [48;5;16m  [48;5;231m    [48;5;145m [48;5;16m     [48;5;231m    [49m
[1C[48;5;231m    [48;5;16m   [48;5;145m [48;5;231m    [48;5;16m  [48;5;204m [48;5;168m           [48;5;16m  [48;5;231m  [48;5;16m     [48;5;231m      [49m
[3C[48;5;231m     [48;5;16m     [48;5;231m [48;5;16m   [48;5;131m [48;5;168m       [48;5;16m   [48;5;59m [48;5;16m  [48;5;168m    [48;5;204m [48;5;16m  [48;5;231m   [49m
[3C[48;5;231m   [48;5;16m  [48;5;168m    [48;5;204m [48;5;16m  [48;5;231m  [48;5;16m        [48;5;231m   [48;5;16m  [48;5;168m       [48;5;16m [48;5;145m [48;5;231m  [49m
[3C[48;5;231m  [48;5;16m  [48;5;168m       [48;5;16m  [48;5;231m      [48;5;16m  [48;5;145m [48;5;231m    [48;5;16m  [48;5;168m     [48;5;16m  [48;5;231m   [49m
[3C[48;5;231m  [48;5;16m  [48;5;168m       [48;5;16m  [48;5;231m   [48;5;16m   [48;5;204m [48;5;168m [48;5;204m [48;5;16m   [48;5;231m  [48;5;16m       [48;5;231m   [49m
[3C[48;5;231m   [48;5;16m   [48;5;168m   [48;5;89m [48;5;16m  [48;5;231m  [48;5;16m  [48;5;53m [48;5;168m       [48;5;52m [48;5;16m [48;5;231m          [49m
[4C[48;5;231m    [48;5;188m [48;5;16m   [48;5;145m [48;5;231m    [48;5;16m  [48;5;168m         [48;5;16m  [48;5;231m  [49m
[7C[48;5;231m       [1C  [48;5;16m  [48;5;168m        [48;5;204m [48;5;16m  [48;5;231m  [49m
[15C[48;5;231m   [48;5;16m   [48;5;168m     [48;5;16m   [48;5;231m   [49m
[16C[48;5;231m     [48;5;16m     [48;5;231m    [49m
[19C[48;5;231m         [0m

END
)



#echo "$LOGO"

echo ""
echo ""
echo "#################################################################################################################"
echo "This script will install the PiNet screens application."
echo "Note that the defaults used by the application assume the only PiNet Pis being used are used for display screens."

read -r -p "Are you sure? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        echo "Installing..."
        ;;
    *)
        exit 1
        ;;
esac

cd ../

apt install python3-venv -y

mkdir /opt/PiNet-Screens
cp -r * /opt/PiNet-Screens
cp /opt/PiNet-Screens/secrets/config_example.py /opt/PiNet-Screens/secrets/config.py

python3 -m venv /opt/PiNet-Screens/venv
source /opt/PiNet-Screens/venv/bin/activate
pip3 install -r /opt/PiNet-Screens/requirements.txt
python3 /opt/PiNet-Screens/scripts/create_user.py
deactivate

useradd -r pinetscreens

cp scripts/pinetscreens.service /etc/systemd/system/pinetscreens.service


sudo systemctl start pinetscreens
sudo systemctl enable pinetscreens

sensible-browser localhost:80


# Setup shared folder that is used

mkdir /home/shared/screens
mkdir /home/shared/screens/scripts/
chown root: /home/shared/screens
chmod 0700 /home/shared/screens
ReplaceAnyTextOnLine /usr/local/bin/bindfs-mount "/home/shared/screens" "bindfs -o perms=0775,force-group=teacher /home/shared/screens /home/shared/screens"