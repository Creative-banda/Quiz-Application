from customtkinter import *
from pyautogui import size
from tkinter import messagebox,ttk,Radiobutton
import mysql.connector as mycon
import tkinter as tk
from PIL import Image,ImageTk
import json
from time import sleep
from threading import Thread

set_appearance_mode("Dark")

width,height = size()
count = 0
fnt = ("ariel",10,"bold")
font_for_radiobutton = ("Century751 SeBd BT",15,"bold")
cnt = 0
score = 0
timer_contidion = True


dic = {
    "Question" : [],
    "Option" : [],
    "Right_Answer" : [],
    "Timer" : []
}

con = True


#######################    Functions      ##########################


########         TimerFunctions      #########################


def set_Timer():
    global dic,data,second_win
    timer_list = []
    global hour_entry,min_entry,second_entry
    
    hr = hour_entry.get()
    sec = second_entry.get()
    minute = min_entry.get()
    
    try:
        int(hr),int(sec),int(minute)
    except:
        messagebox.showerror("Check","Please Check The Timer")
        return False
    timer_list.append(hr)
    timer_list.append(minute)
    timer_list.append(sec)
    with open(f"C:/Quiz_User/{user_info.get()}/{grade_Location.get()}/{file_loc.get()}.json","r") as f:
        try:
            data = json.load(f)
        except:
            data = dic
        if data['Timer'] != []:
            data['Timer'].clear()
        data["Timer"].append(timer_list)

        with open(f"C:\Quiz_User\{user_info.get()}\{grade_Location.get()}\{file_loc.get()}.json", "w") as json_object:
            json.dump(data,json_object)
        messagebox.showinfo("Timer Set","Timer Setted Sucessfully")
        second_win.forget(second_win)

def click_Timer():
    global hour_entry,min_entry,second_entry,second_win
    second_win = CTkToplevel()
    second_win.title("Create File")
    second_win.geometry("500x250")
    second_win.wm_resizable(False,False)
    CTkLabel(second_win,text="Set Timer",font=("Ubuntu",30),fg_color='#515457',height=50).pack(fill = BOTH)
    
    frame = CTkFrame(second_win)
    frame.pack()

    hour_entry = CTkEntry(frame,height=50,width=100,placeholder_text="Hrs ",font=('B612 Mono',10,'bold'))
    hour_entry.pack(side = LEFT,pady = 20)
    
    min_entry = CTkEntry(frame,height=50,width=100,placeholder_text="Min ",font=('B612 Mono',10,'bold'))
    min_entry.pack(side = LEFT,pady = 20,padx=20)
    
    second_entry = CTkEntry(frame,height=50,width=100,placeholder_text="Sec",font=('B612 Mono',10,'bold'))
    second_entry.pack(pady = 20)

    button = CTkButton(second_win,text = "Set Timer",command=set_Timer)
    button.pack(pady = 40)

def CountingTimer():
    global score,len_of_question
    hr = data["Timer"][0][0]
    minu = data["Timer"][0][1]
    sec = data["Timer"][0][2]

    hr = int(hr)
    minu = int(minu)
    sec = int(sec)
    len_of_question = len(data['Question'])

    while timer_contidion:
        if sec == 0 and minu != 0:
            minu-=1
            sec = 60
            
        if minu == 0 and hr != 0:
            hr-=1
            minu = 60
        if minu == 0 and sec == 0 and hr == 0:
            messagebox.showinfo("Opps Time Over","Time over Better Luck Next Time")
            Score_label.configure(text=f"You got {score} out of {len_of_question}")
            real_quiz_frame.pack_forget()
            result_frame.pack(fill = BOTH,expand = YES)
            return False
        sec-=1
        sleep(1)
        Timer_Label.configure(text = f"{hr}Hour {minu} Minute {sec} second")

########         TimerFunctions      #########################

def button_pressed(text):
    global data


    file_loc.set(text)
    Choose_Question_Frame.pack_forget()
    Question_entrying_frame.pack(fill = 'both',expand = 'yes')
    with open(f"C:/Quiz_User/{user_info.get()}/{grade_Location.get()}/{file_loc.get()}.json","r") as f:

        data = json.load(f)
        print("Data_Loaded Done From Button Pressed")
        
        
def button_pressed_for_student(text):
    global data
    
    file_loc.set(text)

    Student_Choose_Question.pack_forget()
    real_quiz_frame.pack(fill = 'both',expand = 'yes')
    with open(f"C:/Quiz_User/Executed_Files/Grade{class_combo.get()}/{file_loc.get()}.json","r") as f:
        print(f"Grade{class_combo.get()}")

        data = json.load(f)
        next()
        Thread(target=CountingTimer).start()

def back_to_Choose_Question():
    Question_entrying_frame.pack_forget()
    Choose_Question_Frame.pack(fill=BOTH,expand=YES)

def real_creation():
    global data
    if entry.get() == "":
        messagebox.showwarning("Warning","Please Choose a Name For The File")
    else:
        Choose_Question_Frame.pack_forget()
        win.forget(win)

        Question_entrying_frame.pack(fill = BOTH,expand = YES)
        file_loc.set(entry.get())
        with open(f"C:/Quiz_User/{user_info.get()}/{grade_Location.get()}/{file_loc.get()}.json","w") as f:
            try:
                data = json.load(f)
                print("Loaded")
            except:
                print("Not Loaded")

def create_file():
    global entry,win
    win = CTkToplevel()
    win.title("Create File")
    win.geometry("500x500")
    win.wm_resizable(False,False)

    CTkLabel(win,text="Create New File",font=("Ubuntu",30),fg_color='#515457',height=50).pack(fill = BOTH)

    label = CTkLabel(win,text="File Name",anchor='s',font=('ariel',10,'bold'),height= 50)
    label.pack(anchor = 'w',padx = 60)

    entry = CTkEntry(win,height=30,width=300,placeholder_text="Enter File Name ",font=('B612 Mono',10,'bold'))
    entry.pack(pady = 20)

    button = CTkButton(win,text = "Create File",command=real_creation)
    button.pack()

def packing_button():
    global con

    d = f"C:\Quiz_User\{user_info.get()}\{grade_Location.get()}"
    for widget in second_frame.winfo_children():
        widget.destroy()
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            lis = full_path.split('\\')
            out = lis[-1]
            file = out.split('.')
            lis = file[0].split('/n')
            con = False
            for txt in lis:
                CTkButton(second_frame,text=txt,
                        command=lambda m=txt: button_pressed(m),
                        height=50,font=("Corbel",20)).pack(fill = 'both',pady = 10)
    if con == True:
        CTkLabel(second_frame,text = 'Create a File',font=("B612 Mono",30)).pack(pady = 200)
        print("Done")

def back_to_Grade():
    Choose_Question_Frame.pack_forget()
    Grade_Choose_Question.pack(fil= BOTH,expand = YES)

def packing_button_for_Student():
    global con
    try:
        d = f"C:\Quiz_User\Executed_Files/Grade{class_combo.get()}"
        for path in os.listdir(d):
            full_path = os.path.join(d, path)
            if os.path.isfile(full_path):
                lis = full_path.split('\\')
                out = lis[-1]
                file = out.split('.')
                lis = file[0].split('/n')
                con = False
                for txt in lis:
                    CTkButton(Right_Frame,text=txt,
                            command=lambda m=txt: button_pressed_for_student(m),
                            height=50,font=("Corbel",20)).pack(fill = 'both',pady = 10)
    except:
        pass
    if con == True:
        CTkLabel(Right_Frame,text = 'Sorry No Exam is There',font=("B612 Mono",30)).pack(pady = height/3)

def execute_File():
    global destination_path,data
    
    source_path = f"C:/Quiz_User/{user_info.get()}/{grade_Location.get()}/{file_loc.get()}.json"
    destination_path = f"C:/Quiz_User/Executed_Files/{grade_Location.get()}/{file_loc.get()}.json"
    

    if os.path.exists(destination_path):
        res = messagebox.askyesno("Confirmation", "Do you want to Unexecute this file?")
        if res:
            os.remove(destination_path)  
            print("File Unexecuted")
    else:
        result = messagebox.askyesno("Confirmation", "Do you really want to Execute this file?")
        if result:
            if data['Timer'] == []:
                messagebox.showwarning("Timer","Please Set The Timer ")
                return False
            print("Done")
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
  
            with open(source_path, 'rb') as source_file:
                with open(destination_path, 'wb') as destination_file:
                    destination_file.write(source_file.read())
                    
            print("File Executed")
        else:
            print("No")
            return False

def back_from_create_teacher_account():
    create_password_frame.pack_forget()
    login_frame.pack(fill = BOTH,expand = YES)

def previous_que():
    global cnt,len_of_question,data
    cnt-=1


    if cnt == 0:
        l_question_in_pre_frame.configure(state = DISABLED)

    if cnt != len_of_question:
        n_question_in_pre_frame.configure(state = NORMAL)


    p_question_entry.delete(0,END),p_option_1_entry.delete(0,END),p_option_2_entry.delete(0,END),p_option_3_entry.delete(0,END),p_option_4_entry.delete(0,END),p_r_ans_entry.delete(0,END)

    try:
        p_question_entry.insert(0,data['Question'][cnt]),p_option_1_entry.insert(0,data['Option'][cnt][0]),p_option_2_entry.insert(0,data['Option'][cnt][1]),p_option_3_entry.insert(0,data['Option'][cnt][2]),p_option_4_entry.insert(0,data['Option'][cnt][3]),p_r_ans_entry.insert(0,data['Right_Answer'][cnt])
    except:
        l_question_in_pre_frame.configure(state = DISABLED)

def previous_question_frame_function():
    global data,cnt,len_of_question


    cnt = 0

    p_question_entry.delete(0,END),p_option_1_entry.delete(0,END),p_option_2_entry.delete(0,END),p_option_3_entry.delete(0,END),p_option_4_entry.delete(0,END),p_r_ans_entry.delete(0,END)

    p_question_entry.insert(0,data['Question'][cnt]),p_option_1_entry.insert(0,data['Option'][cnt][0]),p_option_2_entry.insert(0,data['Option'][cnt][1]),p_option_3_entry.insert(0,data['Option'][cnt][2]),p_option_4_entry.insert(0,data['Option'][cnt][3]),p_r_ans_entry.insert(0,data['Right_Answer'][cnt])


    len_of_question = len(data['Question'])

    if len_of_question == cnt+1:
        l_question_in_pre_frame.configure(state = DISABLED)
        n_question_in_pre_frame.configure(state = DISABLED)
    else:
        n_question_in_pre_frame.configure(state = NORMAL)

    Question_entrying_frame.pack_forget()
    preview_frame.pack(fill = 'both',expand = 'yes')

def show_folder_count():
    folder_path = f"C:/Quiz_User/{user_info.get()}"
    folder_names = get_folder_names(folder_path)
    create_folder_buttons(folder_names)

def get_folder_names(folder_path):    
    folder_names = []
    
    for item in os.listdir(folder_path):
        
        if os.path.isdir(os.path.join(folder_path, item)):
            
            folder_names.append(item)
    folder_names.sort(key=lambda x: int(x.replace('Grade', '')))
    return folder_names

def button_click(folder_name):
    grade_Location.set(folder_name)
    packing_button()    
    Grade_Choose_Question.pack_forget()
    Choose_Question_Frame.pack(fill= BOTH,expand = YES)
    
def create_folder_buttons(folder_names):
    
    # Clear any existing buttons
    
    for widget in Right_Frame_of_Grade.winfo_children():
        
        widget.destroy()
    
    # Create a button for each folder name
    CTkLabel(Right_Frame_of_Grade,text="Choose Grade To Continue",font=("ariel",30,"bold")).pack(fill=BOTH,pady=20)
    for folder_name in folder_names:
        folder_button = CTkButton(Right_Frame_of_Grade, text=folder_name, command=lambda name=folder_name: button_click(name),height=50,font=('ariel',20,"bold"))
        folder_button.pack(pady=5,fill = BOTH)

def next_que():
    global cnt,len_of_question,data

    cnt+=1

    if cnt == len_of_question-1:
        n_question_in_pre_frame.configure(state = DISABLED)
    if cnt != 0:
        l_question_in_pre_frame.configure(state = NORMAL)



    p_question_entry.delete(0,END),p_option_1_entry.delete(0,END),p_option_2_entry.delete(0,END),p_option_3_entry.delete(0,END),p_option_4_entry.delete(0,END),p_r_ans_entry.delete(0,END)

    try:
        p_question_entry.insert(0,data['Question'][cnt]),p_option_1_entry.insert(0,data['Option'][cnt][0]),p_option_2_entry.insert(0,data['Option'][cnt][1]),p_option_3_entry.insert(0,data['Option'][cnt][2]),p_option_4_entry.insert(0,data['Option'][cnt][3]),p_r_ans_entry.insert(0,data['Right_Answer'][cnt])
    except:
        n_question_in_pre_frame.configure(state = DISABLED)

def next():
    global data
    global count,score,timer_contidion,len_of_question
    global r11,r22,r33,r44
    
    check=0
    val = opt.get()

    if val == "Hello" and check!=0:
        messagebox.showwarning("Not Valid","Please Select One Option To Continue")
        return False

    check=1

    try:
        if val == data['Right_Answer'][count-1]:
            score+=1
        var.set(f"Question {count+1} : "+data['Question'][count]),r11.set(data['Option'][count][0]),r22.set(data['Option'][count][1]),r33.set(data['Option'][count][2]),r44.set(data['Option'][count][3])
        
        
        r1.config(value=data['Option'][count][0]),r2.config(value=data['Option'][count][1]),r3.config(value=data['Option'][count][2]),r4.config(value=data['Option'][count][3])

        print(val,data['Right_Answer'][count],score)
    except:
        len_of_question = len(data['Question'])
        Score_label.configure(text=f"You got {score} out of {len_of_question}")
        Entering_Studata_intoDB()
        real_quiz_frame.pack_forget()
        timer_contidion = False
        result_frame.pack(fill=BOTH,expand=YES)

    count+=1

def sub_que():
    global dic,data

    if question_entry.get() == "":
        messagebox.showinfo('< Question >',"Please Entry Question To Continue")
        return False
    elif option_1_entry.get() == '' or  option_2_entry.get() == '' or option_3_entry.get() == '' or option_4_entry.get() == '' or  r_ans.get() == '':
        messagebox.showinfo('< Option >',"Please Choose Option")
        return False

    opt_list = []
    with open(f"C:/Quiz_User/{user_info.get()}/{grade_Location.get()}/{file_loc.get()}.json","r") as f:
        try:
            data = json.load(f)
            print("loaded")
        except:
            data = dic
            print("loaded dic")
    opt_list.append(option_1_entry.get()),opt_list.append(option_2_entry.get()),opt_list.append(option_3_entry.get()),opt_list.append(option_4_entry.get())

    data["Question"].append(question_entry.get())
    data["Option"].append(opt_list)
    data["Right_Answer"].append(r_ans.get())



    with open(f"C:\Quiz_User\{user_info.get()}\{grade_Location.get()}\{file_loc.get()}.json", "w") as json_object:
        json.dump(data,json_object)



    question_entry.delete(0,END),option_1_entry.delete(0,END),option_2_entry.delete(0,END),option_3_entry.delete(0,END),option_4_entry.delete(0,END)
    r_ans.set('')

def create_new_acc():
    login_frame.pack_forget()
    create_password_frame.pack(fill = BOTH,expand = YES)

def Entering_Studata_intoDB():
    global score,name_Entry,class_var,Roll_no_Entry,section_combo,gender
    try:
        conn = mycon.connect(host = "localhost",
                            user = "root",
                            password = "",
                            database = "quiz")

    except:
        messagebox.showerror("Error","Not Able To Connect To The DataBase")
        return False

    try:
        cur = conn.cursor()
        cmd = "insert into stu_info (name,class,roll_no,section,gender,score) values (%s,%s,%s,%s,%s,%s)"
        
        val = (name_Entry.get(),class_var.get(),Roll_no_Entry.get(),var_combo.get(),gender.get(),score)
        cur.execute(cmd,val)
        conn.commit()
        messagebox.showinfo("Done","Congratulations! You Completed The Quiz !")
    except:
        messagebox.showerror("Error","Not Able To Insert Data")
        return False

def click(event):
    r_ans['values'] = (option_1_entry.get(),option_2_entry.get(),option_3_entry.get(),option_4_entry.get())

def click_in_preview_frame(event):
    p_r_ans_entry['values'] = (p_option_1_entry.get(),p_option_2_entry.get(),p_option_3_entry.get(),p_option_4_entry.get())

def make_change():
    global data,cnt

    list1 = [p_question_entry.get(),p_option_1_entry.get(),p_option_2_entry.get(),p_option_3_entry.get(),p_option_4_entry.get(),p_r_ans_entry.get()]

    list2 = [data['Question'][cnt],data['Option'][cnt][0],data['Option'][cnt][1],data['Option'][cnt][2],data['Option'][cnt][3],data['Right_Answer'][cnt]]


    if list1 == list2:
        messagebox.showinfo("Same","Please Change Something")
    else:

        if p_r_ans_entry.get() not in list1 :
            messagebox.showerror("Warning","Please Select One Option")
            return False

        data['Question'][cnt] = p_question_entry.get()
        data['Option'][cnt][0] = p_option_1_entry.get()
        data['Option'][cnt][1] = p_option_2_entry.get()
        data['Option'][cnt][2] = p_option_3_entry.get()
        data['Option'][cnt][3] = p_option_4_entry.get()
        data['Right_Answer'][cnt] = p_r_ans_entry.get()

        with open(f"C:\Quiz_User\{user_info.get()}\{grade_Location.get()}\{file_loc.get()}.json", "w") as outfile:
            json.dump(data,outfile)
        messagebox.showinfo("Sucessfully Complete","Data Update Sucessfully")

def change():
    global dic,data,cnt
    cnt = 0

    preview_frame.pack_forget()
    Question_entrying_frame.pack(fill = 'both',expand = 'yes')

def Creating_Account_For_Teacher():

    if user_entry.get() == "":
        messagebox.showerror("Name Please","Enter Your Name Please")
        return False

    elif pass_entry.get() == "":
        messagebox.showerror("Password Please","Enter Your Password Please")
        return False

    elif con_pass_entry.get() == "":
        messagebox.showerror("Confirm Your Password","Please Confirm Your Password To Continue")
        return False

    elif pass_entry.get() != con_pass_entry.get():
        messagebox.showwarning("Wrong password","Both Password are not Matching")
        return False
    try:
        conn = mycon.connect(host = "localhost",
                            user = "root",
                            password = "",
                            database = "quiz")

    except:
        messagebox.showerror("Error","Not Able To Connect To The DataBase")
        return False



    try:
        cur = conn.cursor()
        cmd = "insert into login_info values (%s,%s)"
        val = (user_entry.get(),pass_entry.get())
        cur.execute(cmd,val)
        conn.commit()
        messagebox.showinfo("Done","Your Data Has Been Submited")
    except:
        messagebox.showerror("Error","Not Able To Insert Data")
        return False
    try:
        os.mkdir(os.path.join("C:/","Quiz_User"))
        os.mkdir(os.path.join("C:/","Quiz_User/Executed_Files"))

    except:
        pass
    os.mkdir(os.path.join("C:/Quiz_User/",user_entry.get()))
    for i in range(1,13):
        os.mkdir(os.path.join(f"C:/Quiz_User/{user_entry.get()}/Grade{i}"))
    try:
        for i in range(1,13):
            os.mkdir(os.path.join(f"C:/Quiz_User/Executed_Files/Grade{i}"))    
    except:
        pass

    user_info.set(user_entry.get())
    create_password_frame.pack_forget()
    Grade_Choose_Question.pack(fill = "both",expand = "yes")
    show_folder_count()

def login_for_teacher():
    if log_user_entry.get() == "":
        messagebox.showwarning("UserName","Please Enter Your User Name")
        return False
    elif log_pass_entry.get() == "":
        messagebox.showwarning("Password","Please Enter Your Password")
        return False
    else:
        try:
            conn = mycon.connect(host = "localhost",
                                user = "root",
                                password = "",
                                database = "quiz")

        except:
            messagebox.showerror("Error","Not Able To Connect To The DataBase")
            return False
        cur = conn.cursor()
        cur.execute("select * from login_info")
        data = cur.fetchall()

        for i in range(0,10):

            if log_user_entry.get() in data[i][0] and log_pass_entry.get() in data[i][1]:
                user_info.set(log_user_entry.get())
                login_frame.pack_forget()
                Grade_Choose_Question.pack(fill=BOTH,expand = YES)
                show_folder_count()
                # Choose_Question_Frame.pack(fill = 'both',expand = 'yes')
                # packing_button()
                break

            if i == len(data)-1:
                    messagebox.showerror("Wrong Info","Please Check The Username or Password")
                    break

def student_button_click():
    starting_frame.pack_forget()
    info_frame.pack(fill = "both",expand = "yes")


def teacher_click():
    try:
        conn = mycon.connect(host = "localhost",
                            user = "root",
                            password = "",
                            database = "quiz")

    except:
        messagebox.showerror("Error","Not Able To Connect To The DataBase")
        return False

    cur = conn.cursor()

    cur.execute("select * from login_info")

    data = cur.fetchall()

    if data == []:
        starting_frame.pack_forget()
        create_password_frame.pack(fill = "both",expand = "yes")
    else:
        starting_frame.pack_forget()
        login_frame.pack(fill = BOTH,expand = YES)

def submit():
    global data,count,r11,r22,r33,r44

    if name_Entry.get() == '' or Roll_no_Entry.get() == '' or class_combo.get() == '' or section_combo.get() == '' or gender.get() == '':
        messagebox.showerror('Fill Details',"Please Fill all the Details To Continue")
        return False
    packing_button_for_Student()
    info_frame.pack_forget()
    Student_Choose_Question.pack(fill=BOTH,expand=YES)

def validate_integer(action, value_if_allowed):
    if action == '1':  # Insertion or deletion happening
        if value_if_allowed.isdigit():
            return True
        else:
            return False
    return True


##########      Graphics User InterFace      ############


root = CTk()
root.attributes('-fullscreen',True)
root.title("Quiz Game")


########################       Tkinter Variable Of Setting Values         #######################



right_answer = StringVar()
que = StringVar()
var = StringVar()


r11 = StringVar()
r22 = StringVar()
r33 = StringVar()
r44 = StringVar()

file_loc = StringVar()
user_info = StringVar()
grade_Location = StringVar()

##################################################################################################
###########        Frames          ###########


starting_frame = CTkFrame(root)
starting_frame.pack(fill = "both",expand = "yes")

start_btn_frame = CTkFrame(starting_frame)


###########       Choose Frame      ############


Header = CTkLabel(starting_frame,text="Choose Your Section",font = ("Amatic SC",50))
Header.pack(pady = 20)

start_btn_frame.pack(fill = "both")

teacher_button = CTkButton(start_btn_frame,text="Teacher Section",
                                            height=100,width=300,corner_radius=50,command=teacher_click,
                                            font =("ariel",15,"bold"),text_color="black",fg_color="#575452",hover_color="#42413F")
teacher_button.pack(side = "left",padx = 160,pady = height/5)


Student_button = CTkButton(start_btn_frame,text="Student Section",
                                            height=100,width=300,corner_radius=50,
                                            font=("ariel",15,"bold"),text_color="black",fg_color="#575452",hover_color="#42413F",command=student_button_click)
Student_button.pack(pady = height/5)


info_para = CTkLabel(starting_frame , text = "Select One To Continue The Teacher Section is Protected with A Password",
                                    font=("Cambria",20,"bold"),text_color="white")
info_para.pack(pady = 30)





###################          Students Entrying There Info Frame        ###################


info_frame = CTkFrame(root)

info_header = CTkLabel(info_frame,text = "Fill Your Information here",font=("Julius Sans One",50,"bold"),bg_color="#403E3C",anchor = "s",height=10)
info_header.pack(fill = "both",side = "top")

box_frame = CTkFrame(info_frame)
box_frame.pack(padx = 300,pady=100,anchor = 'n',expand=YES)

label_frame = CTkFrame(box_frame)
label_frame.pack(side = "left",fill = "both")

entry_frame = CTkFrame(box_frame)
entry_frame.pack(side = "left",expand = "yes",fill = "both")

name_label = CTkLabel(label_frame,text="Name",font = fnt,anchor = "w")
name_label.pack(pady = 40,padx = 120,anchor = "w")

name_Entry = CTkEntry(entry_frame,placeholder_text="Enter Your Full Name",width = 250,height=40)
name_Entry.pack(anchor = "w",pady = 30)

class_label = CTkLabel(label_frame,text="Class",font=fnt,anchor = "w")
class_label.pack(pady = 30,padx = 120,anchor = "w")

class_var = StringVar()

class_combo= CTkComboBox(entry_frame,variable=class_var,values=("1","2","3","4","5","5","6","7","8","9","10","11","12"),
                                        text_color="black",width = 250,
                                        height = 45,state="readonly",
                                        font=("Bebas Neue",20,"bold"),
                                        dropdown_font=("Baskerville Old Face",10,"bold"))

class_combo.pack(anchor = "w",pady = 27)

roll_no_label = CTkLabel(label_frame,text="Roll no",font=fnt,anchor = "w")
roll_no_label.pack(pady = 30,padx = 120,anchor = "w")

validation = root.register(validate_integer)

Roll_no_Entry = CTkEntry(entry_frame,placeholder_text="Enter Your Roll No",width = 250,height=40,validate='key', validatecommand=(validation, '%d', '%P'))
Roll_no_Entry.pack(anchor = "w",pady = 27)

Section_label = CTkLabel(label_frame,text="Section",font=fnt,anchor = "w")
Section_label.pack(pady = 30,padx = 120,anchor = "w")

var_combo= StringVar()

section_combo= CTkComboBox(entry_frame,variable=var_combo,values=("A","B","C","D"),
                                        text_color="black",
                                        width = 250,height = 45,
                                        state="readonly",font=("Bebas Neue",20,"bold"),
                                        dropdown_font=("Baskerville Old Face",10,"bold"))

section_combo.pack(anchor = "w",pady = 27)


gender_label = CTkLabel(label_frame,text="Gender",font=fnt)
gender_label.pack(pady = 30,padx = 119,anchor = "w")

gender = StringVar()


CTkRadioButton(entry_frame,text="Male",variable=gender,value="Male").pack(side = "left")

CTkRadioButton(entry_frame,text="Female",variable=gender,value="Female").pack(pady = 30)


submit_button = CTkButton(info_frame,text="Submit Info",height = 50,width = 50,corner_radius=30,font=("Bell MT",15),command=submit)
submit_button.place(x=width/2,y=height/1.2)

###############################             UserName And Password Frame              #####################################

create_password_frame = CTkFrame(root,fg_color="#4C4A48")

head = CTkLabel(create_password_frame,text="Create Your UserName And Password",height=100,anchor = 's',fg_color="#363433",font=("Bodoni MT",30,"bold"))
head.pack(fill = "both")

header_lable = CTkLabel(create_password_frame,height=80,anchor = 's',text="Hello Sir !! Please Create a Username And Password To Continue. Next Time It's Will Be Required",font=("Consolas",15))
header_lable.pack(fill = 'both')

header_lable_1 = CTkLabel(create_password_frame,text="Write Your Username and Password Somewhere Becouse There is No Option For Forget  :-)",font=("Consolas",15))
header_lable_1.pack(fill = 'both')

frame = CTkFrame(create_password_frame,fg_color="#4C4A48")
frame.pack(fill = 'both',expand = 'yes')

user_label = CTkLabel(frame,text="UserName",anchor='w',font=('ariel',10,'bold'))
user_label.pack(anchor = 'w',pady = 20,padx = 530)

user_entry = CTkEntry(frame,height=30,width=300,placeholder_text="UserName")
user_entry.pack()

pass_label = CTkLabel(frame,text = "Password",
                                    anchor='w',font=('ariel',10,'bold'))
pass_label.pack(anchor = 'w',pady = 15,padx = 530)

pass_entry = CTkEntry(frame,height=30,width=300,placeholder_text="Password",show = "*")
pass_entry.pack()

con_pass_label = CTkLabel(frame,text = "Confirm Your Password",
                                        anchor='w',font=('ariel',10,'bold'))
con_pass_label.pack(anchor = 'w',pady = 15,padx = 530)

con_pass_entry = CTkEntry(frame,height=30,width=300,
                                        placeholder_text="Confirm Your Password",show = "*")
con_pass_entry.pack()

sub_button = CTkButton(frame,text = "Create User",command = Creating_Account_For_Teacher)
sub_button.pack(pady = 20)

back_button = CTkButton(frame,text = "Back",command=back_from_create_teacher_account)
back_button.pack(pady = 20)

######################           Selecting File Or Create File Of Questions       #####################

Choose_Question_Frame = CTkFrame(root)

img= Image.open("create_icon.png")
resized_image= img.resize((80,100))
header= ImageTk.PhotoImage(resized_image)

img= Image.open("backbutton.png")
resized_image= img.resize((60,100))
back_button= ImageTk.PhotoImage(resized_image)

button_frame = CTkFrame(Choose_Question_Frame,border_width=2,fg_color = "#686C70")
button_frame.pack(side = "left",anchor = 'n',fill = BOTH)

second_frame = CTkScrollableFrame(Choose_Question_Frame)
second_frame.pack(side = 'right',anchor = 'n',fill = BOTH,expand = YES)

create_file_label = CTkButton(button_frame,image = header,text = "",hover = False,fg_color="#686C70",command = create_file)
create_file_label.pack(pady = 30,padx = 40)

back_to_Grade_button = CTkButton(button_frame,image = back_button,text = "",hover = False,fg_color="#686C70",command = back_to_Grade)
back_to_Grade_button.pack(pady = 30,padx = 40,side = BOTTOM)

####################              Login Form For Teacher            #################

login_frame = CTkFrame(root)


header = CTkLabel(login_frame,text = "Please Login Here With Your Last User Name And Password",height=100,font=("Exo 2",20),anchor='s',fg_color="#3B3938")
header.pack(fill = "both")

container = CTkFrame(login_frame)
container.pack(pady = 40)

user_label = CTkLabel(container,text="UserName",anchor='s',font=('ariel',10,'bold'))
user_label.grid(row = 0, column = 0,pady = 30,padx = 20)

log_user_entry = CTkEntry(container,height=30,width=300,placeholder_text="UserName")
log_user_entry.grid(row = 0,column = 1,pady = 30,padx = 20)

pass_label = CTkLabel(container,text = "Password",
                                    anchor='w',font=('ariel',10,'bold'))
pass_label.grid(row = 1, column = 0,pady = 30,padx = 20)

log_pass_entry = CTkEntry(container,height=30,width=300,placeholder_text="Password",show = "*")
log_pass_entry.grid(row = 1 , column = 1,pady = 30,padx = 20)


login_me = CTkButton(container,text = "Submit",font=('ariel',10,'bold'),command=login_for_teacher)
login_me.grid(row = 2 , column = 1,pady = 30)


Create_new_account = CTkButton(container,text = "Create New User",font=('ariel',10,'bold'),command=create_new_acc)
Create_new_account.grid(row = 3,column = 1)

#####################            Entering Question And Answer Into Json File           ###################

Question_entrying_frame = CTkFrame(root)

heade = CTkLabel(Question_entrying_frame,text="Write The Questions And The Options And Don't Forget to Choose The Right Answer",font=('ariel',15,'bold'),height=80,anchor='s',fg_color="#4C4A48")
heade.pack(fill = 'both')

timer_button = CTkButton(Question_entrying_frame,text = "Set Timer",font=('ariel',10,'bold'),command=click_Timer)
timer_button.place(x=10,y=10)


frame_22 = CTkFrame(Question_entrying_frame)
frame_22.pack(fill='both')

see_question = CTkButton(frame_22,text="Preview The Questions",corner_radius=15,command = previous_question_frame_function)
see_question.pack(side='left')

execute_file_button = CTkButton(frame_22,text="Execute This File",corner_radius=15,command = execute_File)
execute_file_button.pack(anchor='e',pady=10)

question_label = CTkLabel(Question_entrying_frame,text="Question",anchor='s',font=('ariel',10,'bold'),height= 50)
question_label.pack(anchor = 'w',pady = 10,padx = 530)

question_entry = CTkEntry(Question_entrying_frame,height=30,width=300,placeholder_text="Question ")
question_entry.pack()

option_1_label = CTkLabel(Question_entrying_frame,text = "Option 1 ",
                                    anchor='w',font=('ariel',10,'bold'))
option_1_label.pack(anchor = 'w',pady = 5,padx = 530)

option_1_entry = CTkEntry(Question_entrying_frame,height=30,width=300,placeholder_text="Option 1 ")
option_1_entry.pack()

option_2_label = CTkLabel(Question_entrying_frame,text = "Option 2 ",
                                    anchor='w',font=('ariel',10,'bold'))
option_2_label.pack(anchor = 'w',pady = 5,padx = 530)

option_2_entry = CTkEntry(Question_entrying_frame,height=30,width=300,placeholder_text="Option 2 ")
option_2_entry.pack()

option_3_label = CTkLabel(Question_entrying_frame,text = "Option 3 ",
                                    anchor='w',font=('ariel',10,'bold'))
option_3_label.pack(anchor = 'w',pady = 5,padx = 530)

option_3_entry = CTkEntry(Question_entrying_frame,height=30,width=300,placeholder_text="Option 3 ")
option_3_entry.pack()

option_4_label = CTkLabel(Question_entrying_frame,text = "Option 4 ",
                                    anchor='w',font=('ariel',10,'bold'))
option_4_label.pack(anchor = 'w',pady = 5,padx = 530)

option_4_entry = CTkEntry(Question_entrying_frame,height=30,width=300,placeholder_text="Option 4 ")
option_4_entry.pack()

r_ans_label = CTkLabel(Question_entrying_frame,text = "Right Answer",
                                    anchor='w',font=('ariel',10,'bold'))
r_ans_label.pack(anchor = 'w',pady = 5,padx = 530)

r_ans = ttk.Combobox(Question_entrying_frame,textvariable=right_answer,width = 40,state="readonly",font=("Exo 2",10,"bold"),validate='all',foreground="black",background="black",)

r_ans.pack()

r_ans.bind("<Button-1>",click)

next_questions = CTkButton(Question_entrying_frame,text = "Next Question",font=('ariel',10,'bold'),command=sub_que)
next_questions.pack(anchor = 'w',pady = 15,padx = 530)
back_to_Choose_Question = CTkButton(Question_entrying_frame,text = "Back to File",font=('ariel',10,'bold'),command=back_to_Choose_Question)
back_to_Choose_Question.pack(anchor = 'w',padx = 530)

###############################         Frame Where Student Have to Choose The Question Paper For Test                #########################################

Student_Choose_Question = CTkFrame(root)

Left_frame = CTkFrame(Student_Choose_Question,border_width=2,fg_color = "#686C70")
Left_frame.pack(side = "left",anchor = 'n',fill = BOTH)

Right_Frame = CTkScrollableFrame(Student_Choose_Question)
Right_Frame.pack(side = 'right',anchor = 'n',fill = BOTH,expand = YES)

###############################         Frame Where Teacher Have to Choose The Grade For Test                #########################################

Grade_Choose_Question = CTkFrame(root)

Left_frame = CTkFrame(Grade_Choose_Question,border_width=2,fg_color = "#686C70")
Left_frame.pack(side = "left",anchor = 'n',fill = BOTH)

Right_Frame_of_Grade = CTkScrollableFrame(Grade_Choose_Question)
Right_Frame_of_Grade.pack(side = 'right',anchor = 'n',fill = BOTH,expand = YES)

#######################        See The Preview of the existience Question of the json file        #######################

preview_frame = CTkFrame(root,fg_color="#343638")
# preview_frame.pack(fill = 'both',expand = 'yes')

p_heade = CTkLabel(preview_frame,text="Check The Previous Question You Entered Before If You Want To Change Or Correct It So You Can It",font=('Exo 2',15),height=80,anchor='s',fg_color="#4C4A48")
p_heade.pack(fill = 'both')

b_frame = CTkFrame(preview_frame,fg_color="#343638")
b_frame.pack(fill = 'both')

l_question_in_pre_frame = CTkButton(b_frame,text="previous Question",command = previous_que,text_color_disabled='#343638',state=DISABLED)
l_question_in_pre_frame.pack(side = 'left',anchor = 'n',pady = 10,padx = 10)

n_question_in_pre_frame = CTkButton(b_frame,text="Next Question",command = next_que,text_color_disabled='#343638',state=DISABLED)
n_question_in_pre_frame.pack(side = 'right',anchor = 'n',pady = 10,padx = 10)

p_question_label = CTkLabel(preview_frame,text="Question",anchor='s',font=('ariel',10,'bold'),height= 50)
p_question_label.pack(anchor = 'w',pady = 5,padx = 470)

p_question_entry = CTkEntry(preview_frame,height=30,width=350)
p_question_entry.pack()

p_option_1_label = CTkLabel(preview_frame,text = "Option 1 ",
                                    anchor='w',font=('ariel',10,'bold'))
p_option_1_label.pack(anchor = 'w',pady = 5,padx = 500)

p_option_1_entry = CTkEntry(preview_frame,height=30,width=350)
p_option_1_entry.pack()

p_option_2_label = CTkLabel(preview_frame,text = "Option 2 ",
                                    anchor='w',font=('ariel',10,'bold'))
p_option_2_label.pack(anchor = 'w',pady = 5,padx = 500)

p_option_2_entry = CTkEntry(preview_frame,height=30,width=350)
p_option_2_entry.pack()

p_option_3_label = CTkLabel(preview_frame,text = "Option 3 ",
                                    anchor='w',font=('ariel',10,'bold'))
p_option_3_label.pack(anchor = 'w',pady = 5,padx = 500)

p_option_3_entry = CTkEntry(preview_frame,height=30,width=350)
p_option_3_entry.pack()

p_option_4_label = CTkLabel(preview_frame,text = "Option 4 ",
                                    anchor='w',font=('ariel',10,'bold'))
p_option_4_label.pack(anchor = 'w',pady = 5,padx = 500)

p_option_4_entry = CTkEntry(preview_frame,height=30,width=350)
p_option_4_entry.pack()

p_r_ans_entry = ttk.Combobox(preview_frame,height=30,width = 40,font=("Exo 2",10,"bold"),validate='all',foreground="black",background="black")

p_r_ans_entry.pack(pady = 10)

p_r_ans_entry.bind("<Button-1>",click_in_preview_frame)

button_ok = CTkButton(preview_frame,text = "Make Change",command = make_change)
button_ok.pack(pady = 5)

con_change = CTkButton(preview_frame,text = "Back To Question",command = change)
con_change.pack(pady = 5)

################################             Real Quiz Starting  From Here { Let's Do This :) }  ###############################

real_quiz_frame = CTkFrame(root,fg_color="#999591")

quiz_label = CTkLabel(real_quiz_frame,text = "Select The Right Answer And Click Next Question For Next Question",height=100,anchor='s',fg_color="#4C4A48",font=("Bodoni MT",20),bg_color="#999591"
                        )
quiz_label.pack(fill = 'both')

Timer_Label = CTkLabel(real_quiz_frame,text = "No Time Limit",anchor='s',fg_color="#4C4A48",font=("Bodoni MT",20),bg_color="#999591"
                        )
Timer_Label.place(x=0,y=0)


ques = CTkLabel(real_quiz_frame,textvariable = var,height = 50,anchor = 's',font = ("B612 Mono",25,'bold'),fg_color="#999591")
ques.pack(pady = 40)

############                         Selection variable                          ##################

opt = tk.StringVar(value="Hello")

radio_frame = CTkFrame(real_quiz_frame,fg_color="#999591")
radio_frame.pack()

r1 = Radiobutton(radio_frame,font=font_for_radiobutton,textvariable = r11,variable=opt,value=r11,background='#999591',anchor="w")
r1.pack(pady=5,fill=BOTH)

r2 = Radiobutton(radio_frame,font=font_for_radiobutton,textvariable = r22,variable=opt,value=r22,background='#999591',anchor="w")
r2.pack(pady=5,fill=BOTH)

r3 = Radiobutton(radio_frame,font=font_for_radiobutton,textvariable = r33,variable=opt,value=r33,background='#999591',anchor="w")
r3.pack(pady=5,fill=BOTH)

r4 = Radiobutton(radio_frame,font=font_for_radiobutton,textvariable = r44,variable=opt,value=r44,background='#999591',anchor="w")
r4.pack(pady=5,fill=BOTH)

next_que_button = CTkButton(real_quiz_frame,text = "Next Question",command=next)
next_que_button.pack(pady=10)

 #############################                       Result Frame                     ###############################

result_frame = CTkFrame(root)

Score_label = CTkLabel(result_frame,text="",font=("ariel",20,"bold"))
Score_label.pack(pady=height/4)

root.mainloop()
