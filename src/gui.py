import tkinter as tk
from PIL import Image, ImageTk
import random
import linearsearch

WIDTH = 1366
HEIGHT = 768
BACKGROUND = "#808080"
FONTCOLOR = "#ffffff"


def hello():
    pass


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()  # Initiating Super Method
        self.state("zoomed")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.title("DS_ALGO_VISUALIZER")
        # icon = tk.PhotoImage(file="../assets/brain.png")
        # self.iconphoto(True, icon)
        self.config(background=BACKGROUND)

        self.updateScreenGeometry()

        self.pages = {}
        self.raised = []
        # for P in (WelcomePage, AboutPage, PickAndPlacePage, WritingPage, SettingsPage, CalibrationPage, ManualControlPage):
        for P in (WelcomePage, SearchingPage):
            page = P(self)
            self.pages[P] = page

        self.showPage(WelcomePage)

    def showPage(self, page):
        self.raised = []
        self.raised.append(page)
        frame = self.pages[page]
        frame.tkraise()

    def updateScreenGeometry(self):
        global WIDTH, HEIGHT
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()


class TextLabel(tk.Label):
    def __init__(self, page, text, fontsize=20):
        super().__init__(
            page,
            fg=FONTCOLOR,
            text=text,
            font=('Arial', fontsize),
            bg=BACKGROUND
        )


class ImageLabel(tk.Label):
    def __init__(self, page, location, size, bg=BACKGROUND):
        imageRaw = Image.open(location)
        imageRaw = imageRaw.resize(size)
        self.image = ImageTk.PhotoImage(imageRaw)  # Avoid garbage collection
        super().__init__(page, bg=BACKGROUND, image=self.image)


class ButtonLabel(tk.Button):
    def __init__(self, page, text, fontsize=15, command=hello, width=20, borderwidth=3, state=tk.NORMAL):
        super().__init__(page,
                         text=text,
                         font=('Arial', fontsize),
                         relief=tk.RAISED,
                         bg=BACKGROUND,
                         fg=FONTCOLOR,
                         width=width,
                         borderwidth=borderwidth,
                         command=command,
                         activebackground=FONTCOLOR,
                         activeforeground=BACKGROUND,
                         state=state
                         )


class Page(tk.Frame):
    def __init__(self, container):
        super().__init__(container, bg=BACKGROUND)
        self.container = container
        self.grid(row=0, column=0, sticky="nsew")


class WelcomePage(Page):
    def __init__(self, container):
        super().__init__(container)

        text = TextLabel(self, text="DS_ALGO_VISUALIZER", fontsize=40)
        text.pack(fill="x")

        # headingImage = ImageLabel(
        #     self,
        #     location="../assets/brain.png",
        #     size=(400, 400)
        # )
        # headingImage.pack(fill='x', pady=10)

        self.searchingButton = ButtonLabel(
            self,
            text="Searching Algorithms",
            command=lambda: self.container.showPage(SearchingPage)
        )
        self.searchingButton.pack()

        self.sortingButton = ButtonLabel(
            self,
            text="Sorting Algorithms",
            # command=lambda: self.container.showPage(ManualControlPage)
        )
        self.sortingButton.pack()

        self.stackQueueButton = ButtonLabel(
            self,
            text="Stack and Queue",
            # command=lambda: self.container.showPage(WritingPage)

        )
        self.stackQueueButton.pack()

        self.settingsButton = ButtonLabel(
            self,
            text="Settings",
            # command=lambda: self.container.showPage(SettingsPage)
        )
        self.settingsButton.pack()

        self.aboutButton = ButtonLabel(
            self,
            text="About",
            # command=lambda: self.container.showPage(AboutPage)
        )
        self.aboutButton.pack()
        self.exitButton = ButtonLabel(
            self,
            text="Exit",
            command=self.container.destroy
        )
        self.exitButton.pack()

        self.disableButtons()

    def disableButtons(self):
        # self.pickAndPlaceButton["state"] = tk.DISABLED
        # self.writingButton["state"] = tk.DISABLED
        # self.manualButton["state"] = tk.DISABLED
        pass

    def enableButtons(self):
        # self.pickAndPlaceButton["state"] = tk.NORMAL
        # self.writingButton["state"] = tk.NORMAL
        # self.manualButton["state"] = tk.NORMAL
        pass


class SearchingPage(Page):
    def __init__(self, container):
        super().__init__(container)
        text = TextLabel(self, "Searching Algorithms", fontsize=40)
        text.pack(fill="x")

        self.board = DrawingBoard(self)
        self.board.pack()

        self.backButton = ButtonLabel(
            self,
            text="Back",
            command=lambda: self.container.showPage(WelcomePage)
        )
        self.backButton.pack(
            pady=5, padx=10, side="right", anchor="se")

        self.createArrayButton = ButtonLabel(
            self,
            text="Update Array",
            command=self.createArray
        )
        self.createArrayButton.pack(
            pady=5, padx=10, side="right", anchor="se")

        self.linearSearchButton = ButtonLabel(
            self,
            text="Linear Search",
            command=self.showLinearSearch
        )
        self.linearSearchButton.pack(
            pady=5, padx=10, side="right", anchor="se")

        self.binarySearchButton = ButtonLabel(
            self,
            text="Binary Search",
            # command=self.showLinearSearch
        )
        self.binarySearchButton.pack(
            pady=5, padx=10, side="right", anchor="se")

        self.input = tk.Entry(self, width=20,
                              font=("Arial", 20))
        self.input.insert(0, string="0")
        self.input.pack(pady=10, padx=10, side="right", anchor="se")
        self.createArray()

    def createArray(self):
        self.arr = []
        self.vals = []
        for i in range(0, 26, 1):
            self.vals.append(random.randint(0, 100))
        self.vals.sort()

        # print(self.vals)
        for i in range(0, 26, 1):
            self.arr.append(ArrayElement(i, self.vals[i]))
        self.board.delete("all")
        self.board.showArrayElements(self.arr)

    def showLinearSearch(self):
        searchItem = 0
        if(self.input.get() != ''):
            searchItem = int(self.input.get())
        x = linearsearch.linearSearchV(self, self.arr, searchItem)
        if(x != False):
            self.board.showResult(f"{searchItem} Was Found at index {x}")
        else:
            self.board.showResult(f"{searchItem} Was Not Found")
        self.board.showArrayElements(self.arr)

    def updateBoard(self, arr):
        self.board.delete("all")
        for elem in arr:
            self.board.showArrayElements(arr)
        self.container.update()


class DrawingBoard(tk.Canvas):
    def __init__(self, container):
        self.height = HEIGHT*.8
        self.width = WIDTH*.95
        super().__init__(container, bg="white", height=self.height, width=self.width)

    def showArrayElements(self, elements):
        for el in elements:
            self.create_rectangle(el.x0, el.y0, el.x1,
                                  el.y1, width=el.width, outline=el.outline)
            self.create_text(el.x0+20, el.y0+20, text=el.value,
                             fill="black", font=('Helvetica 15 bold'))

    def showResult(self, text):
        xpos = len(text)/2 * 20
        self.create_text(xpos, 100, text=text,
                         fill="black", font=('Helvetica 25 bold'))


class ArrayElement:
    def __init__(self, index, value, selected=True, success=True):
        self.selected = selected
        self.success = success
        self.x0 = 5 + index * 50
        self.x1 = self.x0 + 40
        self.y0 = HEIGHT * 0.35
        self.y1 = self.y0 + 40
        self.value = value
        self.success = False
        self.toggleSelection()
        self.toggleSuccess()

    def toggleSelection(self):
        self.selected = not self.selected
        if self.selected:
            self.width = 4
        if not self.selected:
            self.width = 1

    def toggleSuccess(self):
        self.success = not self.success
        if self.success:
            self.outline = "black"
        if not self.success:
            self.outline = "green"


window = GUI()
window.mainloop()
