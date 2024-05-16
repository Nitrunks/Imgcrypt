from cryptography.fernet import Fernet
import os
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw,UnidentifiedImageError
from PIL.ExifTags import TAGS
import argparse
import matplotlib.pyplot as plt


#gets directories from user's pc
global starting_directory, input_directory, output_directory, watermark_directory
starting_directory= os.getcwd()
input_directory =starting_directory+"/input"
output_directory =starting_directory+"/output"
watermark_directory =starting_directory+"/watermark"
keys_directory=starting_directory+"/keys"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
if not os.path.exists(input_directory):
    os.makedirs(input_directory)
if not os.path.exists(watermark_directory):
    os.makedirs(watermark_directory)
if not os.path.exists(keys_directory):
    os.makedirs(keys_directory)


def variable_calling():
    Flag=True
    print("Welcome to imgcrypt, please select one of the following options")
    print("=============================================")
    while Flag:
        user_input=str(input("Press 1 to use the encryptor\nPress 2 to remove/extract metadata from image\nPress 3 to use steganography\nPress 4 to add  watermark\nPress 0 to exit\n"))
        if user_input=="1":
            encryption()
        elif user_input=="2":
            metadata()
        elif user_input=="3":
            steganography()
        elif user_input=="4":
            create_watermark_image()
        elif user_input=="0":
            Flag= False
        else:
            print("Please enter a correct value")
        




#encryptor
def encryption():
    Flag=True
    while Flag:
        encryptmessage=str(input("Press 1 to generate a new key\nPress 2 to encrypt using a key\nPress 3 to decrypt using a key\nPress 0 to exit\n"))
        if encryptmessage=="1":
            key = Fernet.generate_key()
            os.chdir(keys_directory)
 
            # string the key in a file
            keygeneration=str(input("What name would you like to give to your key?\n"))
            with open(keygeneration+".key", 'wb') as filekey:
                filekey.write(key)
            print("Success")
            print("=============================================")
        elif encryptmessage=="2":
            keyopen=str(input("Please enter the name of the encryption key you'd like to open\n"))
            os.chdir(keys_directory)
            with open(keyopen+".key", 'rb') as filekey:
                key = filekey.read()
            filename=str(input("Please enter the file you'd like to encrypt (include the file's extension)\n"))
            os.chdir(input_directory)
            with open(filename, 'rb') as file:
                original = file.read()  
            fernet = Fernet(key)
            encrypted = fernet.encrypt(original)
            os.chdir(output_directory)
            # opening the file in write mode and 
            # writing the encrypted data
            with open(filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            print("Success")
            print("=============================================")

        elif encryptmessage=="3":
            keyopen=str(input("Please enter the name of the encryption key you'd like to open\n"))
            os.chdir(keys_directory)
            with open(keyopen+".key", 'rb') as filekey:
                key = filekey.read()
            fernet = Fernet(key)
            filename=str(input("Please enter the file you'd like to encrypt (add the files extension)\n"))
            os.chdir(input_directory)
            with open(filename, 'rb') as enc_file:
                encrypted = enc_file.read()
            decrypted = fernet.decrypt(encrypted)
            os.chdir(output_directory)
            with open(filename, 'wb') as dec_file:
                dec_file.write(decrypted)
            print("Success")
            print("=============================================")

        elif encryptmessage=="0":
            Flag=False
            print("=============================================")
        else:
            print("Please enter a correct value")

#metadata extractor/delete
def metadata():
    Flag=True
    while Flag:
        metadatamessage=str(input("Press 1 to extract metadata\nPress 2 to remove metadata\nPress 3 to do both\nPress 0 to exit\n"))
        if metadatamessage=="1":
            imagename=str(input("Enter the image you'd like to remove the metadata from\n"))            
            os.chdir(input_directory)
            image = Image.open(imagename) # open the image
            exifdata = image.getexif() # extracting the exif metadata            
            exifdata = image.getexif() # extracting the exif metadata
            os.chdir(output_directory) #saves metadata in txt file
            savedimage= open(imagename[0:-3]+"txt","w")
            for tagid in exifdata: # looping through all the tags present in exifdata
                tagname = TAGS.get(tagid, tagid) # getting the tag name instead of tag id
                value = exifdata.get(tagid) # passing the tagid to get its respective value
                savedimage.write(f"{tagname:25}: {value}\n")
                print(f"{tagname:25}: {value}")
            savedimage.flush()
            savedimage.close
            print("Success")
            print("=============================================")
        elif metadatamessage=="2":
            imagename=str(input("Enter the image you'd like to remove the metadata from\n"))
            os.chdir(input_directory)
            image_file = open(imagename)
            image = Image.open(imagename) # open the image
            # next 3 lines strip exif
            image_data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(image_data)
            os.chdir(output_directory)
            image_without_exif.save(u"clean_{}".format(imagename))
        elif metadatamessage=="3":
            imagename=str(input("Enter the image you'd like to remove the metadata from\n"))          
            os.chdir(input_directory)
            image = Image.open(imagename) # open the image
            exifdata = image.getexif() # extracting the exif metadata            
            exifdata = image.getexif() # extracting the exif metadata
            os.chdir(output_directory) #saves metadata in txt file
            savedimage= open(imagename[0:-3]+"txt","w")
            for tagid in exifdata: # looping through all the tags present in exifdata
                tagname = TAGS.get(tagid, tagid) # getting the tag name instead of tag id
                value = exifdata.get(tagid) # passing the tagid to get its respective value
                savedimage.write(f"{tagname:25}: {value}\n")
                print(f"{tagname:25}: {value}")
            savedimage.flush()
            savedimage.close
            os.chdir(input_directory)
            image_file = open(imagename)
            image = Image.open(imagename) # open the image
            # next 3 lines strip exif
            image_data = list(image.getdata())
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(image_data)
            os.chdir(output_directory)
            image_without_exif.save(u"clean_{}".format(imagename))        
            print("Success")
            print("=============================================")
        elif metadatamessage=="0":
            Flag=False
            print("=============================================")
        else:
            print("Please enter a correct value")




# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
 
        # list of binary codes
        # of given data
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
 
# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
 
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Encode data into image
def encode():
    img = input("Enter image name(with extension) : ")
    os.chdir(input_directory)
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Enter the name of the new image(with extension)\n")
    os.chdir(output_directory)
    if ".jpg" in new_img_name:
        new_img_name=new_img_name[0:-3]+"jpeg" #python doesn't like .jpg extensions
        
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    print("Success")
    print("=============================================")
 
# Decode the data in the image
def decode():
    os.chdir(input_directory)
    img = input("Enter image name(with extension)\n")
    image = Image.open(img, 'r')
    
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
    print("Success")
    print("=============================================")
# Main Function
def steganography():
    Flag=True
    while Flag:
        a = str(input("Press 1 to encode a message\nPress 2 to decode a message\nPress 0 to exit\n"))
        if (a == "1"):
            encode() 
        elif (a == "2"):
            print("Decoded Word :  " + decode())
        elif (a=="0"):
            Flag=False
        
        else:
            print("Please enter a correct value")
 
def create_watermark_image():
    inputImage=str(input("Enter the name of the file\n"))
    outputImage=str(input("Enter the name of the new image with the watermark(include extension)\n"))
    if ".jpg" in outputImage:
        outputImage=outputImage[0:-3]+"jpeg" #python doesn't like .jpg extensions
    watermarkImage=str(input("Enter the name of the watermark\n"))

    
    potition=()
    #gets the position of the watermark
    a=int(input("Enter value of x\n"))
    b=int(input("Enter value of y\n"))
    lista=[]
    lista.append(a)
    lista.append(b)
    potition=tuple(lista)
    os.chdir(input_directory)
    baseImage = Image.open(inputImage)
    os.chdir(watermark_directory)

    #creates a copy of the original watermark to fix the transparency that gets affected by the putalpha command
    watermark = Image.open(watermarkImage)
    watermark2=watermark.copy()
    opacity=int(input("Enter opacity\n"))
    watermark2.putalpha(opacity)
    watermark.paste(watermark2,watermark)
    baseImage.paste(watermark, potition, mask=watermark)

    os.chdir(output_directory)
    baseImage.save(outputImage)
    print("Success")
    print("=============================================")
    return baseImage


variable_calling()
