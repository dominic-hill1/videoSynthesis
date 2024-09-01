# Modular Video Synth
A full-stack application to emulate analogue video synthesis, using a node editor to generate GLSL shaders

## Showcase
![image](https://github.com/user-attachments/assets/05b4e7a7-8a6e-44ed-a274-314c3cb01eb2)

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



