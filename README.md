# Onshape-3D-Printer

## Set up Pi
Start by flashing the latest version of Octopi onto your raspberry pi. Download the [image from here](https://octoprint.org/download/), unzip the file so you get the .img file, then flash it to an SD card with the raspberry pi imager. Once done flashing, unplug and replug the SD card so it shows up as "Boot", then change the "octopi_wpa_supplicant.conf" file to connect to your wifi network.

Once done, plug the SD card into your pi and power it on. When it starts up, you should be able to go to "octopi.local" on your wifi network and see the interface.

To access the RPi, run the following command (password should be default, "raspberry")
```
ssh pi@octopi.local
```

Now you are in and can start setting up the automation

## Set up Onshape Repo
Start by cloning this repository, then going into the new folder

```
git clone https://github.com/PTC-Education/Onshape-3D-Printer
cd Onshape-3D-Printer
```

Then running this command to install all packages

```
pip3 install -r requirements.txt
```

## Set up Slic3r

From terminal run
```
sudo apt-get update
sudo apt-get install slic3r-prusa3d
```

From your computer, copy a configuration file to the Pi with the following line (config file can be generated from the Prusa Slicer desktop app to make sure you have your settings correct for your printer)
```
scp colabConfigBundle.ini pi@octopi.local:~/Documents
```

Then run the following command to slice your file (change your config.ini file and OnshapePart.stl if different)
```
/usr/bin/slic3r-prusa3d --load configtest4.ini OnshapePart.stl
```