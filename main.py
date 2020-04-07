from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase


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


    def on_enter(self, *args):
        pass

class STRequests(Screen):
    current = ""

    
    def on_enter(self, *args):
        pass

class MyCourses(Screen):
    current = ""
    course = ObjectProperty(None)
    def add_button(self):
        if self.course.text != "":
            self.reset()

    def reset(self):
        pass
    def on_enter(self, *args):
        pass

class TACourses(Screen):
    current = ""

    
    def on_enter(self, *args):
        pass

class STCourses(Screen):
    current = ""
    course_id = ObjectProperty(None)
    def req_button(self):
        if self.course_id.text != "":
            self.course_id.text = ""

    
    def on_enter(self, *args):
        pass


class CourseTA(Screen):
    def add_assign_button(self):
        pass
    def on_enter(self, *args):
        pass

class CourseProf(Screen):
    ta_id = ObjectProperty(None)
    def add_assign_button(self):
        pass

    def add_ta(self):
        if self.ta_id.text != "":
            self.ta_id.text = ""
    def course_students(self):
        sm.current = "students"
    def on_enter(self, *args):
        pass

class Students(Screen):
    def back(self):
        sm.current = "courseprof"
    def on_enter(self, *args):
        pass


class CourseST(Screen):
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

sm.current = "profassign"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
