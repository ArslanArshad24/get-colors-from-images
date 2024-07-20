
file_name="yummy_macarons.jpg"
my_img=Image.open(file_name)
# sRGB_array=my_img/225
my_img_gray = my_img @ grey_vals
plt.imshow(np.flip(my_img_gray), cmap='gray')
# plt.imshow(np.rot90(my_img_gray))
plt.show()