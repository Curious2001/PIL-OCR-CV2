#My Code
import PIL
from PIL import Image,ImageEnhance,ImageDraw,ImageFont
# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')

# build a list of 9 images which have different brightnesses
#enhancer=ImageEnhance.Brightness(image)
images=[]
fnt = ImageFont.truetype('readonly/fanwood-webfont.ttf', 50)
matrices = []
i = 0
while i<=8:
    R=1; G=1; B=1;
    if i%3==0:
        var=0.1
    elif i%3==1:
        var=0.5
    elif i%3==2:
        var=0.9
    else:
        print("Black hole!")
    if i//3==0:
        R=var
    elif i//3==1:
        G=var
    elif i//3==2:
        B=var
    else:
        print("Hakuna Matata!")
    matrices.append((R,0,0,0,0,G,0,0,0,0,B,0))
    i = i+1
#print(matrices)
image=image.convert('RGB')
i = 0
while i<=8:
    image3 = Image.new(mode = "RGB", size = (800,50), color = "black")
    draw = ImageDraw.Draw(image3)
    w = "channel "+str(int(i//3))+" intensity "+str(0.1+(0.4*(i%3)))
    draw.text((0,10), w, font=fnt, fill=(255,255,255))
    result=PIL.Image.new(image.mode, (image.width,image.height+50))
    result.paste(image, (0, 0))
    result.paste(image3, (0, 450))
    images.append(result.convert('RGB',matrices[i]))
    i = i+1
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)
