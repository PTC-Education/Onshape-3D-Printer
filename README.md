# Onshape-3D-Printer

This repo has python scripts that allow you to communicate between an Onshape document and an Octoprint server for starting 3D prints and controlling the removal of the 3D print with an AL5D robot arm.

![PrintRemoval](https://user-images.githubusercontent.com/54808875/135482423-0e2dea25-97e1-4e1e-8ade-f34e2ea6ab85.gif)


## Set up Pi
Start by flashing the latest version of Octopi onto your raspberry pi. Download the [image from here](https://octoprint.org/download/), unzip the file so you get the .img file, then flash it to an SD card with the raspberry pi imager. Once done flashing, unplug and replug the SD card so it shows up as "Boot", then change the "octopi_wpa_supplicant.conf" file to connect to your wifi network.

Once done, plug the SD card into your pi and power it on. When it starts up, you should be able to go to "octopi.local" on your wifi network and see the interface.

To access the RPi, run the following command (password should be default, "raspberry"). If you've done this before, you may need to clear the SSH keys with `ssh-keygen -R octopi.local`
```
ssh pi@octopi.local
```

Now you are in! Run the following two lines to finish setting up the Pi
```
sudo apt-get update --allow-releaseinfo-change
sudo apt-get upgrade
```

## Set up Onshape Repo
Start by cloning this repository, then going into the new folder

```
git clone https://github.com/PTC-Education/Onshape-3D-Printer
cd Onshape-3D-Printer
```

First run the following lines to install pip3 package installer
```
sudo apt-get -y install python3-pip
```

Then running this command to install all packages

```
pip3 install -r requirements.txt
```

You will also need to generate API Keys for Onshape and OctoPi, then add them to a file called "apikeys.py". 

- Go to [Onshape's Developer Portal](https://dev-portal.onshape.com/) and generate api keys
- Create a new appkey from the Octoprint interface [(instructions here)](https://docs.octoprint.org/en/master/bundledplugins/appkeys.html). You can put any sting in as your "application identifier" such as "Onshape".
- Create a new text file named "apikeys.py" (can run `sudo nano apikeys.py` to creater the file) with the content formatted as below, then make sure the file is in the same folder as the high level folder created once you cloned the repo.

**Note: It is very important to never share these keys**

```
access = "<access key here>"
secret = "<secret key here>"
OPappKey = "<OctoPi Appkey here>"
```

## Set up Slic3r

From terminal run
```
sudo apt-get update
sudo apt-get install slic3r-prusa
```

From your computer, **open a new terminal window** and copy a configuration file to the Pi with the following line (config file can be generated from the Prusa Slicer desktop app to make sure you have your settings correct for your printer)
```
scp Ender3config.ini pi@octopi.local:~/Onshape-3D-Printer
```

Then run the following command to slice your file (change your config.ini file and OnshapePart.stl if different)
```
/usr/bin/slic3r-prusa3d --load Ender3config.ini OnshapePart.stl
```

## Using the Code

The repo contains a number of python scripts that you can execute (or modify to develop your own custom integration) to integrate Onshape data with your 3D printing system. 

#### Automated export, slicing, and printing of parts
```
python3 ExportSliceUpload.py
```
This script first asks for a URL of an Onshape Part Studio, then checks if there are configurations and asks you to specify the configurations if there are any. It will then ask for a filename for the exported parts (ending in .stl), export all parts in the part studio, slice them using your pre-loaded configuration file (ending in .ini), then send the gcode file to Octopi and start the print.
