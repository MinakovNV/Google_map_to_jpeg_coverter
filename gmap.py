import tkinter
import SDP4_python_mini_project.Gmap_downloader
from PIL import ImageTk, Image


class MyFrame(tkinter.Frame):

    def __init__(self, master, im):
        tkinter.Frame.__init__(self, master)
        self.caption = tkinter.Label(self, text="Venik.Team Presents:")
        self.caption.grid()
        self.image = ImageTk.PhotoImage(im)
        self.image_label = tkinter.Label(self, image=self.image, bd=0)
        self.image_label.grid()
        self.grid()

def main():

    SDP4_python_mini_project.Gmap_downloader.main_l()
    im = Image.open("mymap.jpg") # read map from disk

    mainw = tkinter.Tk()
    mainw.frame = MyFrame(mainw, im)
    mainw.mainloop()

main()