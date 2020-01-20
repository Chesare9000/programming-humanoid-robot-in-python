


#only way to avoid redundancy
# Python program to explain os.symlink() method

# importing os module
import os


# Source file path
src = '../joint_control/angle_interpolation.py'

# Destination file path
dst = 'angle_interpolation.py'

# Create a symbolic link
# pointing to src named dst
# using os.symlink() method
os.symlink(src, dst)

print("Symbolic link created successfully")
