# Image and imread for manipulate and access the images.
from PIL import Image
from skimage.io import imread

# Numpy for manipulate, access and optimise operations on matrices and arrays.
import numpy as np

#Matplotlib.pyplot for plotting.
import matplotlib.pyplot as plt

# Defining the functions

def image_to_binary_matrix(image_path, threshold=128):
    # Load the image
    image = Image.open(image_path)
    
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    # Convert the grayscale image to a numpy array
    image_array = np.array(grayscale_image)
    
    # Binarize the array. The threshold is on 128 as between white and black values.
    binary_array = (image_array < threshold).astype(int)
    
    return binary_array

def jaccard_index(binary_matrix_1, binary_matrix_2):
    # Convert matrices to numpy arrays
    mat1 = np.array(binary_matrix_1)
    mat2 = np.array(binary_matrix_2)
    
    # Calculate intersection and union
    intersection = np.logical_and(mat1, mat2).sum()
    union = np.logical_or(mat1, mat2).sum()
    
    # Avoid division by zero
    if union == 0:
        return 0  
    
    # Compute Jaccard index
    jaccard = intersection / union
    
    return jaccard

#Name of the three samples images
all_samples = ["Circle", "Neuron", "Random"]

# List to store images and binary matrices for each sample
binary_matrices = []  
images=[]

# Loop to generate the binary matrix and plot both real and binary images for each sample
for sample in all_samples:
    image_path = "./" + sample + ".png"
    image = imread(image_path)
    
    #Generate the binary matrix from the image of each sample
    binary_matrix = image_to_binary_matrix(image_path)
    
    #Add the image and binary matrix of each sample to the list
    images.append(image)
    binary_matrices.append(binary_matrix)  

# Decide the number of subplots and the size of the figure
fig, axes = plt.subplots(2, len(all_samples), figsize=(7,6)) 

#Loop on number of samples to populate the subplots
id_sample=0
for index in range(len(all_samples)):
    
    ## First row of the subplots
    #Plot the image of the current sample
    axes[0, index].imshow(images[id_sample])
    #Plot the image title of the current sample
    axes[0, index].set_title(f'{all_samples[id_sample]} Real Image', fontsize=14)
    #Set axis of the image to off
    axes[0, index].axis('off')

    ## Second row of the subplots
    #Plot the binary matrix of the current sample
    axes[1, index].imshow(binary_matrices[id_sample], cmap='Greys')
    #Plot the binary matrix title of the current sample
    axes[1, index].set_title(f'{all_samples[id_sample]} Binary Matrix', fontsize=14)
    #Set axis of the binary matrix to off
    axes[1, index].axis('off')
    
    #Increase id_sample to go to the next sample and continue
    id_sample=id_sample+1
    
plt.tight_layout()
plt.show()

# With np we can create a square matrix of zeros to store the Jaccard indices
jaccard_matrix = np.zeros((len(binary_matrices), len(binary_matrices)))
    
# Here we populate the Jaccard matrix with Jaccard index between all the pairs of samples
for row in range(len(binary_matrices)):
    for column in range(len(binary_matrices)):
        jaccard = jaccard_index(binary_matrices[column], binary_matrices[row])
        jaccard_matrix[column][row] = jaccard

#Size of the plot
plt.figure(figsize=(5, 5))

#Show the jaccard matrix
plt.imshow(jaccard_matrix, cmap='magma', interpolation='nearest') 

#Style the x and y ticks
plt.xticks(range(len(all_samples)), all_samples, fontsize=14)
plt.yticks(range(len(all_samples)), all_samples, fontsize=14)

#Add the title
plt.title('Jaccard Index Matrix', fontsize=24)

#Style the values of jaccard index for each entry
for i in range(len(all_samples)):
    for j in range(len(all_samples)):
        plt.text(j, i, f"{jaccard_matrix[i][j]:.2f}",
                 ha='center', va='center', color='black' if jaccard_matrix[i][j] > 0.5 else 'white', 
                 fontsize=25)
plt.tight_layout()
plt.show()

