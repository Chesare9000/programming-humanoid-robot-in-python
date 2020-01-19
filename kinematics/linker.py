


#only way to avoid redundancy
# Python program to explain os.symlink() method

# importing os module
import os


# Source file path
src = '../joint_control/keyframes'

# Destination file path
dst = 'keyframes'

# Create a symbolic link
# pointing to src named dst
# using os.symlink() method
os.symlink(src, dst)

print("Symbolic link created successfully")
