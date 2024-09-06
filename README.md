⬇️⬇️ Installation instructions below ⬇️⬇️
# Modular Video Synth
A full-stack application to emulate analogue modular video synthesis, using a node editor to generate GLSL shaders

![image](https://github.com/user-attachments/assets/05b4e7a7-8a6e-44ed-a274-314c3cb01eb2)

## Installation
The app has some awkward prerequisites, so I've made an install script to download it all for you.

It takes a while, but only takes a few commands

### Linux (recommended)
- Run the commands:
  - `wget https://raw.githubusercontent.com/dominic-hill1/videoSynthesis/main/install.sh`
  - `chmod +x install.sh`
  - `sudo ./install.sh`
This should run a script which installs the app and all of its prerequisites.
**This will take a while**. It took 10 mins on my machine.
After it finishes running, the app should open.
If the install script doesn't work, have a look at install.sh and try to find the point where things went wrong or send me a message and I'll try to help out.

If you close the app and want to run it again, the main python file can be found at:
`of_v0.12.0_linux64gcc6_release/apps/myApps/videoSynthesis/GUI`

### Windows
I've written this so someone without any command line experience can install the app easily. If you've worked with WSL before you'll know what to do for the first section. 
- Open a Windows PowerShell window (This can be done by searching up "Windows Powershell" on your PC)
- Type the command `wsl --install` and hit enter to run the command and follow the instructions. More info [here](https://learn.microsoft.com/en-us/windows/wsl/install)
- You might need to run the command `wsl.exe --install Ubuntu-22.04`
- Restart your computer
- You should now see a terminal that looks like this:
- ![image](https://github.com/user-attachments/assets/853d670b-e612-4889-a3d6-e979bbe16b2c)
- In this terminal, run the commands:
- `wget https://raw.githubusercontent.com/dominic-hill1/videoSynthesis/main/install.sh`
- `chmod +x install.sh`
- `sudo ./install.sh`
- Occationally you'll get messages asking for confirmation to download something. Press "y" and enter to continue the installation

This should run a script which installs the app and all of its prerequisites.
**This will take a while**. It took 10 mins on my machine.
After it finishes running, the app should open.
If the install script doesn't work, have a look at install.sh and try to find the point where things went wrong or send me a message and I'll try to help out.

If you close the app and want to run it again, run these commands:
- `cd ~/of_v0.12.0_linux64gcc6_release/apps/myApps/videoSynthesis/GUI`
- `python3 main.py`


I know this is an inconvenient installation process. The app works on OpenFrameworks which is a big c++ framework. The next step in the project is migrating away from this framework to make the installation process easier. 

## Getting started
I'd recommend copying this layout, then messing around with it and expanding.
![image](https://github.com/user-attachments/assets/a1a8aa60-df48-4923-a0e2-24f8da429570)

You can get modules by clicking the buttons in the sidebar to spawn them in. 

You get the sliders by dragging them off the pile already on the canvas. 

Hit `ctrl+s` when it's all set up to show the video output

Let's talk through what's happening here:

- We start with a video module. This plays video clips of 2001 A Space Odyssey on repeat.
- That signal is passed into a zooming feedback module. This module will perform the equivalent of pointing a camera at its own output screen, where it looks like it repeats forever.
- This signal is then passed into a colour displacer, which will change the colours of the video signal according to its 3 inputs.
- This signal is then passed into a luma keying module. This performs the equivalent of a green screen effect, but based on brightness instead of greenness. It will choose between the 2 video inputs based on the brighter pixels on each video.
- This is then passed to the output, which is shown on your screen

You can move the sliders around and work out how the video changes. 

Next, try to add more modules to the layout and experiment.

## Usage
- The node editor is used to define rules for the colour of a pixel depending on the position of that pixel
- Visuals are made in real time
- Numeric outputs (yellow nodes) must be connected with numeric inputs
- Video outputs (red nodes) must be connected with video inputs
- Only one connection is allowed into an input, but multiple connections can come out of an output
- Press `ctrl+s` to send changes to output
- Hold `ctrl+click` and drag to create a line to delete connections


### The modules
Oscillators:
- 3 types (Sin, Square and Circle)
- 3 inputs (2 for circle):
  -   Amplitude
  -   Rate
  -   Frequency
- Output: Oscillating number between 0-1

Video input:
- This plays video clips of 2001 A Space Odyssey on repeat.
- The video can be changed by replacing movie.mp4 in `bin/data/`

Audio input:
- Microphone volume normalised between 0-1

Colour Mixer:
- Takes red, green and blue channels to create a full video.

Colour Addition:
- Add two colour channels

Colour Multiplication:
- Multiply two colour channels

Colour displacement:
- Takes a video input and has 3 colour channels which can be displaced.

Luma Keying:
- Similar to a green screen effect, but selects pixels based on brightness
- 3 inputs:
  -   Default video
  -   Alternative Video
  -   Sensitivity: control the sensitivity of the effect (0 will show one video, 1 will show the other)
- Output: Keyed video

Zooming feedback:
- Takes a video, and does the equivalent of pointing a camera at its own output.
- Zoom factor controls the strength of the effect

X-Coordinate:
- An x-coordinate of a pixel, normalized between 0-1

Y-Coordinate:
- A y-coordinate of a pixel, normalized between 0-1

Time:
- A constantly increasing value

Arthithmetic modules:
- Addition
- Multiplication
- Negation

## Acknowledgements
Thanks to [Pavel Křupala](https://gitlab.com/pavel.krupala) for his node editor tutorials for helping me to get started on the node editor

Thanks to [Andrei Jay](https://andreijaycreativecoding.com/) for his insight into emulating analogue video synthesis


## Contact Me
[Email Me](mailto:dominic.hill.eng@gmail.com)<br>
[Connect on LinkedIn](https://www.linkedin.com/in/dominichill1)



