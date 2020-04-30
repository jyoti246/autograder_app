from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "" and not db.validate(self.email.text, self.password):
                db.add_user(self.email.text, self.password.text, self.namee.text)

                # self.reset()
                MainWindow.current = self.email.text
                self.reset()
                sm.current = "main"
                # sm.current = "main"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class Profile(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def back(self):
        sm.current = "main"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    current = ""

    def logOut(self):
        sm.current = "login"

    def profl(self):
        Profile.current = self.current
        sm.current = "profile"

    def enrolled_st(self):
        STCourses.current = self.current;
        sm.current = "stcourses"
    def enrolled_ta(self):
        TACourses.current = self.current;
        sm.current = "tacourses"
    def ta_join_req(self):
        TARequests.current = self.current;
        sm.current = "tarequests"
        
    def st_join_req(self):
        STRequests.current = self.current;
        sm.current = "strequests"
    def my_courses(self):
        MyCourses.current = self.current;
        sm.current = "mycourses"
    
    def on_enter(self, *args):
        pass


class TARequests(Screen):
    current = ""
    lbl1 = ObjectProperty(None)
    lbl2 = ObjectProperty(None)
    flag =0
    # bt1 = ObjectProperty(None)
    # bt2 = ObjectProperty(None)
    def back(self):
        ind=0
        if(self.flag ==0):
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
        else:
            self.ids.ides.remove_widget(self.labl)
        self.wrtfile.close()
        with open("tarequest.txt", "r") as f:
            lines = f.readlines()
        with open("tarequest.txt", "w") as f:
            f.write("")
            for line in lines:
                course, fromusr, tousr = line.strip().split(";")
                if ind>= self.ind or tousr != self.current:
                    # print(line)
                    f.write(line)
                else:
                    # print("Bhaiyaji hum nikal lia ")
                    ind = ind+1
        

        sm.current = "main"



    def accept(self,instance):
        self.wrtfile.write(self.users[self.ind][0]+";"+self.users[self.ind][1]+";"+self.current+"\n")
        self.ind=self.ind+1
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Guide: "+ self.users[self.ind][1]


    def deny(self,instance):
        self.ind=self.ind+1
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Guide: "+ self.users[self.ind][1]


    def on_enter(self, *args):
        self.file = open("tarequest.txt", "r")
        self.users = []

        for line in self.file:
            if line !="":
                course, fromusr, tousr = line.strip().split(";")
                if(tousr == self.current):
                    self.users.append((course, fromusr))
            
        self.wrtfile = open("courseta.txt", "a")
        self.file.close()
        self.ind = 0
        self.labl1 = Label(id= self.lbl1, text = "Course: ", size_hint = (0.5, 0.08),pos_hint = {"x":0.0, "top":.7-.1},font_size= 15)
        self.labl2 = Label(id= self.lbl2, text = "Guide: ", size_hint = (0.5, 0.08),pos_hint = {"x":0.0, "top":.62-.1},font_size= 15)
        self.btn1 = Button(text= "Accept", size_hint = (0.2, 0.08),pos_hint = {"x":0.7, "top":.7-.1},font_size= 15)
        self.btn2 = Button(text = "Deny" ,size_hint = (0.2, 0.08),pos_hint = {"x":0.7, "top":.62-.1},font_size= 15)
        self.btn1.bind(on_release = self.accept)
        self.btn2.bind(on_release = self.deny)
        self.ids.ides.add_widget(self.labl1)
        self.ids.ides.add_widget(self.labl2)
        self.ids.ides.add_widget(self.btn1)
        self.ids.ides.add_widget(self.btn2)
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Guide: "+ self.users[self.ind][1]
           

class STRequests(Screen):
    current = ""
    lbl1 = ObjectProperty(None)
    lbl2 = ObjectProperty(None)
    flag =0
    # bt1 = ObjectProperty(None)
    # bt2 = ObjectProperty(None)
    def back(self):
        ind=0
        if(self.flag ==0):
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
        else:
            self.ids.ides.remove_widget(self.labl)
        self.wrtfile.close()
        with open("strequest.txt", "r") as f:
            lines = f.readlines()
        with open("strequest.txt", "w") as f:
            f.write("")
            for line in lines:
                course, fromusr, tousr = line.strip().split(";")
                if ind>= self.ind or tousr != self.current:
                    # print(line)
                    f.write(line)
                else:
                    # print("Bhaiyaji hum nikal lia ")
                    ind = ind+1
        

        sm.current = "main"



    def accept(self,instance):
        self.wrtfile.write(self.users[self.ind][0]+";"+self.current+";"+self.users[self.ind][1]+"\n")
        self.ind=self.ind+1
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Student: "+ self.users[self.ind][1]


    def deny(self,instance):
        self.ind=self.ind+1
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Student: "+ self.users[self.ind][1]


    def on_enter(self, *args):
        self.file = open("strequest.txt", "r")
        self.users = []

        for line in self.file:
            if line !="":
                print("\n\n\nhere")
                print(line)
                print("here\n\n\n")
                course, fromusr, tousr = line.strip().split(";")
                if(tousr == self.current):
                    self.users.append((course, fromusr))
            
        self.wrtfile = open("coursest.txt", "a")
        self.file.close()
        self.ind = 0
        self.labl1 = Label(id= self.lbl1, text = "Course: ", size_hint = (0.5, 0.08),pos_hint = {"x":0.0, "top":.7-.1},font_size= 15)
        self.labl2 = Label(id= self.lbl2, text = "Student: ", size_hint = (0.5, 0.08),pos_hint = {"x":0.0, "top":.62-.1},font_size= 15)
        self.btn1 = Button(text= "Accept", size_hint = (0.2, 0.08),pos_hint = {"x":0.7, "top":.7-.1},font_size= 15)
        self.btn2 = Button(text = "Deny" ,size_hint = (0.2, 0.08),pos_hint = {"x":0.7, "top":.62-.1},font_size= 15)
        self.btn1.bind(on_release = self.accept)
        self.btn2.bind(on_release = self.deny)
        self.ids.ides.add_widget(self.labl1)
        self.ids.ides.add_widget(self.labl2)
        self.ids.ides.add_widget(self.btn1)
        self.ids.ides.add_widget(self.btn2)
        if(self.ind == len(self.users)):
            
            self.ids.ides.remove_widget(self.btn1)
            self.ids.ides.remove_widget(self.btn2)
            self.ids.ides.remove_widget(self.labl1)
            self.ids.ides.remove_widget(self.labl2)
            self.labl = Label(text="No Requests to Show", size_hint = (0.6, 0.08),pos_hint = {"x":0.2, "top":.7},font_size= 20 )
            self.ids.ides.add_widget(self.labl)
            self.flag=1
        else:
            self.labl1.text = "Course: "+ self.users[self.ind][0]
            self.labl2.text = "Student: "+ self.users[self.ind][1]
           

class MyCourses(Screen):
    current = ""
    course = ObjectProperty(None)
    count=0
    def back(self):
        self.course.text = ""
        self.wrtfile.close()
        for button in self.buttons:
            self.ids.ides.remove_widget(button)
        sm.current = "main"
    def add_button(self):
        if self.course.text != "":
            self.reset()

    def reset(self):
        temp = self.count
        self.buttons.append(Button(text= self.course.text, size_hint = (1, 0.05),pos_hint = {"x":0, "top":0.8-.05*self.count},font_size= 15,on_release = lambda x: self.enter_course(x = temp)))
        # self.buttons[self.count].bind(on_release = self.enter_course)
        self.ids.ides.add_widget(self.buttons[self.count])
        self.courses.append(self.course.text)
        self.count= self.count+1
        self.tot = self.tot+1
        self.wrtfile.write(str(self.tot)+";"+self.course.text+";"+self.current+"\n")
        self.course.text = ""
    def enter_course(self, x):
        CourseProf.currentProf = self.current;
        CourseProf.currentCourse = self.courses[x]
        sm.current = "courseprof"
        
    def on_enter(self, *args):
        self.file = open("courses.txt", "r")
        self.courses = []
        self.count = 0
        self.tot=0
        for line in self.file:
            if line !="":
                bakwas, sub, guide = line.strip().split(";")
                self.tot = self.tot+1
                if(guide == self.current):
                    self.courses.append(sub)
        
        self.file.close()
        self.buttons =[]
        self.wrtfile = open("courses.txt", "a")
        for sub in self.courses :
            temp = self.count
            self.buttons.append(Button(text= sub, size_hint = (1, 0.05),pos_hint = {"x":0, "top":0.8-.05*self.count},font_size= 15, on_release = lambda x: self.enter_course(x = temp)))
            # self.buttons[self.count].bind(on_release = self.enter_course)
            self.ids.ides.add_widget(self.buttons[self.count])
            self.count= self.count+1

        
        


class TACourses(Screen):
    current = ""
    
    count=0
    def back(self):
        
        for button in self.buttons:
            self.ids.ides.remove_widget(button)
        sm.current = "main"
    
    
    def enter_course(self, x):
        CourseTA.currentTa = self.current
        CourseTA.currentProf = self.courses[x][1]
        CourseTA.currentCourse = self.courses[x][0]
        sm.current = "courseta"
        
    def on_enter(self, *args):
        self.file = open("courseta.txt", "r")
        self.courses = []
        self.count = 0
        
        for line in self.file:
            if line !="":
                sub, guide, ta = line.strip().split(";")
                
                if(ta == self.current):
                    self.courses.append((sub, guide))
        
        self.file.close()
        self.buttons =[]
        for sub in self.courses :
            temp = self.count
            self.buttons.append(Button(text= "Course:  "+sub[0]+"         Guide:  "+ sub[1], size_hint = (1, 0.05),pos_hint = {"x":0, "top":0.8-.05*self.count},font_size= 15, on_release = lambda x: self.enter_course(x = temp)))
            # self.buttons[self.count].bind(on_release = self.enter_course)
            self.ids.ides.add_widget(self.buttons[self.count])
            self.count= self.count+1

        
        

class STCourses(Screen):
    current = ""
    course_id = ObjectProperty(None)
    def req_button(self):
        if self.course_id.text != "":
            tempfile = open("courses.txt", "r")
            flag =0
            for line in tempfile:
                if line !="":
                    a, b, c = line.strip().split(";")
                    if(a==self.course_id.text and self.current != c):
                        reqf = open("strequest.txt", "a")
                        reqf.write(b+";"+c+";"+self.current+"\n")
                        reqf.close()
                        flag =1
                        break
            

            tempfile.close()
            if flag ==0:
                pop = Popup(title='Invalid Course ID',
                content=Label(text='Invalid Course ID'),
                size_hint=(None, None), size=(400, 400))
                pop.open()
            self.course_id.text = ""

    count=0
    def back(self):
        self.course_id.text = ""
        for button in self.buttons:
            self.ids.ides.remove_widget(button)
        sm.current = "main"
    
    
    def enter_course(self, x):
        CourseST.currentSt = self.current
        CourseST.currentProf = self.courses[x][1]
        CourseST.currentCourse = self.courses[x][0]
        sm.current = "coursest"
        
    def on_enter(self, *args):
        self.file = open("coursest.txt", "r")
        self.courses = []
        self.count = 0
        
        for line in self.file:
            if line !="":
                sub, guide, st = line.strip().split(";")
                
                if(st == self.current):
                    self.courses.append((sub, guide))
        
        self.file.close()
        self.buttons =[]
        for sub in self.courses :
            temp = self.count
            self.buttons.append(Button(text= "Course:  "+sub[0]+"         Guide:  "+ sub[1], size_hint = (1, 0.05),pos_hint = {"x":0, "top":0.8-.05*self.count},font_size= 15, on_release = lambda x: self.enter_course(x = temp)))
            # self.buttons[self.count].bind(on_release = self.enter_course)
            self.ids.ides.add_widget(self.buttons[self.count])
            self.count= self.count+1

        


class CourseTA(Screen):
    currentTa= ""
    currentProf =""
    currentCourse =""
    def add_assign_button(self):
        pass
    def on_enter(self, *args):
        pass

class CourseProf(Screen):
    currentProf =""
    currentCourse =""
    ta_id = ObjectProperty(None)
    def add_assign_button(self):
        pass

    def add_ta(self):
        if self.ta_id.text != "":
            tempf = open("users.txt", "r")
            flag =0
            for line in tempf:
                if line !="":
                    a, b, c ,d = line.strip().split(";")
                    if(a == self.ta_id.text):
                        flag =1
                        break
            tempf.close()
            if flag ==1:
                tempf = open("tarequest.txt", "a")
                tempf.write(self.currentCourse+";"+self.currentProf+";"+self.ta_id.text+"\n")
                tempf.close()
            else:
                pop = Popup(title='Error',
                          content=Label(text="User Not Available",font_size = 15),
                          size_hint=(None, None), size=(300, 200))
                pop.open()
            self.ta_id.text = ""
    def course_students(self):
        Students.currentProf = self.currentProf
        Students.currentCourse = self.currentCourse
        sm.current = "students"
    def on_enter(self, *args):
        tempf = open("courses.txt", "r")
        for line in tempf:
            if line !="":
                a, b, c = line.strip().split(";")
                
                if(b == self.currentCourse and c == self.currentProf):
                    pop = Popup(title='Course ID',
                              content=Label(text=a,font_size = 30),
                              size_hint=(None, None), size=(300, 200))
                    pop.open()
                    break

        tempf.close()
        

class Students(Screen):
    currentProf =""
    currentCourse =""
    def back(self):
        for button in self.buttons:
            self.ids.ides.remove_widget(button)

        with open("coursest.txt", "r") as f:
            lines = f.readlines()
        self.count=0
        with open("coursest.txt", "w") as f:
            f.write("")
            for line in lines:
                a, b, c = line.strip().split(";")
                if(a==currentCourse and b==currentProf):
                    if self.flag[self.count]==0:
                        pass
                    else:
                        f.write(line)
                    self.count= self.count+1
                else:
                    f.write(line)
                

        sm.current = "courseprof"


    def remove_student(self, x):
        self.flag[x]=0
        


    def on_enter(self, *args):
        self.students =[]
        self.flag =[]
        self.count =0
        tempf = open("coursest.txt", "r")
        for line in tempf:
            if line !="":
                a, b, c = line.strip().split(";")
                if(a==currentCourse and b==currentProf):
                    self.students.append(c)
                    self.flag.append(1)
        tempf.close()
        self.buttons =[]
        for student in self.students :
            temp = self.count
            self.buttons.append(Button(text= "Deregister: "+student, size_hint = (1, 0.02),pos_hint = {"x":0, "top":0.8-.02*self.count},font_size= 10, on_release = lambda x: self.remove_student(x = temp)))
            # self.buttons[self.count].bind(on_release = self.enter_course)
            self.ids.ides.add_widget(self.buttons[self.count])
            self.count= self.count+1


        



class CourseST(Screen):
    currentSt= ""
    currentProf =""
    currentCourse =""
    def on_enter(self, *args):
        pass

class ProfAssign(Screen):
    def back(self):
        sm.current = "courseprof"
    def upload_assgn(self):
        pass
    def upload_tc(self):
        pass
    def grade_button(self):
        sm.current = "gradeprof"
        pass
    def on_enter(self, *args):
        pass

class TaAssign(Screen):
    def back(self):
        sm.current = "courseta"
    def upload_assgn(self):
        pass
    def upload_tc(self):
        pass
    def grade_button(self):
        sm.current = "gradeta"
        pass
    def on_enter(self, *args):
        pass

class SubmitAssign(Screen):
    def back(self):
        sm.current = "coursest"
    def upload_assgn(self):
        pass
    def download_assgn(self):
        pass
    def on_enter(self, *args):
        pass

class GradeTA(Screen):
    def back(self):
        sm.current = "taassign"
    def on_enter(self, *args):
        pass
class GradeProf(Screen):
    def back(self):
        sm.current = "profassign"
    def on_enter(self, *args):
        pass

class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), 
Profile(name = "profile"),TARequests(name="tarequests"),STRequests(name="strequests"),STCourses(name="stcourses"),
TACourses(name="tacourses"),MyCourses(name="mycourses"),CourseTA(name="courseta"),CourseST(name="coursest"),CourseProf(name="courseprof"),
Students(name= "students"),ProfAssign(name="profassign"),SubmitAssign(name="submitassign"),TaAssign(name="taassign"),GradeTA(name="gradeta"),GradeProf(name="gradeprof")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        
        return sm


if __name__ == "__main__":
    MyMainApp().run()
