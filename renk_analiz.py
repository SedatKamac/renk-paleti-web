from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


image = Image.open("ornek.jpg")
image = image.resize((150, 150))  


pixels = np.array(image).reshape(-1, 3)


k = 5  
kmeans = KMeans(n_clusters=k)
kmeans.fit(pixels)

colors = kmeans.cluster_centers_.astype(int)
hex_colors = [rgb_to_hex(c) for c in colors]


plt.figure(figsize=(8, 2))
for i, color in enumerate(colors):
    plt.subplot(1, k, i+1)
    plt.axis("off")
    plt.imshow([[color]])
plt.show()

print("Renkler (HEX):")
for h in hex_colors:
    print(h)
