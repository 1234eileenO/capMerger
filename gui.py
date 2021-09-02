# Written by Eileen O
import os
import time
import shutil
import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from PIL import ImageGrab, Image
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = ROOT_DIR / Path("./capturedImgs")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
    
def setDestDir():
    # Ask for the output directory
    folder_selected = filedialog.askdirectory()

    if folder_selected == "": 
        return
    destFolderTxt.delete(0, END)
    destFolderTxt.insert(0, folder_selected)

def validateInput():

    # Check if there is an empty input
    if(destFolderTxt.index("end") ==0 or entry_1.index("end") == 0 or entry_2.index("end")==0):
        showError("Please fill in all the input.")
        return False
    
    # Check if designated output folder directory exists
    if not (Path(destFolderTxt.get()).exists()):
        showError("Please fill correct directory.")
        return False

    # Check if the time input is number
    if not(entry_1.get().isdigit() or entry_2.get().isdigit()):
        showError("Please enter number between 1 - 60. \n Enter 0 for empty entry.")
        return False

    minInput = int(entry_1.get())
    secInput = int(entry_2.get())
    # Check the min and max value of time
    if(minInput>60 or minInput<0 or secInput>60 or secInput<0):
        showError("Please enter number between 1 - 60. \n Enter 0 for empty entry.")
        return False
        
    # Start counting down to five if all input is valid
    countDown(5) 

def countDown(count):

    if(count >= 0):
        canvas.after(1000, countDown, count-1)
        countDownLabel['text'] = "Screen capture will start in " + str(count) + " seconds."

    if( count < 0):    
        countDownLabel['text'] = "In progres"
        captureImgs()

def captureImgs():
    # List that contains the path of captured images     
    list_file = []
    
    # If it doesn't exist, create a temporary folder to save captured images 
    if CAPTURE_DIR.exists() == FALSE:
        os.mkdir(CAPTURE_DIR)

    totalSec = int(entry_2.get()) + 60*(int(entry_1.get()))
     
    for i in range(0, totalSec):
        # Screen captures the current screen
        img = ImageGrab.grab() 
        dest_path = os.path.join(CAPTURE_DIR, "capture{}.png".format(i))
        img.save(dest_path)
        list_file.append(dest_path)
        # Get 1 image/sec
        time.sleep(1) 
        progress = (i + 1) / totalSec * 50 
        # Update progress bar
        p_var.set(progress)
        progressBar.update()

    mergeImgs(list_file, destFolderTxt.get())


def mergeImgs(list_file, outputFolder):
    try:
        imgS = spaceCmb.get()
        if imgS == "no space":
            imgS = 0
        elif imgS == "small":
            imgS = 30
        elif imgS == "moderate":
            imgS = 60
        else:
            imgS = 150

        imgW = widthCmb.get()
        if imgW == "original":
            imgW = -1 
        else:
            imgW = int(imgW)
    
        images = []
        for file in list_file:
            images.append(Image.open(file))

        newWidth, newHeight = [], []
       
        if imgW > -1:
            # Change width and height
            for x in images:
                newWidth.append(int(imgW)) # Width is equal to the user input
                newHeight.append(int(imgW * x.size[1] / x.size[0])) # Change the height in accordance with the ratio

        else:
            # Keep the original size and ratio
            for x in images:
                newWidth.append(int(x.size[0]))
                newHeight.append(int(x.size[1]))

        # Combine the contents of the two lists
        newSizes = list(zip(newWidth, newHeight))

        # Number of images * Height of one image
        total_height = len(newSizes) * newSizes[0][1]
       
        if imgS > 0: 
            # Add the total height of space
            total_height += (imgS * (len(images) - 1))
    
        # Prepare the background sketchbook
        result_img = Image.new("RGB", (newSizes[0][0], total_height), (255, 255, 255)) 
        
        y_offset = 0 

        for idx, img in enumerate(images):
            # Resize the images 
            if imgW > -1:
                img = img.resize(newSizes[idx])

            result_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + imgS) 

            progress = 50
            progress += (idx + 1) / len(images) * 50 
            p_var.set(progress)
            progressBar.update()

        # Save the merged file
        # Rename the file if duplicate exists
        file_name = "merged_photo"+".png"
        dest_path = os.path.join(outputFolder, file_name)
            
        uniq = 1
        while Path(dest_path).exists():

            file_name = 'merged_photo(%d)' % (uniq)+".png"
            dest_path = os.path.join(outputFolder, file_name)
            uniq+=1
                
        result_img.save(dest_path)
        msgbox.showinfo("Complete", "Images have been merged.")

        # Delete the temporary directory that contians captured images
        shutil.rmtree(CAPTURE_DIR, ignore_errors=True)
      
        clearEntry()

    except Exception as err: 
        showError("Unexpected error has occured. Please retry.")


def clearEntry():
    # Clears user input
    entry_1.delete(0, END)   
    entry_2.delete(0, END) 
    destFolderTxt.delete(0,END)
    p_var.set(0)
    countDownLabel['text'] = ""
    
def showError(msg):
    tkinter.messagebox.showwarning(title="Error", message=msg)
    clearEntry()

###GUI### 
# Figma GUI design file was converted using Tkinter Designer by Parth Jadhav
window = Tk()

window.geometry("469x500")
window.configure(bg = "#F0F0F0")

canvas = Canvas(
    window,
    bg = "#F0F0F0",
    height = 564,
    width = 469,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

# Capture time minute input
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    115.0,
    73.91291809082031,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0,
)
entry_1.place(
    x=40.0,
    y=54.0,
    width=150.0,
    height=37.825836181640625
)

# Capture time second input
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    354.0,
    73.91291809082031,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0
)
entry_2.place(
    x=279.0,
    y=54.0,
    width=150.0,
    height=37.825836181640625
)

# Output directory input
entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    234.70408630371094,
    144.71438598632812,
    image=entry_image_3
)
destFolderTxt = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0
)
destFolderTxt.place(
    x=40.0,
    y=124.80146789550781,
    width=389.4081726074219,
    height=37.825836181640625
)

# Width size combobox
widthCmb = ttk.Combobox( 
   state="readonly", values=["original", "1024", "800", "640"], width=20, font="Roboto"
)

widthCmb.place(
    x=40,
    y=196.19851684570312,
    width=154,
    height=43)
widthCmb.current(0)

# Space size comboboz
spaceCmb = ttk.Combobox( 
   state="readonly", values=["no space", "small", "moderate", "large"], font="Roboto" 
)

spaceCmb.place(
    x=278,
    y=196.19851684570312,
    width=154,
    height=43
)


# Progress bar
entry_7 = Frame(
    bd=0,
    highlightthickness=0,
    bg="#F0F0F0"
)

entry_7.place(
    x=40.0,
    y=280,
    width=389.4081726074219,
    height=30
)

p_var = DoubleVar()
progressBar = ttk.Progressbar(entry_7, maximum=100, variable=p_var)
progressBar.place( x=40.0,
    y=100,
    width=389.4081726074219,
    height=10)
progressBar.pack(fill="x")

spaceCmb.current(0)

# Output directory button
# Icon image is from "https://www.flaticon.com/authors/good-ware" 
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: setDestDir(),
    relief="flat"
)
button_4.place(
    x=400.0,
    y=137.19851684570312,
    width=15.0,
    height=15.0
)

# Start button
button_2 = Button(
    bg="#57F967",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: validateInput(),
    relief="flat",
    text="START",
    fg="#ffffff",
    font=("Roboto Bold", 20 * -1)
)
button_2.place(
    x=40.0,
    y=340,
    width=150.0,
    height=40.0,
)

# Cancel button
button_3 = Button(
    borderwidth=0,
    highlightthickness=0,
    command=lambda: quit(),
    relief="flat",
    bg="#FC6262",
    fg="#ffffff",
    font=("Roboto Bold", 20 * -1),
    text="CANCEL"
)
button_3.place(
    x=280.0,
    y=340,
    width=150.0,
    height=40.0
)

# Texts
canvas.create_text(
    39,
    13,
    anchor="nw",
    text="CAPTURE DURATION TIME",
    fill="#7E39F0",
    font=("Roboto Light", 14 * -1)
)
canvas.create_text(
    230.0,
    47,
    anchor="nw",
    text=":",
    fill="#7E39F0",
    font=("Roboto Bold", 35 * -1)
)

canvas.create_text(
    38,
    32,
    anchor="nw",
    text="MINUTE",
    fill="#7E39F0",
    font=("Roboto Light", 13 * -1)
)

canvas.create_text(
    275,
    32,
    anchor="nw",
    text="SECONDS",
    fill="#7E39F0",
    font=("Roboto Light", 13 * -1)
)

canvas.create_text(
    40,
    105,
    anchor="nw",
    text="SAVE",
    fill="#808080",
    font=("Roboto Light", 13 * -1)
)

canvas.create_text(
    40,
    177,
    anchor="nw",
    text="WIDTH",
    fill="#808080",
    font=("Roboto Light", 13 * -1)
)

canvas.create_text(
    278,
    177,
    anchor="nw",
    text="SPACE",
    fill="#808080",
    font=("Roboto Light", 13 * -1)
)

countDownLabel = tkinter.Label(canvas)
countDownLabel.place(
    x = 40, y = 400
   )
countDownLabel.config(
    fg="#7E39F0", 
    font=("Roboto Light", 23 * -1)
)

# Icon image is from "https://www.freepik.com" from Flaticon
mainIcon = PhotoImage(file=relative_to_assets("merge.png"))
window.title("Capture & Merge")
window.iconphoto(False, mainIcon)

window.resizable(False, False)
window.mainloop()
