# Sunset Predictor
### By Matthew Wilcox & Hanna Butsko

## Background
This project uses Generative Adversarial Networks to build sky representations at Sunset. We built a GAN to just make sky images at sunset as well as a conditional GAN. The GAN was built based off of the DCGAN Pytorch Tutorial[^1]. 

## Data
We collected Image data from the NREL Solar Radiation Research Laboratory in Golden, Colorado [^2]. 
Our Weather data was collected from Visual Crossing [^3].

## GAN
Here is our Sunset Image GAN. It is built off of Random Noise to generate the images.

[[Insert Image Results Here]]

## Conditional GAN

Here is our Sunset Image Conditional GAN. It uses the weather conditions as predicted by the Sunset Images.

[[Insert Image Results Here]]



# Presentation

Additionally, our presentation can be viewed [here](https://docs.google.com/presentation/d/1snyJtPPNObgghG0M7vTY_YhoZyB9Emy9/edit?usp=sharing&ouid=109507058081018285692&rtpof=true&sd=true)!


[^1]:https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html
[^2]: Andreas, A.; Stoffel, T.; (1981). NREL Solar Radiation Research Laboratory (SRRL): Baseline Measurement System (BMS); Golden, Colorado (Data); NREL Report No. DA-5500-56488. http://dx.doi.org/10.5439/1052221 
[^3]: https://www.visualcrossing.com/
