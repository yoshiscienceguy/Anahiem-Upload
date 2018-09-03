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

    print(Schools)
#nonActiveColors = ["#00bff3","#f68e56","#a186be","#82ca9c","#fff799"]

nonActiveColors = ["white","white"]
activeColors = ["#6dcff6","#f9ad81","#8560a8","#3cb878","#fff568"]


CURRENTSCHOOL = "Ponderosa"
getFolders()

class App(Frame):
    def __init__(self,root):
        self.CODENAME = ""
        self.teacherButtons = []
        self.selectedTeacher = ""
        self.teamButtons = []
        self.selectedTeam = ""
        self.PROJECTS = {}
        self.selectedProject = ""
        self.actionButtons = []
    
        self.header = Frame(root,bg= "white")
        self.header.pack(side="top",fill = "both",expand=True)

        self.actionLabel = Label(self.header,bd=0,font = LookATME,bg= "white",
                                 foreground="red", text = "Select your Teacher")
        self.actionLabel.pack(padx = 30, pady = 30)
        
        self.mainFrame = Frame(root,bg="white")
        self.mainFrame.pack(side="top", fill="both", expand=True)
        

        self.TeacherSelection = LabelFrame(self.mainFrame,font = LookATME,bd=0,text="Teachers",bg="white",width = 450, height = 400)
        self.TeacherSelection.pack(side = LEFT,fill = "both",expand=True)

        self.TeamSelection = LabelFrame(self.mainFrame,font = LookATME,bd=0,text="Team Number",bg="white",width = 450, height = 400)
        

        self.ActionSelection = LabelFrame(self.mainFrame,font = LookATME,bd=0,text="Action",bg= "white",width = 450, height = 400)
        
        self.createActionButtons(self.ActionSelection)

        self.DownloadSelection = LabelFrame(self.mainFrame,font = LookATME,bd=0,text="Download",bg="white",width = 450, height = 400)
        self.UploadSelection = LabelFrame(self.mainFrame,font = LookATME,bd=0,text="Upload",bg="white",width = 450, height = 400)
        
        
        self.teacherSelection(["Navarro","Gruber","Morales","Dixon","Fernandez"],self.TeacherSelection)

        self.teamSelection(["1","2","3","4","5","6","7","8","9","10"],self.TeamSelection)

        self.UploadButton = Button(self.UploadSelection,font = Newfont, text = "UPLOAD",width = 20, height = 10,relief=RIDGE,bd=5,state=DISABLED,
                            command = self.chooseFile,highlightcolor="RED",highlightthickness = 2)
        self.UploadButton.pack(padx = 50)
        
        

    def download(self,fileID,fileName):
        drive.downloadTo(fileID,fileName)
        
        
    def upload(self,fileName):
        folderURL = Schools[CURRENTSCHOOL]["Folders"][self.selectedTeacher][int(self.selectedTeam)-1]
        print(folderURL)
        success = drive.upload(fileName,folderURL)
        if(success):
            print("yay")
            
        print(self.selectedTeacher + " "+self.selectedTeam + " " + fileName)
    def chooseFile(self):
        filename = askopenfilename(filetypes = (("Python Files","*.py"),("All Files","*.*")))
        if(filename == ""):
            return
        self.upload(filename)

    def changeAction(self,action):
        self.DownloadSelection.pack_forget()
        self.UploadSelection.pack_forget()

        self.createCodeSelection(self.DownloadSelection)
        
        if(action == "down"):
            self.actionButtons[1]["background"] = activeColors[0]
            self.actionButtons[0]["background"] = "white"
            
            self.DownloadSelection.pack(side = LEFT,padx=(20,0),fill = "both",expand=True)
            self.actionLabel["text"] = "Select a file and click download"
            for projects in self.PROJECTS:
                info = self.PROJECTS[projects]
                info[1]["state"] = "normal"
        if(action == "up"):
            self.actionButtons[0]["background"] = activeColors[0]
            self.actionButtons[1]["background"] = "white"
            self.UploadSelection.pack(side = LEFT,padx=(20,0),fill = "both",expand=True)
            self.actionLabel["text"] = "Click on Upload and select a file"
            self.UploadButton["state"] = "normal"
            
    def createActionButtons(self,parentFrame):
        
        upButton = Button(parentFrame,font = Newfont,text = "upload",height=  3, width = 10,bg="white",relief=RIDGE,bd=5,
                            highlightcolor="RED",highlightthickness = 2,
                          command = lambda :self.changeAction("up"),state=DISABLED)
        downButton = Button(parentFrame,font = Newfont,text = "downlo",height=  3, width = 10,bg="white",relief=RIDGE,bd=5,
                            highlightcolor="RED",highlightthickness = 2,
                            command = lambda :self.changeAction("down"),state=DISABLED)
        self.actionButtons.append(upButton)
        self.actionButtons.append(downButton)
        upButton.pack(pady = 25,padx=(20,0))
        downButton.pack(pady = 25,padx=(20,0))
        
    def selectProject(self,projName):
        for projects in self.PROJECTS:
            info = self.PROJECTS[projects]
            info[0]["background"] = "white"
            info[2]["state"] = DISABLED
            info[2]["background"] = "white"
        self.PROJECTS[projName][0]["background"] = "red"
        self.PROJECTS[projName][2]["state"] = "normal"
        self.PROJECTS[projName][2]["background"] = "green"
        self.UploadButton["state"] = DISABLED
        
    def createCodeSelection(self,parentFrame):
        count = 0
        folderID = Schools[CURRENTSCHOOL]["Folders"][self.selectedTeacher][int(self.selectedTeam)-1]
        projects = drive.download(folderID)
        for project in self.PROJECTS:
            self.PROJECTS[project][0].destroy()
            self.PROJECTS[project][1].destroy()
            self.PROJECTS[project][2].destroy()
        self.PROJECTS={}
        if(projects):
            for code in projects:
                projFrame = Frame(parentFrame,background = "white")
                projButton = Button(projFrame,font = Newfont,text = code,width = 10, height= 1, background="white",relief=GROOVE,
                                    command = lambda codeName = code : self.selectProject(codeName))
                projButton.pack(side = LEFT,padx = 20)
                downButton = Button(projFrame,font = Newfont, text = "Down",width = 10, height= 1,state="disabled",
                                    background="white",relief=FLAT, command = lambda fileID = projects[code],fileName = code:self.download(fileID,fileName))
                downButton.pack(side = LEFT,padx = (20,20),pady =20)
                projFrame.pack(fill = "both",expand=True)
                self.PROJECTS[code] = (projFrame,projButton,downButton)
                count +=1
        else:
            self.actionLabel["text"] = "No Files Found"

    def teamSelection(self,teamNames,newFrame):
        twosFrame = Frame(newFrame,width = 400,background="white")
        count=-1
        for name in teamNames:
            fix = count+ 1
            button = Button(twosFrame,font = Newfont,text=name,width = 5,height=1,relief=RIDGE,bd=5,
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
        self.actionLabel["text"] = "Select Upload or Download"
        self.ActionSelection.pack(side=LEFT,padx=(0,20),fill = "both",expand=True)
        print(teamName)
        for action in self.actionButtons:
            action["state"] = "normal"
        self.UploadButton["state"] = DISABLED
        self.actionButtons[1]["background"] = "white"
        self.actionButtons[0]["background"] = "white"
        for projects in self.PROJECTS:
            info = self.PROJECTS[projects]
            info[0]["background"] = "white"
            info[1]["state"] = DISABLED
            info[2]["state"] = DISABLED
            info[2]["background"] = "white"    
    def teacherSelection(self,teacherNames,newFrame):
        twosFrame = Frame(newFrame,width = 600,background="white")
        count=-1
        for name in teacherNames:
            button = Button(twosFrame,font = Newfont,text=name,width = 10,height=3,relief=RIDGE,bd=5,
                            highlightcolor="RED",highlightthickness = 2,background=nonActiveColors[count%len(nonActiveColors)],
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
            self.teacherButtons[i]["background"] = nonActiveColors[i%len(nonActiveColors)]
        self.teacherButtons[buttonNum]["background"]= activeColors[buttonNum]
        print(teacher)

        for team in self.teamButtons:
            team["state"] = "normal"
        self.actionLabel["text"] = "Select your team"
        self.TeamSelection.pack(side = LEFT,fill = "both",expand=True)

        for i in range(len(self.teamButtons)):
            self.teamButtons[i]["background"] = nonActiveColors[i%len(nonActiveColors)]
        self.actionButtons[1]["background"] = "white"
        self.actionButtons[0]["background"] = "white"
        self.actionButtons[0]["state"] = DISABLED
        self.actionButtons[1]["state"] = DISABLED
        self.UploadButton["state"] = DISABLED
        for projects in self.PROJECTS:
            info = self.PROJECTS[projects]
            info[0]["background"] = "white"
            info[1]["state"] = DISABLED
            info[2]["state"] = DISABLED
            info[2]["background"] = "white"        

drive.login()
root = Tk()
root.title("AESD Upload Program")
root.configure(background='white')
root.resizable(0,0)
Newfont = tkFont.Font(root,family="Helvetica",size=20,weight="bold")
LookATME = tkFont.Font(root,family="Helvetica",size=25,weight="bold")
images = [PhotoImage(file="./Box1.gif"),
          PhotoImage(file="./Box2.gif"),
          PhotoImage(file="./Box3.gif"),
          PhotoImage(file="./Box4.gif"),
          PhotoImage(file="./Box5.gif")]
A = App(root)
root.mainloop()
