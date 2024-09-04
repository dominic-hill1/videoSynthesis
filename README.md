# Modular Video Synth
A full-stack application to emulate analogue video synthesis, using a node editor to generate GLSL shaders

## Showcase
![image](https://github.com/user-attachments/assets/05b4e7a7-8a6e-44ed-a274-314c3cb01eb2)

## Installation
The app has some awkward prerequisites, so I've made a install script to download it all for you.

### Windows
I've written this so someone without any command line experience can install the app easily. 
- Open a Windows PowerShell window (This can be done by searching up "Windows Powershell" on your PC)
- Type the command `wsl --install` and hit enter to run the command
- Run the command `wsl.exe --install Ubuntu-22.04`
- Run the command `wget https://raw.githubusercontent.com/dominic-hill1/videoSynthesis/main/install.sh`
- Run the command `chmod +x install.sh`
- Run the command `sudo ./install.sh`
- Occationally you'll get messages asking for confirmation to download something. Press "y" and enter to continue the installation

This should run a script which installs the app and all of its prerequisites.
This will take a while. It took 10 mins on my machine.
After it finishes running, the app should open.
If the install script doesn't work, have a look at install.sh and try to find the point where things went wrong or send me a message and I'll try to help out.

If you close the app and want to run it again, run these commands:
- `cd ~/of_v0.12.0_linux64gcc6_release/apps/myApps/videoSynthesis/GUI`
- `python3 main.py`

### Linux
- Run the commands:
  - `wget https://raw.githubusercontent.com/dominic-hill1/videoSynthesis/main/install.sh`
  - `chmod +x install.sh`
  - `sudo ./install.sh`
This should run a script which installs the app and all of its prerequisites.
This will take a while. It took 10 mins on my machine.
After it finishes running, the app should open.
If the install script doesn't work, have a look at install.sh and try to find the point where things went wrong or send me a message and I'll try to help out.

If you close the app and want to run it again, the main python file can be found at:
`of_v0.12.0_linux64gcc6_release/apps/myApps/videoSynthesis/GUI`

I know this is an inconvenient installation process. The app works on OpenFrameworks which is a big c++ framework. The next step in the project is migrating away from this framework to make the installation process easier. 

## Usage
- The node editor is used to define rules for the colour of a pixel depending on the position of that pixel
- Visuals are made in real time
- Numeric outputs (yellow nodes) must be connected with numeric inputs
- Video outputs (red nodes) must be connected with video inputs
- Press `ctrl+s` to send changes to output

### The modules
Oscillators:
- 3 types (Sin, Square and Circle)
- 3 inputs (2 for circle):
  -   Amplitude
  -   Rate
  -   Frequency
- Output: Oscillating number between 0-1

Luma Key:
- Similar to a green screen effect, but selects on brightness
- 3 inputs:
  -   Default video
  -   Alternative Video
  -   Sensitivity: control the sensitivity of the effect (0 will show one video, 1 will show the other)
- Output: Keyed video
  
X-Coordinate:
- An x-coordinate of a pixel, normalized between 0-1

Y-Coordinate:
- A y-coordinate of a pixel, normalized between 0-1


## Contact Me
[Email Me](mailto:dominic.hill.eng@gmail.com)<br>
[Connect on LinkedIn](https://www.linkedin.com/in/dominichill1)



