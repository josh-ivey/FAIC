from FAIC_Backend import *
import Tkinter as tk
import sys
#For Raspberry Pi: sys.path.append('/usr/local/lib/python2.7/site-packages')

###Only important parts of this code is commented, the reason for this is that because it is the frontend and produces the user interface, is it very repetitive and easy to comprehend

#SampleApp is the root "window"
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self._frame = SetupScreen(master=self.container, controller=self)

    def switch_frame(self, frame_class):
        #Destroys current frame and replaces it with a new one.
        new_frame = frame_class(master=self.container, controller=self)
        self._frame.destroy()
        self._frame = new_frame

#This screen is the initial screen, it pops up when no users are registered
class SetupScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        #This creates a blank canvas for everything to go on
        #Every screen has this, but with a different image for the background
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/setup_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        #This button proceeds to the setup
        setup_image = ImageTk.PhotoImage(file="Design/setup_screen_SETUP.png")
        s = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                   command=lambda: controller.switch_frame(RegisterNameScreen))
        
        s.config(image=setup_image)
        s.image=setup_image
        s_window = canvas.create_window(38,230, anchor='nw', window = s)

        #This creates the BASE class, to allow 1-User recognition as described in the report
        create_base()
        
        self.pack()

#Appears when the setup has been completed        
class SetupCompleteScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        Setup.complete = True

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/setup_complete_screen.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        thumbs_up_image = ImageTk.PhotoImage(file="Design/THUMBS_Y.png")
        t_u = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(RegisterNameScreen))
        t_u.config(image=thumbs_up_image)
        t_u.image=thumbs_up_image
        t_u_window = canvas.create_window(27,280, anchor='nw', window = t_u)

        thumbs_down_image = ImageTk.PhotoImage(file="Design/THUMBS_N.png")
        t_d = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(UnlockScreen))
        t_d.config(image=thumbs_down_image)
        t_d.image=thumbs_down_image
        t_d_window = canvas.create_window(178,280, anchor='nw', window = t_d)

        self.pack()

#This screen shows the user the Backup-PIN
class PINScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/backup_PIN_screen.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        #The PIN is generated from the backend, FAIC_backend.py
        Door.PIN = generate_PIN()

        PIN_label = tk.Label(self, bg="#244c6b", fg="white", width=9, height=1, font=("system", 40))
        PIN_label.configure(text=str(Door.PIN))
        PIN_window = canvas.create_window(160,240, anchor="center", window = PIN_label)

        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: controller.switch_frame(SetupCompleteScreen))
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(160,394, anchor='center', window = next_)

        self.pack()

#This is the "Home screen", this appears when somebody wants to unlock the door
class UnlockScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        unlock_button = ImageTk.PhotoImage(file="Design/unlock2.png")
        b = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                   command=lambda: controller.switch_frame(UnlockingScreen))
        
        b.config(image=unlock_button)
        b.image=unlock_button
        b_window = canvas.create_window(35,190, anchor='nw', window = b)

        self.pack()

#Unlocked screen appears either via face recognition or PIN entry
class UnlockedScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/unlockING_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        lmain = tk.Label(self)
        lmain_window = canvas.create_window(180,240, anchor="center", window = lmain)

        border = tk.Label(self, border = 0, bd = 0)
        border_window = canvas.create_window(160, 387, anchor="center", window = border)
        border_img = ImageTk.PhotoImage(file = "Design/unlockING_screen_border.png")
        border.imgtk = border_img
        border.configure(image=border_img)
            
        relock_button = ImageTk.PhotoImage(file="Design/unlockING_screen_relock.png")
        r = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(UnlockScreen))
        r.config(image=relock_button)
        r.image=relock_button
        r_window = canvas.create_window(23,351, anchor='nw', window = r)

        settings_button = ImageTk.PhotoImage(file="Design/unlockING_screen_settings.png")
        s = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(SettingsScreen))
        s.config(image=settings_button)
        s.image=settings_button
        s_window = canvas.create_window(172,351, anchor='nw', window = s)

        #This says "Welcome home " plus the name of whom is recognised, this is retrieved from the backend, FAIC_backend.py
        wh_label = tk.Label(self, bg="#1e4461", fg="white", width=40, height=1, font=("system", 16))
        wh_label.configure(text="Welcome home, " + Door.recognised + ".")
        wh_window = canvas.create_window(160,317, anchor="center", window = wh_label)
     
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        cap.set(4, 480)

        #This shows the user their face on the screen
        def show_frame():
            _, frame = cap.read()

            this_frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(this_frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        show_frame()
        self.pack()

#Occurs if the person is not recognised
class UnrecognisedScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/unlockING_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        lmain = tk.Label(self)
        lmain_window = canvas.create_window(180,240, anchor="center", window = lmain)

        border = tk.Label(self, border = 0, bd = 0)
        border_window = canvas.create_window(160, 387, anchor="center", window = border)
        border_img = ImageTk.PhotoImage(file = "Design/unlockING_screen_border.png")
        border.imgtk = border_img
        border.configure(image=border_img)
            
        retry_button = ImageTk.PhotoImage(file="Design/unlockING_screen_retry.png")
        r = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(UnlockingScreen))
        r.config(image=retry_button)
        r.image=retry_button
        r_window = canvas.create_window(23,351, anchor='nw', window = r)

        pin_button = ImageTk.PhotoImage(file="Design/unlockING_screen_PIN.png")
        s = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(EnterPINScreen))
        s.config(image=pin_button)
        s.image=pin_button
        s_window = canvas.create_window(172,351, anchor='nw', window = s)
        
        wh_label = tk.Label(self, bg="#162e42", fg="white", width=39, height=2, font=("system", 16))
        wh_label.configure(text="You're unrecognised: Retry or use PIN")
        wh_window = canvas.create_window(160,317, anchor="center", window = wh_label)
     
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        cap.set(4, 480)

        def show_frame():
            _, frame = cap.read()

            this_frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(this_frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        show_frame()
        self.pack()

#Class to contain numbers within the PIN screen, works similar to Person class
class Number(object):
    key = ""
    image = ""
    button = ""
    window= ""
    #Contains a set, alike Person
    numbers={}
    def __init__(self,key,button,image,window):
        self.key = key
        self.button = button
        self.image = image
        self.window = window

class EnterPINScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/enter_pin_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        keys = ["1","2","3","4","5","6","7","8","9","0"]
        h_align = 52
        v_align = 293

        #Keys are automatically generated through a for-loop instead of having to create the instances one by one
        #Images are assigned, along with their layouts and button events - enters the number into the entry field
        for i in range(len(keys)):
            if i == 3:
                v_align = 347
                h_align = 52
            elif i == 6:
                v_align = 401
                h_align = 52
            elif i == 9:
                v_align = 455
                h_align = 160

            Number.numbers[keys[i]] = Number("","","","")
            Number.numbers[keys[i]].key = keys[i]
            Number.numbers[keys[i]].image = ImageTk.PhotoImage(file="Design/Keys/" + Number.numbers[keys[i]].key + ".png")
            Number.numbers[keys[i]].button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                                       command = lambda i=i:enter_PIN.insert(len(enter_PIN.get()),Number.numbers[keys[i]].key))
            Number.numbers[keys[i]].button.config(image=Number.numbers[keys[i]].image)
            Number.numbers[keys[i]].button.image=Number.numbers[keys[i]].image
            Number.numbers[keys[i]].window = canvas.create_window(h_align,v_align, anchor='center', window = Number.numbers[keys[i]].button)
            h_align = h_align + 108

        enter_PIN = tk.Entry(self, width="12", font = "fixedsys 25 bold", bg="#244c6b", fg="white", justify='center')
        canvas.create_window(8,138, anchor='nw', window = enter_PIN)

        unlock_image = ImageTk.PhotoImage(file="Design/Keys/unlock.png")
        unlock_button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                    command=lambda: unlock_with_PIN(enter_PIN))
        unlock_button.config(image=unlock_image)
        unlock_button.image=unlock_image
        unlock_button_window = canvas.create_window(52,455, anchor='center', window = unlock_button)

        backspace_image = ImageTk.PhotoImage(file="Design/Keys/BACKSPACE_2.png")
        backspace_button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                    command=lambda: backspace(enter_PIN))
        backspace_button.config(image=backspace_image)
        backspace_button.image=backspace_image
        backspace_button_window = canvas.create_window(52+216,455, anchor='center', window = backspace_button)

        def unlock_with_PIN(pin):
            if str(pin.get()) == str(Door.PIN):
                Door.unlocked = True
                Door.recognised = "homeowner"
                controller.switch_frame(UnlockedScreen)
            else:
                pin.delete(0, tk.END)
                pin.insert(0, "INCORRECT")
                
        def backspace(entry):
            if entry.get() == "INCORRECT":
                entry.delete(0, tk.END)
            else:
                txt = entry.get()[:-1]
                entry.delete(0, tk.END)
                entry.insert(0, txt)

        self.pack()
        
class UnlockingScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.crop_img = 0
        self.remaining = 0
        self.take_picture_now = False
        
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()

        lmain = tk.Label(self)
        lmain_window = canvas.create_window(180,240, anchor="center", window = lmain)
        self.countdown(3)
		
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        cap.set(4, 480)

        def show_frame():
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y),(w+w, y+h), (255,255,255),4)
                roi_gray = gray[y:y+h, x:x+w]

            #Show persons face on the Tkinter window
            this_frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(this_frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

            if self.take_picture_now == True:
                try:
                    self.crop_img = frame[y:y+h, x:x+w]
                except UnboundLocalError:
                    self.countdown(3)
                    self.take_picture_now = False
                else:
                    cv2.imwrite("testing/recognise_me.jpg", self.crop_img)
                    self.take_picture_now = False
                    try:
                        #This is the recognition, obtained from the backend, FAIC_backend.py
                        #This uses training_PCA() and testing_PCA() to formulate the Eigenfaces and calulcate the weights to produce a response an alter the Door.unlocked variable
                        recognise_user()
                    except IndexError:
                        #If there was some error - namely not detecting a face, countdown from 3 and try again
                        self.take_picture_now = False
                        self.countdown(3)
                    else:
                        time.sleep(1)
                        if Door.unlocked == True:
                            #If they are recognised, unlock the door and welcome them home
                            show_recognised()
                        elif Door.unlocked == False:
                            #Otherwise, show a display where they can try again or enter the PIN
                            show_unrecognised()

        def show_recognised():
            controller.switch_frame(UnlockedScreen)

        def show_unrecognised():
            controller.switch_frame(UnrecognisedScreen)
            
        show_frame()
        self.pack()

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining
            
        if self.remaining <= 0:
            self.take_picture_now = True       
        else:                
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)
            
class SettingsScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/settings_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        go_back_button = ImageTk.PhotoImage(file="Design/go_back.png")
        g = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, 
                      command=lambda: controller.switch_frame(UnlockedScreen))
        g.config(image=go_back_button)
        g.image=go_back_button
        g_window = canvas.create_window(12, 8, anchor='nw', window = g)

        edit_users_button = ImageTk.PhotoImage(file="Design/settings_screen_EDITUSERS.png")
        e = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: controller.switch_frame(EnterNameForEditUserScreen))
        e.config(image=edit_users_button)
        e.image=edit_users_button
        e_window = canvas.create_window(14, 75, anchor='nw', window = e)

        new_user_button = ImageTk.PhotoImage(file="Design/settings_screen_ADDNEWUSER.png")
        n = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(RegisterNameScreen))
        n.config(image=new_user_button)
        n.image=new_user_button
        n_window = canvas.create_window(13,200, anchor='nw', window = n)

        change_PIN_button = ImageTk.PhotoImage(file="Design/settings_screen_CHANGEPIN.png")
        c = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(ChangePINScreen))
        c.config(image=change_PIN_button)
        c.image=change_PIN_button
        c_window = canvas.create_window(13,320, anchor='nw', window = c)

        self.pack()

class EnterNameForEditUserScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/enternameforedituser_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        go_back_button = ImageTk.PhotoImage(file="Design/go_back.png")
        g = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, 
                      command=lambda: controller.switch_frame(SettingsScreen))
        g.config(image=go_back_button)
        g.image=go_back_button
        g_window = canvas.create_window(12, 8, anchor='nw', window = g)

        keys = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "A", "S", "D", "F","G", "H", "J", "K", "L", "Y", "X", "C", "V", "B", "N", "M"] 
        h_align = 2
        v_align = 219
        for i in range(len(keys)):
            if i == 10:
                v_align = 271
                h_align = 18
            elif i == 19:
                v_align = 323
                h_align = 50
                
            Letter.letters[keys[i]] = Letter("","","","")
            Letter.letters[keys[i]].key = keys[i]
            Letter.letters[keys[i]].image = ImageTk.PhotoImage(file="Design/Keys/" + Letter.letters[keys[i]].key + ".png")
            Letter.letters[keys[i]].button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                                       command = lambda i=i:name.insert(len(name.get()),Letter.letters[keys[i]].key))
            Letter.letters[keys[i]].button.config(image=Letter.letters[keys[i]].image)
            Letter.letters[keys[i]].button.image=Letter.letters[keys[i]].image
            Letter.letters[keys[i]].window = canvas.create_window(h_align,v_align, anchor='nw', window = Letter.letters[keys[i]].button)
            h_align = h_align + 32

        name = tk.Entry(self, width="12", font = "fixedsys 25 bold", bg="#244c6b", fg="white", justify='center')
        canvas.create_window(8,102, anchor='nw', window = name)

        ## Create a space in the entry field
        space_image = ImageTk.PhotoImage(file="Design/Keys/SPACE.png")
        space = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: name.insert(len(name.get())," "))
        space.config(image=space_image)
        space.image=space_image
        space_window = canvas.create_window(3,368, anchor='nw', window = space)
        
        ## Next part of register process
        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: editUser())
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(88,429, anchor='nw', window = next_)

        ## Take away last letter of entry field
        back_image = ImageTk.PhotoImage(file="Design/Keys/BACKSPACE.png")
        back = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: backspace(name))
        back.config(image=back_image)
        back.image=back_image
        back_window = canvas.create_window(280,323, anchor='nw', window = back)

        ## Method for backspace to use
        def backspace(entry):
            txt = entry.get()[:-1]
            entry.delete(0, tk.END)
            entry.insert(0, txt)

        def create_model():

            model_image = ImageTk.PhotoImage(file = "Design/model2.png")
            model = tk.Label(self, bd =0, border = 0)
            model.config(image=model_image)
            model.image=model_image
            model_window = canvas.create_window(160,244, anchor="center", window = model)
            
            ok_image = ImageTk.PhotoImage(file="Design/model_ok.png")
            ok = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: rid_model(model,ok))
            ok.config(image=ok_image)
            ok.image=ok_image
            ok_window = canvas.create_window(160,365, anchor='center', window = ok)

        def rid_model(this,that):
            this.destroy()
            that.destroy()

        def editUser():
            Person.this_name = name.get()
            controller.switch_frame(EditUserScreen)

        self.pack()

class EditUserScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/editusers_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        name_label = tk.Label(self, bg="#204967", fg="white", width=12, height=1, font=("system", 18))
        name_label.configure(text=Person.this_name)
        name_window = canvas.create_window(200,40, anchor="center", window = name_label)

        face = tk.Label(self, bg="black", border = 0, bd = 0, highlightthickness = 0)
        face_w = canvas.create_window(160, 178, anchor="center", window = face)
        face_img = Image.open("C:/Users/Josh/Desktop/learning/training/" + Person.this_name + "/1.jpg")
        face_img = face_img.resize((180, 180), Image.ANTIALIAS) #The (250, 250) is (height, width)
        face_img = ImageTk.PhotoImage(face_img)
        face.imgtk = face_img
        face.configure(image=face_img)

        go_back_button = ImageTk.PhotoImage(file="Design/go_back.png")
        g = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(SettingsScreen))
        g.config(image=go_back_button)
        g.image=go_back_button
        g_window = canvas.create_window(12, 8, anchor='nw', window = g)

        rename_image = ImageTk.PhotoImage(file="Design/editusers_screen_RENAME.png")
        rename = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                           command=lambda: controller.switch_frame(RenameScreen))
        rename.config(image=rename_image)
        rename.image=rename_image
        rename_window = canvas.create_window(16,282, anchor='nw', window = rename)

        recalib_image = ImageTk.PhotoImage(file="Design/editusers_screen_RECALIB.png")
        recalib = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                            command=lambda: controller.switch_frame(PreRegisterFaceScreen))
        recalib.config(image=recalib_image)
        recalib.image=recalib_image
        recalib_window = canvas.create_window(16,346, anchor='nw', window = recalib)

        delete_image = ImageTk.PhotoImage(file="Design/editusers_screen_DELETE.png")
        delete = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                           command=lambda: controller.switch_frame(DeleteScreen))
        delete.config(image=delete_image)
        delete.image=delete_image
        delete_window = canvas.create_window(16,410, anchor='nw', window = delete)

        self.pack()

class DeleteScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/delete.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: delete_user())
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(160,394, anchor='center', window = next_)

        def after_delete():
            if Person.num_instances == 1:
                controller.switch_frame(SetupScreen)
            else:
                controller.switch_frame(SettingsScreen)

        def delete_user():
            path = "training/" + Person.this_name
            shutil.rmtree(path, ignore_errors=False, onerror=None)
            del Person.people[Person.this_name]
            Person.num_instances = Person.num_instances - 1
            
            ##if Person.num_instance == 0:
            deleted_image = ImageTk.PhotoImage(file = "Design/deleted.png")
            deleted = tk.Label(self, bd =0, border = 0)
            deleted.config(image=deleted_image)
            deleted.image=deleted_image
            deleted_window = canvas.create_window(160,240, anchor="center", window = deleted)

            name_label = tk.Label(self, bg="#204967", fg="white", width=12, height=1, font=("system", 18))
            name_label.configure(text=Person.this_name)
            name_window = canvas.create_window(160,160, anchor="center", window = name_label)

            next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
            next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                command=lambda: after_delete())
            next_.config(image=next_image)
            next_.image=next_image
            next_window = canvas.create_window(160,394, anchor='center', window = next_)
                

        self.pack()

class RenameScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/rename_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        go_back_button = ImageTk.PhotoImage(file="Design/go_back.png")
        g = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                      command=lambda: controller.switch_frame(EditUserScreen))
        g.config(image=go_back_button)
        g.image=go_back_button
        g_window = canvas.create_window(12, 8, anchor='nw', window = g)

        keys = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "A", "S", "D", "F","G", "H", "J", "K", "L", "Y", "X", "C", "V", "B", "N", "M"] 
        h_align = 2
        v_align = 219
        for i in range(len(keys)):
            if i == 10:
                v_align = 271
                h_align = 18
            elif i == 19:
                v_align = 323
                h_align = 50
                
            Letter.letters[keys[i]] = Letter("","","","")
            Letter.letters[keys[i]].key = keys[i]
            Letter.letters[keys[i]].image = ImageTk.PhotoImage(file="Design/Keys/" + Letter.letters[keys[i]].key + ".png")
            Letter.letters[keys[i]].button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                                       command = lambda i=i:name.insert(len(name.get()),Letter.letters[keys[i]].key))
            Letter.letters[keys[i]].button.config(image=Letter.letters[keys[i]].image)
            Letter.letters[keys[i]].button.image=Letter.letters[keys[i]].image
            Letter.letters[keys[i]].window = canvas.create_window(h_align,v_align, anchor='nw', window = Letter.letters[keys[i]].button)
            h_align = h_align + 32

        new_name = tk.Entry(self, width="12", font = "fixedsys 25 bold", bg="#244c6b", fg="white", justify='center')
        canvas.create_window(8,102, anchor='nw', window = new_name)

        ## Create a space in the entry field
        space_image = ImageTk.PhotoImage(file="Design/Keys/SPACE.png")
        space = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: new_name.insert(len(new_name.get())," "))
        space.config(image=space_image)
        space.image=space_image
        space_window = canvas.create_window(3,368, anchor='nw', window = space)
        
        ## Next part of register process
        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: rename_user())
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(88,429, anchor='nw', window = next_)

        ## Take away last letter of entry field
        back_image = ImageTk.PhotoImage(file="Design/Keys/BACKSPACE.png")
        back = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: backspace(new_name))
        back.config(image=back_image)
        back.image=back_image
        back_window = canvas.create_window(280,323, anchor='nw', window = back)

        ## Method for backspace to use
        def backspace(entry):
            txt = entry.get()[:-1]
            entry.delete(0, tk.END)
            entry.insert(0, txt)

        #This pops up if there is an error, namely if a username is already taken
        def create_model():
            model_image = ImageTk.PhotoImage(file = "Design/model.png")
            model = tk.Label(self, bd =0, border = 0)
            model.config(image=model_image)
            model.image=model_image
            model_window = canvas.create_window(160,244, anchor="center", window = model)
            
            ok_image = ImageTk.PhotoImage(file="Design/model_ok.png")
            ok = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: rid_model(model,ok))
            ok.config(image=ok_image)
            ok.image=ok_image
            ok_window = canvas.create_window(160,365, anchor='center', window = ok)

        def rid_model(this,that):
            this.destroy()
            that.destroy()

        def renamed():
            renamed_image = ImageTk.PhotoImage(file = "Design/renamed.png")
            renamed = tk.Label(self, bd =0, border = 0)
            renamed.config(image=renamed_image)
            renamed.image=renamed_image
            renamed_window = canvas.create_window(160,240, anchor="center", window = renamed)

            old_name_label = tk.Label(self, bg="#204967", fg="white", width=12, height=1, font=("system", 18))
            old_name_label.configure(text=Person.this_name)
            old_name_window = canvas.create_window(160,92, anchor="center", window = old_name_label)

            new_name_label = tk.Label(self, bg="#204967", fg="white", width=12, height=1, font=("system", 18))
            new_name_label.configure(text=new_name.get())
            new_name_window = canvas.create_window(160,306, anchor="center", window = new_name_label)

            next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
            next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                command=lambda: controller.switch_frame(SettingsScreen))
            next_.config(image=next_image)
            next_.image=next_image
            next_window = canvas.create_window(160,394, anchor='center', window = next_)
            

        def rename_user():
            try:
                #Folder is renamed first
                os.rename(str(Person.people[Person.this_name].folder), "training/" + new_name.get())
            except Exception:
                #Somebody is already called that
                new_name.delete(0, tk.END)
                create_model()
            else:
                Person.people[new_name.get()] = Person.people.pop(Person.this_name)
                Person.people[new_name.get()].folder = "training/" + new_name.get()

                renamed()
                Person.this_name = new_name.get()
                                               
        self.pack()

class ChangePINScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/are_you_sure_change_pin_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        thumbs_up_image = ImageTk.PhotoImage(file="Design/THUMBS_Y.png")
        t_u = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(NewPINScreen))
        t_u.config(image=thumbs_up_image)
        t_u.image=thumbs_up_image
        t_u_window = canvas.create_window(27,280, anchor='nw', window = t_u)

        thumbs_down_image = ImageTk.PhotoImage(file="Design/THUMBS_N.png")
        t_d = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                        command=lambda: controller.switch_frame(SettingsScreen))
        t_d.config(image=thumbs_down_image)
        t_d.image=thumbs_down_image
        t_d_window = canvas.create_window(178,280, anchor='nw', window = t_d)        

        self.pack()

class NewPINScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/new_pin_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        Door.PIN = generate_PIN()

        PIN_label = tk.Label(self, bg="#244c6b", fg="white", width=9, height=1, font=("system", 40))
        PIN_label.configure(text=str(Door.PIN))
        PIN_window = canvas.create_window(160,240, anchor="center", window = PIN_label)

        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: controller.switch_frame(SettingsScreen))
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(160,394, anchor='center', window = next_)      

        self.pack()

class Letter(object):
    key = ""
    image = ""
    button = ""
    window= ""
    letters={}
    def __init__(self,key,button,image,window):
        self.key = key
        self.button = button
        self.image = image
        self.window = window

class RegisterNameScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/register_screen_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        #This automatically generates the letters within a for loop, it lays out the images of the keys and assigns their button events to enter the desired key into the entry field
        keys = ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "A", "S", "D", "F","G", "H", "J", "K", "L", "Y", "X", "C", "V", "B", "N", "M"] 
        h_align = 2
        v_align = 219
        for i in range(len(keys)):
            if i == 10:
                v_align = 271
                h_align = 18
            elif i == 19:
                v_align = 323
                h_align = 50
                
            Letter.letters[keys[i]] = Letter("","","","")
            Letter.letters[keys[i]].key = keys[i]
            Letter.letters[keys[i]].image = ImageTk.PhotoImage(file="Design/Keys/" + Letter.letters[keys[i]].key + ".png")
            Letter.letters[keys[i]].button = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                                                       command = lambda i=i:name.insert(len(name.get()),Letter.letters[keys[i]].key))
            Letter.letters[keys[i]].button.config(image=Letter.letters[keys[i]].image)
            Letter.letters[keys[i]].button.image=Letter.letters[keys[i]].image
            Letter.letters[keys[i]].window = canvas.create_window(h_align,v_align, anchor='nw', window = Letter.letters[keys[i]].button)
            h_align = h_align + 32

        name = tk.Entry(self, width="12", font = "fixedsys 25 bold", bg="#244c6b", fg="white", justify='center')
        canvas.create_window(8,102, anchor='nw', window = name)

        ## Create a space in the entry field
        space_image = ImageTk.PhotoImage(file="Design/Keys/SPACE.png")
        space = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: name.insert(len(name.get())," "))
        space.config(image=space_image)
        space.image=space_image
        space_window = canvas.create_window(3,368, anchor='nw', window = space)
        
        ## Next part of register process
        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0,
                          command=lambda: createUserFromEntry())
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(88,429, anchor='nw', window = next_)

        ## Take away last letter of entry field
        back_image = ImageTk.PhotoImage(file="Design/Keys/BACKSPACE.png")
        back = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: backspace(name))
        back.config(image=back_image)
        back.image=back_image
        back_window = canvas.create_window(280,323, anchor='nw', window = back)

        ## Method for backspace to use
        def backspace(entry):
            txt = entry.get()[:-1]
            entry.delete(0, tk.END)
            entry.insert(0, txt)

        def create_model():

            model_image = ImageTk.PhotoImage(file = "Design/model.png")
            model = tk.Label(self, bd =0, border = 0)
            model.config(image=model_image)
            model.image=model_image
            model_window = canvas.create_window(160,244, anchor="center", window = model)
            
            ok_image = ImageTk.PhotoImage(file="Design/model_ok.png")
            ok = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda: rid_model(model,ok))
            ok.config(image=ok_image)
            ok.image=ok_image
            ok_window = canvas.create_window(160,365, anchor='center', window = ok)

        def rid_model(this,that):
            this.destroy()
            that.destroy()

        def createUserFromEntry():
            
            Person.this_name = name.get()
            ## CALLING make_person FROM Setup_and_recognise.py
            try:
                Person.people[Person.this_name] = make_person(Person.this_name, "training/" + Person.this_name + "/")
            except Exception:
                name.delete(0, tk.END)
                create_model()
            else:
                ## Go to take pictures screen
                controller.switch_frame(PreRegisterFaceScreen)

        self.pack()

class PreRegisterFaceScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        background_image = ImageTk.PhotoImage(file = "Design/register_screen_2_background.png")
        canvas.create_image(160, 240, image=background_image)
        canvas.image=background_image

        next_image = ImageTk.PhotoImage(file="Design/Keys/NEXT.png")
        next_ = tk.Button(self, border = 0, highlightthickness = 0, bd = 0, command=lambda:controller.switch_frame(RegisterFaceScreen))
        next_.config(image=next_image)
        next_.image=next_image
        next_window = canvas.create_window(88,429, anchor='nw', window = next_)

        self.pack()
        
class RegisterFaceScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.remaining = 0
        self.take_picture_now = False
        self.pictures_taken = 0
        self.timing_fudge = -20
        self.crop_img = 0
        self.refresh_ = False
        
        canvas = tk.Canvas(self, width=320, height=480)
        canvas.pack()
        
        lmain = tk.Label(self)
        lmain_window = canvas.create_window(180,240, anchor="center", window = lmain)

        #This is a countdown timer label that counts down from 2
        self.timer = tk.Label(self, bg="#244c6b", fg="white", width=4, height=2, font=("system", 32))
        self.timer_window = canvas.create_window(240,415, anchor="center", window = self.timer)
        self.countdown(2)

        self.calibration = tk.Label(self, bg="black")
        self.calibration_w = canvas.create_window(160, 240, anchor="center", window = self.calibration)
        self.calibration_img = ImageTk.PhotoImage(file = "Design/takepics/CALIB.png")
        self.calibration.imgtk = self.calibration_img
        self.calibration.configure(image=self.calibration_img)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        cap.set(3, 480)
        cap.set(4, 480)
        
        def show_frame():
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y),(w+w, y+h), (255,255,255),4)
                roi_gray = gray[y:y+h, x:x+w]

            #Display the frame in the Tkinter window so that the user can see their face - this helps detect the face    
            this_frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(this_frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

            #Take 5 pictures
            for i in range(5):
                if self.take_picture_now == True:
                    if self.pictures_taken == i:
                        try:
                            self.crop_img = frame[y:y+h, x:x+w] #Crop the image
                        except UnboundLocalError:
                            #If for some reason it didn't work, try it again
                            self.countdown(2)
                            self.take_picture_now = False
                        else:
                            #Save the images in the folder allocated with the users name
                            cv2.imwrite("training/" + Person.this_name + "/" + str(i+1) + ".jpg", self.crop_img)
                            self.take_picture_now = False
                            self.pictures_taken = self.pictures_taken + 1
                            self.countdown(2)

                            #Change calibration position for every picture
                            if i == 0:
                                canvas.coords(self.calibration_w,(10,300))
                            elif i == 1:
                                canvas.coords(self.calibration_w,(300,200))                               
                            if i == 2:
                                canvas.coords(self.calibration_w,(50,400))
                            elif i == 3:
                                canvas.coords(self.calibration_w,(300,50))
                            elif i == 4:
                                if Setup.complete == False:
                                    controller.switch_frame(PINScreen)
                                elif Setup.complete == True:
                                    controller.switch_frame(UnlockScreen)

        show_frame()
        
    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining
            
        if self.remaining <= 0:
            self.timer.configure(text="0")
            self.take_picture_now = True
            
        else:
            self.timer.configure(text=str(self.remaining))
            self.remaining = self.remaining - 1
            self.timer.after(1000, self.countdown)

        self.pack()
        
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
