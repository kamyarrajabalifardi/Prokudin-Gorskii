# Prokudin-Gorskii
In this problem we try to register 3 channels of images from ***Prokudin Gorskii*** collection. To do so, we shift channels on each other to get the best result. However, the images are so big in a way that finding the best shift is impractical. In this regard, we use a guassian image pyramid and we find the best shift in each level of pyramid and try to find the shift in the next level.

<p align="center">
  <img width="550" src="https://user-images.githubusercontent.com/46090276/195189711-91d0f8be-26e8-4858-8cb2-da8d6ac73ba7.jpg" alt="Alim_Khan">
</p>
As we can see after registration some unwanted artifacts are appeard on the border of image. In this vein, we apply sobel filter to detect horizontal and vertical edges. Next, we adopt a voting approach to remove these borders. Some of our results are shown below:

<p align="center">
  <img width="450" src="https://user-images.githubusercontent.com/46090276/195190698-f929d4bc-3ea6-4adc-977a-19393f67ecb2.jpg" alt="Amir">
</p>


<p align="center">
  <img width="450" src="https://user-images.githubusercontent.com/46090276/195190908-1dc776a6-07e1-456d-b898-3c12406555ed.jpg" alt="Mosque">
</p>

<p align="center">
  <img width="450" src="https://user-images.githubusercontent.com/46090276/195191183-03eec6d5-9fc3-488e-91ce-5e7196094856.jpg" alt="Train">
</p>
