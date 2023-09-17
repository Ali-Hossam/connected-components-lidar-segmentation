from cc_segmentation import alg
import matplotlib.pyplot as plt
import numpy as np
import os

# params
txt_name = "scans_test.txt"
lidar_max_range_ = 20

# generate data
data_size = np.random.randint(lidar_max_range_, lidar_max_range_ ** 2)
num_of_zeros = np.random.randint(0.5 * data_size, 0.7 * data_size)
data_generated = np.zeros(data_size)

for i in range(data_size - num_of_zeros):
    idx = np.random.randint(0, data_size)
    data_generated[idx] = np.random.uniform(5, lidar_max_range_ / 2)

# save generated data
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)
np.savetxt("txt_files\\" + txt_name, data_generated)

# test the algorithm on the generated data
final_file_name = "txt_files\\cells_test.txt"
symbolic_img = alg(txt_name, lidar_max_range_, final_file_name)

# get indices of segments in the image and scatter plot them
indices = np.where(symbolic_img != 0)
indices1 = np.where(symbolic_img == 0)
plt.scatter([symbolic_img.shape[1] / 2], [symbolic_img.shape[0] / 2], marker="^", s=[50])
plt.scatter(indices[1], indices[0], c=symbolic_img[indices], cmap="tab10")
plt.xlim(0, lidar_max_range_ * 2)
plt.ylim(0, lidar_max_range_)

# save fig
fig_name = "images/fig" + str(np.random.randint(0, 1000))
plt.savefig(fig_name)
plt.show()

