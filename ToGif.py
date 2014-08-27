#!/usr/bin/env python

# This tells Python to load the Gimp module 
from gimpfu import *
import os.path

# This generates the filename
def file_name(i):
	name = ""
	for num in range(4-numeber_of_digits(i)):
		name = name + "0"
	name = name + str(i)
	name = name +".png"
	return name

# This tells how many digits given number has. Works only for numbers less than 10 000.
def numeber_of_digits(i):
	if i<10:
		return 1
	if i<100:
		return 2
	if i<1000:
		return 3
	return 4

#This is the main method. Depending on the value of the toDo variable this evokes different functions
def Rbp_brand(toDo, ifile, logoPosition, number, idir, odir, filename,overlay):
	if toDo == "newGif":
		newGif(number, idir, odir, filename, overlay)
	if toDo == "brandPng":
		brandPng(ifile, logoPosition, odir, filename)
	if toDo == "brandGif":
		brandGif(ifile,logoPosition,odir,filename,overlay)

#The function for branding existing gif animation
def brandGif(ifile, logoPosition, odir, filename,overlay):
	image = pdb.file_gif_load(ifile,ifile)
	new_height = int(round(image.height*(600.0/image.width))) #calculate the new height of the gif
	newImage = gimp.Image(600,new_height,0)
	num_layers, layer_ids = pdb.gimp_image_get_layers(image) #extracting the layers from the existing gif

	#Here we set the offset for the logo depending on the position chosen by the user
	if logoPosition=="upperLeft":
		x_offset=20
		y_offset=20
	elif logoPosition=="upperRight":
		x_offset=497
		y_offset=20
	elif logoPosition=="downLeft":
		x_offset=20
		y_offset=newImage.height-39
	elif logoPosition=="downRight":
		x_offset=497
		y_offset=newImage.height-39

	#Branding each of the layers
	for i in range(num_layers):
		layer = image.layers[num_layers-i-1]
		pdb.gimp_layer_scale(layer,600,new_height, False)
		pdb.gimp_image_insert_layer(newImage,pdb.gimp_layer_new_from_drawable(layer, newImage), None, -1)
		martincho = pdb.gimp_file_load_layer(newImage, "rbp.png")
		pdb.gimp_image_insert_layer(newImage,martincho, None, -1)
		pdb.gimp_layer_scale(martincho, 83, 19, False)
		pdb.gimp_layer_set_offsets(martincho, x_offset, y_offset)
		layer = pdb.gimp_image_merge_down(newImage, martincho, 0)
	#Optimizing the animation
	#result = pdb.plug_in_animationoptimize(newImage, pdb.gimp_image_active_drawable(newImage))

	#change the image colors from RGB to Indexed (web optimized)
	pdb.gimp_image_convert_indexed(newImage, NO_DITHER, MAKE_PALETTE, 255, False, True, "")
	#finaly export the image in gif
	pdb.file_gif_save(newImage, pdb.gimp_image_active_drawable(newImage), odir+"/"+filename+".gif", odir+"/"+filename+".gif", 1, 1, 100, overlay+1)
	return



def brandPng(ifile, logoPosition, odir, filename):
	extension = os.path.splitext(ifile)[1]
	if extension == ".jpg":
		image = pdb.file_jpeg_load(ifile,ifile)
	if extension == ".png":
		image = pdb.file_png_load(ifile, ifile)
	if 600<image.height:
		pdb.gimp_image_scale(image, 600, image.height*(600.0/image.width))
	martincho = pdb.gimp_file_load_layer(image, "rbp.png")
	pdb.gimp_image_insert_layer(image,martincho,None,-1)
	pdb.gimp_layer_scale(martincho,83,19, False)
	if logoPosition=="upperLeft":
		pdb.gimp_layer_set_offsets(martincho,20,20)
	elif logoPosition=="upperRight":
		pdb.gimp_layer_set_offsets(martincho,image.width-103,20)
	elif logoPosition=="downLeft":
		pdb.gimp_layer_set_offsets(martincho,20,image.height-39)
	elif logoPosition=="downRight":
		pdb.gimp_layer_set_offsets(martincho,image.width-103,image.height-39)
	pdb.gimp_image_merge_down(image,martincho,0)
	pdb.file_png_save(image, pdb.gimp_image_active_drawable(image), odir+"/"+filename+".png", odir+"/"+filename+".png", False, 9, False, False, False, True, True)
	return


# This is the function that will perform actual actions
def newGif(number, idir, odir, filename, overlay) :
	# create a new image with 720p resolution
	img = gimp.Image(600,338,0)

	#load and brand each of the frames and add them to the newly created image as layers
	for i in range(1,number+1):
		layer = pdb.gimp_file_load_layer(img, idir+"/"+file_name(i))
		martincho = pdb.gimp_file_load_layer(img, "rbp.png")
		pdb.gimp_image_insert_layer(img,layer, None, -1)
		pdb.gimp_layer_scale(layer,600,338,False)
		pdb.gimp_image_insert_layer(img,martincho, None, -1)
		pdb.gimp_layer_scale(martincho, 83, 19, False)
		pdb.gimp_layer_set_offsets(martincho, 20, 20)
		layer = pdb.gimp_image_merge_down(img, martincho, 0)

	#scale the image so that it fits in Moodle
	pdb.gimp_image_scale(img, 600, 338)
	#optimize the image for gif animations and save the result in new image
	result = pdb.plug_in_animationoptimize(img, pdb.gimp_image_active_drawable(img))
	#change the image colors from RGB to Indexed (web optimized)
	pdb.gimp_image_convert_indexed(result, NO_DITHER, MAKE_PALETTE, 255, False, True, "")
	#finaly export the image in gif
	pdb.file_gif_save(result, pdb.gimp_image_active_drawable(result), odir+"/"+filename+".gif", odir+"/"+filename+".gif", 1, 1, 100, overlay+1)
	return

# This is the plugin registration function
register(
    "Rbp_brand",    
    "Image Branding",   
    "This script brand given media with the Robopartans Ltd. Logo. When the chosen image format is png,\
    the script imports the given image, brands it, rezises and saves it into png file. When the chosen image\
    format is gif the script imports the given number of frames from the Input Directory scales, brands, resizes and optimizes them for gif animation.",
    "Ivan Bozhilov", 
    "Robopartans Ltd.", 
    "May 2014",
    "<Toolbox>/Image Branding", 
    "*", 
    [(PF_RADIO, "toDo", "What will we do?", "newGif", (("Generate new gif animation", "newGif"),("Brand existing gif animation", "brandGif"),
    ("Brand existing png or jpeg image","brandPng"))),(PF_FILE, "ifile", "Input Image (only for branding existing images: *.jpg; *.png; *.gif.)", ""),
    (PF_RADIO, "logoPosition", "Where to put the logo?", "upperLeft", 
    (("Upper left corner", "upperLeft"), ("Upper right corner", "upperRight"), ("Down left corner", "downLeft"), ("Down right corner", "downRight"))),
    (PF_INT, "number", "Number of Frames (only for gif)", 60),
    (PF_DIRNAME, "idir", "Input Directory (only for gif)",  "/tmp"),
    (PF_DIRNAME, "odir", "Output Directory",  ""),
    (PF_STRING, "filename", "Output Filename (without the extension)", ""),
    (PF_TOGGLE, "overlay", "Replace? (only for gif)", 1)], 
    [],
    Rbp_brand,
    )

main()