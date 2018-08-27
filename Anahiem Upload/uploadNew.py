from Tkinter import *
import tkFont
from tkFileDialog import askopenfilename
import googleDriveConnect as drive
FOLDERID = "1Q1ViyA6VNwyHzAkKjIbKlxMWrCpFAgeE"
Schools = {
        "Ponderosa":{"Teachers": ["Navarro","Dixon","Vazquez","Morales","Pichardo"],
                     "Folders": {}
                     },
        "Stoddard":4,
        "Jefferson":3,
        "Ross":4
    }

def getFolders():
    f = open(CURRENTSCHOOL+"_folderDirectories.txt","r")
    info = f.readlines()
    info = [l.strip('\n\r') for l in info]
    f.close()
    for i in range(len(info)/10):
        Schools[CURRENTSCHOOL]["Folders"][info[i*11]]= info[i*10 + (i+1):11*(i+1)]
nonActiveColors = ["#00bff3","#f68e56","#a186be","#82ca9c","#fff799"]
activeColors = ["#6dcff6","#f9ad81","#8560a8","#3cb878","#fff568"]

CURRENTSCHOOL = "Ponderosa"
getFolders()

class App(Frame):
    def __init__(self,root):
        self.teacherButtons = []
        self.selectedTeacher = ""
        self.teamButtons = []
        self.selectedTeam = ""
        self.selectedProject = ""
        self.actionButtons = []

        self.header = Frame(root)
        self.header.pack(side="top",fill = "both",expand=True)

        self.actionLabel = Label(self.header,bg= "white", text = "Do dis")
        self.actionLabel.pack(padx = 30, pady = 30)
        
        self.mainFrame = Frame(root,bg="white")
        self.mainFrame.pack(side="top", fill="both", expand=True)
        

        self.TeacherSelection = Frame(self.mainFrame,bg="white",width = 450, height = 400)
        self.TeacherSelection.pack(side = LEFT)

        self.TeamSelection = Frame(self.mainFrame,bg="white",width = 450, height = 400)
        self.TeamSelection.pack(side = LEFT)

        self.ActionSelection = Frame(self.mainFrame,bg= "white",width = 450, height = 400)
        self.ActionSelection.pack(side=LEFT)
        self.createActionButtons(self.ActionSelection)

        self.DownloadSelection = Frame(self.mainFrame,bg="white",width = 450, height = 400)
        self.UploadSelection = Frame(self.mainFrame,bg="white",width = 450, height = 400)
        
        
        self.teacherSelection(["A","B","C","D","E"],self.TeacherSelection)

        self.teamSelection(["1","2","3","4","5","6","7","8","9","10"],self.TeamSelection)
        
        self.createUploadButton(self.UploadSelection)
        self.createCodeSelection(["hi.py","hello.py","bye.py","goodbye.py","nope.avi"],self.DownloadSelection)

    def createActionButtons(self,parentFrame):
        upButton = Button(parentFrame,text = "upload",height=  7, width = 25, command = lambda :self.changeAction("up"),state=DISABLED)
        downButton = Button(parentFrame,text = "downlo",height=  7, width = 25,command = lambda :self.changeAction("down"),state=DISABLED)
        self.actionButtons.append(upButton)
        self.actionButtons.append(downButton)
        upButton.pack(pady = 25)
        downButton.pack(pady = 25)
        
        
    def createCodeSelection(self,projects,parentFrame):
        count = 0
        for code in projects:
            projFrame = Frame(parentFrame,width = 600,background = "white")
            projButton = Label(projFrame,text = code,width = 25, height= 4)
            projButton.pack(side = LEFT,padx = 20)
            downButton = Button(projFrame, text = "Down",width = 15, height= 4)
            downButton.pack(side = LEFT,padx = (20,20),pady =20)
            projFrame.pack()
            count +=1
    def createUploadButton(self,parentFrame):
        UploadButton = Button(parentFrame, text = "UPLOAD",width = 30, height = 15)
        UploadButton.pack(padx = 50)
    def changeAction(self,action):
        self.DownloadSelection.pack_forget()
        self.UploadSelection.pack_forget()
        if(action == "down"):
            self.DownloadSelection.pack(side = LEFT)
        if(action == "up"):
            self.UploadSelection.pack(side = LEFT)
    def upProject(self,projName):
        
        pass
    def teamSelection(self,teamNames,newFrame):
        twosFrame = Frame(newFrame,width = 400,background="white")
        count=-1
        for name in teamNames:
            fix = count+ 1
            button = Button(twosFrame,text=name,width = 20,height=5,relief=RIDGE,bd=5,
                            highlightcolor="RED",highlightthickness = 2,background=nonActiveColors[fix%len(nonActiveColors)],
                            command = lambda team=name, index=count: self.setTeam(team,index+1),state=DISABLED )
            button.pack(side=LEFT,padx=10,pady=10)
            self.teamButtons.append(button)
            if(count%2 == 0):
                twosFrame.pack()
                twosFrame = Frame(newFrame,width = 400,background="white")
            count += 1
        twosFrame.pack()
        
    def setTeam(self,teamName,buttonNum):
        print(buttonNum)
        self.selectedTeam = teamName
        for i in range(len(self.teamButtons)):
            self.teamButtons[i]["background"] = nonActiveColors[i%len(nonActiveColors)]
        self.teamButtons[buttonNum]["background"]= activeColors[buttonNum%len(nonActiveColors)]
        ####
        print(teamName)
        for action in self.actionButtons:
            action["state"] = "normal"
    def teacherSelection(self,teacherNames,newFrame):
        twosFrame = Frame(newFrame,width = 600,background="white")
        count=-1
        for name in teacherNames:
            button = Button(twosFrame,text=name,width = 20,height=10,relief=RIDGE,bd=5,
                            highlightcolor="RED",highlightthickness = 2,background=nonActiveColors[count+1],
                            command = lambda teacher=name, index=count: self.setTeacher(teacher,index+1) )
            button.pack(side=LEFT,padx=10,pady=10)
            self.teacherButtons.append(button)
            if(count%2 == 0):
                twosFrame.pack()
                twosFrame = Frame(newFrame,width = 600,background="white")
            count += 1
        twosFrame.pack()
    def setTeacher(self,teacher,buttonNum):
        self.selectedTeacher = teacher
        for i in range(len(self.teacherButtons)):
            self.teacherButtons[i]["background"] = nonActiveColors[i]
        self.teacherButtons[buttonNum]["background"]= activeColors[buttonNum]
        print(teacher)

        for team in self.teamButtons:
            team["state"] = "normal"
        
##        self.mainFrame.grid_rowconfigure(0,weight=1)
##        self.mainFrame.grid_rowconfigure(1,weight=4)
##        self.mainFrame.grid_columnconfigure(0,weight=1)
##
##        self.backButton = Frame(self.mainFrame,width = 900,bg="white")
##        self.backButton.grid_columnconfigure(0,weight=1)
##        self.backButton.grid_columnconfigure(1,weight=1)
##        
##        self.teamButtons = Frame(self.mainFrame,width = 900,bg="white")
##        self.teamButtons.grid_columnconfigure(0,weight=1)
##        self.teamButtons.grid_columnconfigure(1,weight=1)
##        
##        self.upDownButtons = Frame(self.mainFrame,width = 900,bg="white")
##        self.upDownButtons.grid_rowconfigure(0,weight=1)
##        self.upDownButtons.grid_columnconfigure(0,weight=1)
##        self.upDownButtons.grid_columnconfigure(1,weight=1)
##        self.classesButton = Frame(self.mainFrame,width = 900,bg="white")
##        
##        self.downloadList = Frame(self.mainFrame,width = 900,bg="white")
##        self.downloadList.grid_rowconfigure(0,weight=1)
##        self.downloadList.grid_columnconfigure(0,weight=1)
##        
##        self._createBackButton()
##        self._createClassChoice()
##        self._createDownUp()
##        self._createTeamChoice()
##        self._createlistBox()
##        self.classesButton.tkraise()
##    def getFiles(self):
##        FileID = Schools[CURRENTSCHOOL]["Folders"][self.teacher][self.teamNum-1]
##        self.results = drive.download(FileID)
##        
##        self.updateBox(self.results.keys())
##        self.downloadList.tkraise()
##        self.frameNumber = 3
##        
##    def chooseFile(self):
##        filename = askopenfilename(filetypes = (("Python Files","*.py"),("All Files","*.*")))
##        if(filename == ""):
##            return
##        FileID = Schools[CURRENTSCHOOL]["Folders"][self.teacher][self.teamNum-1]
##        result = drive.upload(filename,FileID)
##        if(result):
##            top = Toplevel(bg = "white")
##            top.wm_geometry("300x200")
##            top.title("Sucess")
##            msg = Message(top, text="Sucessfully uploaded",width=250,bg="white")
##            msg['font'] = helv36
##            msg.pack(pady=15)
##
##            button = Button(top, text="Dismiss", command=top.destroy)
##            button['font'] = helv36
##            button.pack(pady=25)
##        
##    def chooseTeam(self,num):
##        self.teamNum = num
##        self.currentTeamNumber.set("Current Team: "+ str(self.teamNum))
##        self.upDownButtons.tkraise()
##        self.frameNumber = 3
##    def goBack(self):
##        
##        if(self.frameNumber == 2):
##            self.teamButtons.tkraise()
##        if(self.frameNumber == 3):
##            self.classesButton.tkraise()
##        self.teacher = ""
##        self.teamNum = ""
##        self.currentTeamNumber.set("Current Team: "+ str(self.teamNum))
##        self.currentTeacherName.set("Current Teacher: "+ self.teacher)
##        
##    def setTeacher(self,teacherName):
##        self.teacher = teacherName
##        self.currentTeacherName.set("Current Teacher: "+ self.teacher)
##        self.teamButtons.tkraise()
##        self.frameNumber = 3
##    def updateBox(self,keys):
##        self.files= keys
##        self.downloadFiles.delete(0, END)
##        for item in keys:
##            self.downloadFiles.insert(END, item)
##    def selectDownload(self):
##        selection = map(int, self.downloadFiles.curselection())[0]
##        fileName = self.files[selection]
##        fileID = self.results[fileName]
##        drive.downloadTo(fileID)
##        
##    def _createlistBox(self):
##        self.downloadFiles = Listbox(self.downloadList,width = 50)
##        
##
##        
##        self.downloadFiles.grid(row=0,column=0,padx= 25,pady = (25,0))
##        
##        self.forwardPhoto = PhotoImage(file="./Forward.gif")
##        bButton = Button(self.downloadList,image=self.forwardPhoto,bg="white",relief=FLAT,
##                         command=self.selectDownload)
##        bButton.grid(row=1,column=0,padx= 25,pady = (25,0))
##        
##        
##        self.downloadList.grid(row=1,pady=(30,5),padx=25, sticky="nsew")
##    def _createClassChoice(self):
##        amountClasses = len(Schools[CURRENTSCHOOL]["Teachers"])
##        
##        for classNum in range(amountClasses):
##            teacher = Schools[CURRENTSCHOOL]["Teachers"][classNum]
##            button = Button(self.classesButton,text=teacher,bg="white",height=100,
##                            command= lambda teacher=teacher: self.setTeacher(teacher),
##                            image=images[classNum],compound="center" ,fg="white",relief=FLAT
##                            )
##            button['font'] = helv36
##            button.grid(row=0,column=classNum,padx=10, pady=5)
##            button.grid_columnconfigure(classNum,weight=1)
##        self.classesButton.grid(row=1,pady=(30,5),padx=25, sticky="nsew")
##    def _createTeamChoice(self):
##        for teamNum in range(1,11):
##            button = Button(self.teamButtons,text=str(teamNum),bg="white",height=2,width=5,
##                            command= lambda teamNum=teamNum: self.chooseTeam(teamNum),
##                            compound="center" ,fg="black"
##                            )
##            button['font'] = helv36
##            button.grid(row=0,column=teamNum,padx=10, pady=5)
##        self.teamButtons.grid(row=1,pady=(30,5),padx=25, sticky="nsew")
##        
##    def _createDownUp(self):
##        self.Uphoto = PhotoImage(file="./upload.gif")
##        self.Dphoto = PhotoImage(file="./download.gif")
##
##        uploadButton = Button(self.upDownButtons,image=self.Uphoto,bg="white",command=self.chooseFile)
##        downloadButton = Button(self.upDownButtons,image=self.Dphoto,bg="white",command=self.getFiles)
##        uploadButton.grid(row=0,column=0,padx=10, pady=5,sticky="e")
##        downloadButton.grid(row=0,column=1,padx=10, pady=5,sticky="w")
##        self.upDownButtons.grid(row=1,pady=25,padx=25, sticky="nsew")
##        
##    def _createTeacherDisplay(self):
##        self.currentTeacherName = StringVar()
##        w = Label(self.backButton,textvariable=self.currentTeacherName,bg="white")
##        w['font'] = helv36
##        self.currentTeacherName.set("Current Teacher: "+ self.teacher)
##        w.grid(row=0,column=1,padx= 25,pady = (25,0),sticky="w")
##    def _createTeamNumber(self):
##        self.currentTeamNumber = StringVar()
##        w = Label(self.backButton,textvariable=self.currentTeamNumber,bg="white")
##        w['font'] = helv36
##        self.currentTeamNumber.set("Current Team: "+ str(self.teamNum))
##        w.grid(row=1,column=1,padx= 25,pady = (25,0),sticky="w")
##        
##    def _createBackButton(self):
##        self._createTeacherDisplay()
##        self._createTeamNumber()
##        
##        self.backPhoto = PhotoImage(file="./Back.gif")
##        bButton = Button(self.backButton,image=self.backPhoto,bg="white",relief=FLAT,
##                         command=self.goBack)
##        bButton.grid(row=0,column=0,padx= 25,pady = (25,0))
##        self.backButton.grid(row=0,column=0,sticky="ew")

    
        
        
root = Tk()
root.title("AESD Upload Program")
root.configure(background='white')
root.resizable(0,0)
images = [PhotoImage(file="./Box1.gif"),
          PhotoImage(file="./Box2.gif"),
          PhotoImage(file="./Box3.gif"),
          PhotoImage(file="./Box4.gif"),
          PhotoImage(file="./Box5.gif")]
helv36 = tkFont.Font(family='Helvetica', size=15, weight='bold')
A = App(root)
root.mainloop()
