import PySimpleGUI as sg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import random
import string
from datetime import datetime
import re
import os


'''def save_data():#receive sensor data from arduino server and save in file
    url = 'http://gh1.local'
    r = requests.get(url)
    data = r.text
    wd = data[177:182]
    xd = data[261:266]
    file = open("stats.txt", "a+")
    dtime = datetime.now()
    dtime = str(dtime)
    if wd.__contains__('n' or '>'):#formating recieved string from sensor
        wd = ''
    elif xd.__contains__('n' or '>'):
        xd = ''
    else:
        file.write(dtime + "   " + "Temprature:  " + wd + "  Humidity  " + xd)
        file.write("\n")
    file.close()
'''
def display_data():#display data to UI in real time


        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        url = 'http://testingplace.tech/page4display.php'
        r1 = requests.get(url, headers=headers)
        r1 = r1.text

        clean = re.compile('<.*?>')
        r1 = re.sub(clean, '', r1)
        r1 = r1.strip()


        wd = r1[0:2]
        xd = r1[2:4]
        hd =  r1[4:6]

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        url = 'http://testingplace.tech/controlvalues.php'
        r1 = requests.get(url, headers=headers)
        r1 = r1.text

        clean = re.compile('<.*?>')
        r1 = re.sub(clean, '', r1)
        r1 = r1.strip()

        temp = r1[0:2]
        hum = r1[2:4]
        mo = r1[4:6]


        window2['maxt'].update(wd)
        window2['maxh'].update(xd)
        window2['maxs'].update(hd)

        window2['nowt'].update(wd)
        window2['nowh'].update(xd)
        window2['nows'].update(hd)

        window2['mint'].update(wd)
        window2['minh'].update(xd)
        window2['mins'].update(hd)
        if(float(wd)>=float(values['maxt'])):
            window2["maxt"].update(wd)
        else:
            window2["mint"].update(wd)
        if (float(xd) >= float(values['maxh'])):
            window2["maxh"].update(xd)
        else:
            window2["minh"].update(xd)
        if (float(hd) >= float(values['maxs'])):
            window2["maxs"].update(hd)
        else:
            window2["mins"].update(hd)
        window2["currentcontrol1"].update(temp)
        window2["currentcontrol2"].update(hum)
        window2["currentcontrol3"].update(mo)
        if(float(wd)>=float(temp)):
            window2["currentstate1"].update("ON")
            #window2["maxt"].update(wd)
        else:
            window2["currentstate1"].update("OFF")
           # window2["mint"].update(wd)
        if (float(xd) >= float(hum)):
            window2["currentstate2"].update("ON")
          #  window2["maxh"].update(xd)
        else:
            window2["currentstate2"].update("OFF")
           # window2["minh"].update(xd)
        if (float(hd) >= float(mo)):
            window2["currentstate3"].update("ON")
          #  window2["maxh"].update(hd)
        else:
            window2["currentstate3"].update("OFF")
           # window2["mins"].update(hd)

        '''valuet=float(values['maxt'])
        #valueh=float(values['nowh'])
        #valuel=float(values['nows'])'''

'''      if valuet <= float(wd):
                window2['nowt'].update(text_color='red')
                window2['nowt'].update(wd)
        else:

                window2['nowt'].update(wd)
        if valueh <= float(wd):
                window2['nowh'].update(text_color='red')
                window2['nowh'].update(xd)

        else:
            window2['nowh'].update(xd)

            if valuel<= float(wd):
                window2['nows'].update(text_color='red')
                window2['nows'].update(hd)
            else:

                window2['nows'].update(hd)
    except:
        pass
'''




'''def automation():#automatic machine control

 if values['notmanual'] == True:
    xx=values['maxt']
    xx=float(xx)
    xy=values['nowt']
    xy=float(xy)

    if xy>xx:
        onn = 'http://192.168.43.202/LED=ON '
        nn = requests.get(onn)
 else:
     pass'''
def send_mail():#send email
    fromaddr = "scriptkiddie4now@gmail.com"
    toaddr = "atif_razzaq@outlook.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "TEST"

    body = "Result stats"
    msg.attach(MIMEText(body, 'plain'))
    #make request and scrap it open a file save in file
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/displaydata.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
    clean = re.compile('<.*?>')
    r1 = re.sub(clean, '', r1)
    r1 = r1.strip('\n')
    r1 = r1.split(',')
    file = open('results.txt', 'a+')
    for i in r1:
        file.write(i)
        file.write('\n')
    file.close()
    filename= "results.txt"
    attachment = open("results.txt", "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "whysoserious?")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    sg.popup("Email sent" )

def start_m1():#machine control manual
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/on1.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def start_m2():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/on2.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def stop_m1():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/off1.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def stop_m2():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/off2.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def start_m3():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/on3.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def stop_m3():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/off3.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text
def setlimit1():
    data=values["limitvalue1"]
    data=str(data)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/set1.php?&limit1='+data

    r1 = requests.get(url, headers=headers)
    r1 = r1.text

def setlimit2():
    data = values["limitvalue2"]
    data = str(data)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/set2.php?&limit2='+data

    r1 = requests.get(url, headers=headers)
    r1 = r1.text


def setlimit3():
    data = values["limitvalue3"]
    data = str(data)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/set3.php?&limit3='+data

    r1 = requests.get(url, headers=headers)
    r1 = r1.text


def login():#log in
    try:
        #x=open('pass.txt','r')
        #x1=x.read()

        if values['id1']== 'admin' and values["pass"]== 'admin':
            return  True
        else:

            return  False
    except:
        sg.Popup("Something Went Wrong")

def sendandsave():
    try:
        def randomString(stringLength=10):

            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))


        a = randomString(24)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("scriptkiddie4now@gmail.com", "whysoserious?")
        message = "You recovery code is "+ a
        s.sendmail("scriptkiddie4now@gmail.com", "atif_razzaq@outlook.com", message)
        s.quit()

        sg.popup("Email sent")
        file = open("recovery.txt", "a+")
        file.truncate(0)
        file.write(a)
        file.close()
        return True
    except:
        sg.popup("An unexpected Error Happened")
        return False
def reset():#password reset code
    try:

        file=open("recovery.txt","r+")
        x=file.read()
        if values['recover']== x:
            return True

        else:
            sg.popup("Try again")
    except:
        sg.popup("Task Failed")


def change():#change password
    if values['p1'] == values['p2']:
        x=values['p1']
        file1 = open("pass.txt", "r+")
        file1.truncate(0)
        file1.write(x)
        file1.close()
        sg.popup("passwor changed")
    else:
        window4.close()

def draw():

    import matplotlib
    matplotlib.use("TKAgg")


    import matplotlib.pyplot as plt

    timestamp = []
    x = []
    y = []
    z = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'http://testingplace.tech/allgraph.php'
    r1 = requests.get(url, headers=headers)
    r1 = r1.text

    clean = re.compile('<.*?>')
    r1 = re.sub(clean, '', r1)
    r1 = r1.strip()
    r1 = r1.split(',')


    for i in r1:
        tm = i[0:19]
        temp = i[19:21]
        hum = i[21:23]
        mo = i[23:25]
        timestamp.append(tm)
        x.append(temp)
        y.append(hum)
        z.append(mo)



    f1 = plt.figure(figsize=(50, 5))


    # subplot(2 Rows, 3 Columns, First subplot,)
    ax1 = f1.add_subplot(3, 1,1)
    ax1.plot(timestamp, x, label='Curve 1', color="r", marker='^', markevery=2)

    ax2 = f1.add_subplot(3, 1, 2)
    ax2.plot(timestamp, y, label='Curve 2', color="g", marker='*', markevery=2)

    # subplot(2 Rows, 3 Columns, Third subplot)
    ax3 = f1.add_subplot(3, 1, 3)
    ax3.plot(timestamp, z, label='Curve 3', color="b", marker='D', markevery=2)


    plt.figure(1)

    ax1.legend(loc='upper left', fontsize='medium')
    ax1.set_title('Tempertaure Graph ')
    ax1.set_xlabel('DateTime')
    ax1.set_ylabel('Temprature')
    ax1.grid(True)
    ax1.set_xlim([0, 5])
    ax1.set_ylim([0, 5])


    ax2.legend(loc='center left', fontsize='large')
    ax2.set_title('Humidity Graph')
    ax2.set_xlabel('DateTime')
    ax2.set_ylabel('Humidity')
    ax2.grid(True)
    ax2.set_xlim([0, 5])
    ax2.set_ylim([0, 5])


    ax3.legend(loc='lower left', fontsize='large')
    ax3.set_title('Soil Moisture Graph ')
    ax3.set_xlabel('DateTime')
    ax3.set_ylabel('Soil Moisture')
    ax3.grid(True)
    ax3.set_xlim([0, 5])
    ax3.set_ylim([0, 5])
    plt.tight_layout()

    plt.show()
def sendemail():
    d1=values["-IN-"]
    d2=values["-IN1-"]
    if (d1 == '' and d2!=""):
        sg.popup("Please select start date first or no date")
    elif (d1=="" and d2==""):
        dtime = datetime.now()
        dtime = str(dtime)
        dtime=dtime[0:11]
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        url = 'http://testingplace.tech/email1.php?&firstdate='+dtime
        r1 = requests.get(url, headers=headers)
        r1 = r1.text

        clean = re.compile('<.*?>')
        r1 = re.sub(clean, '', r1)
        r1 = r1.strip()
        r1 = r1.split(',')
        print(r1)

        file = open('newresults.txt', 'a+')
        for i in r1:
            file.write(i)
            file.write('\n')

        file.close()
        fromaddr = "scriptkiddie4now@gmail.com"
        toaddr = "atif_razzaq@outlook.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "TEST"

        body = "Result stats"
        msg.attach(MIMEText(body, 'plain'))
        filename = "newresults.txt"
        attachment = open("newresults.txt", "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "whysoserious?")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        os.remove("newresults.txt")
        sg.popup("Email sent")
    elif(d1!="" and d2==""):

        dtime = d1[0:11]
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        url = 'http://testingplace.tech/email1.php?&firstdate='+dtime
        r1 = requests.get(url, headers=headers)
        r1 = r1.text

        clean = re.compile('<.*?>')
        r1 = re.sub(clean, '', r1)
        r1 = r1.strip()
        r1 = r1.split(',')
        print(r1)

        file = open('newresults.txt', 'a+')
        for i in r1:
            file.write(i)
            file.write('\n')

        file.close()
        fromaddr = "scriptkiddie4now@gmail.com"
        toaddr = "atif_razzaq@outlook.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "TEST"

        body = "Result stats"
        msg.attach(MIMEText(body, 'plain'))
        filename = "newresults.txt"
        attachment = open("newresults.txt", "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "whysoserious?")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        os.remove("newresults.txt")
        sg.popup("Email sent")

    else:
        d1=d1[0:11]
        d2=d2[0:11]
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        url = 'http://testingplace.tech/email2.php?&firstdate=' + d1+'&seconddate='+d2
        r1 = requests.get(url, headers=headers)
        r1 = r1.text

        clean = re.compile('<.*?>')
        r1 = re.sub(clean, '', r1)
        r1 = r1.strip()
        r1 = r1.split(',')
        print(r1)

        file = open('newresults.txt', 'a+')
        for i in r1:
            file.write(i)
            file.write('\n')

        fromaddr = "scriptkiddie4now@gmail.com"
        toaddr = "atif_razzaq@outlook.com"

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "TEST"

        body = "Result stats"
        msg.attach(MIMEText(body, 'plain'))
        filename = "newresults.txt"
        attachment = open("newresults.txt", "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "whysoserious?")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        os.remove("newresults.txt")
        sg.popup("Email sent")
sg.theme('DarkAmber')#UI CODE HERE

layout = [  [] ]


window1 = sg.Window('Window Title', layout)

while True:
    event, values = window1.read(1000,'log in')
    if event in (None, 'Cancel'):	# if user closes window or clicks cancel
        break
    elif event == 'log in':
        window1.close()
        layout = [[sg.Frame(layout=[
            [sg.Text("User Name", justification="center", font='Bold'), sg.InputText(size=(20, 0), key='id1')],
            [sg.Text("Password   ", font='Bold'), sg.InputText(password_char='*', size=(20, 0), key='pass')],
            [sg.Button("Login", key='Login', enable_events=True, size=(30, 0))],
            [sg.Button("Forget Password", key='reset', enable_events=True, size=(30, 0))]], title="Login", font="bold",
            title_color='gold', element_justification='center', pad=(0, 90))

        ]]

        window = sg.Window("Welcome", layout, size=(400, 400), element_justification='center', resizable=True)

        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            elif event == 'Login':
                chek=login()
                if chek==True:
                    window.close()

                    layout = [

                        [sg.Frame(layout=[
                            [sg.Text("Maximum Value"),
                             sg.InputText(size=(30, 0), key='maxt', enable_events="True",default_text='00.00'),
                             ],
                            [sg.Text("Current Value    "), sg.InputText(size=(30, 0),key="nowt", default_text='00.00',enable_events=True)],
                            [sg.Text("Minimum Value "), sg.InputText(size=(30, 0), key='mint', enable_events="True",default_text='00.00',)]],
                            size=(30, 0), pad=(0, 30), title='Temprature Statistics', title_color='red',
                            relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags', font='bold'),sg.Frame(layout=[[
                            sg.Text("Current state is"), sg.Text("N/A", key='currentstate1', font='bold'),sg.Text(" and Current conrol value is"), sg.Text("00",key='currentcontrol1', font='bold')
                        ],[sg.Text("Control Value", pad=(1, 3)),sg.InputText(size=(15,0),pad=(0,3),key="limitvalue1",enable_events=True),sg.Button("Set Limit",enable_events=True,key="limit1",size=(5,0))],
                            [sg.Button("ON", enable_events=True,pad=(50,0),key="ON1"), sg.Button("OFF", enable_events=True,key="OFF1")]], title="Machine 1",
                            font="bold", pad=(15, 0),)

                        ],
                        [sg.Frame(layout=[
                            [sg.Text("Maximum Value"), sg.InputText(size=(30, 0), key='maxh', enable_events="True",default_text='00.00')],
                            [sg.Text("Current Value   "), sg.InputText(size=(30, 0), key='nowh', default_text='00.00')],
                            [sg.Text("Minimum Value "), sg.InputText(size=(30, 0), key='minh', enable_events="True",default_text='00.00')]],pad=((5, 15)), title='Humidity Statistics', title_color='Blue', relief=sg.RELIEF_SUNKEN,
                            tooltip='Use these to set flags', font='bold'),sg.Frame(layout=[[
                            sg.Text("Current state is", pad=(0, 2)), sg.Text("N/A", key='currentstate2', font='bold'),sg.Text("and Current conrol value is "), sg.Text("00",key='currentcontrol2', font='bold')
                        ],[sg.Text("Control Value", pad=(1, 3)),sg.InputText(size=(15,0),pad=(0,3),key="limitvalue2",enable_events=True),sg.Button("Set Limit",enable_events=True,key="limit2",size=(5,0))],
                            [sg.Button("ON", enable_events=True,pad=(50,0),key="ON2"), sg.Button("OFF", enable_events=True,key="OFF2")]], title="Machine 2",
                            font="bold", pad=(15, 0),)
                        ],
                        [sg.Frame(layout=[
                            [sg.Text("Maximum Value"),
                             sg.InputText( key='maxs',size=(30,10), enable_events="True",default_text='00.00'),
                             ],
                            [sg.Text("Current Value    "), sg.InputText(size=(30, 0), key="nows", default_text='00.00')],
                            [sg.Text("Minimum Value "), sg.InputText(size=(30, 10), key='mins', enable_events="True",default_text='00.00')]],
                            size=(30, 0), pad=(5, 15), title='Moisture Statistics', title_color='red',
                            relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags', font='bold'),sg.Frame(layout=[[
                            sg.Text("Current state is"), sg.Text("N/A",key='currentstate3', font='bold'),sg.Text("and Current conrol value is"), sg.Text("00",key='currentcontrol3', font='bold')
                        ],[sg.Text("Control Value", pad=(1, 3)),sg.InputText(size=(15,0),pad=(0,3),key="limitvalue3",enable_events=True),sg.Button("Set Limit",enable_events=True,key="limit3",size=(5,0))],
                            [sg.Button("ON3", enable_events=True,pad=(50,0),key="ON1"), sg.Button("OFF", enable_events=True,key="OFF3")]], title="Machine 3",
                            font="bold", pad=(15, 0))
                        ],
                        [sg.Button("Reporting Panel", pad=(300,20), enable_events=True,key='Send Email')]

                    ]

                    window2 = sg.Window('GH Environament Control', layout,)

                    while True:

                        event, values = window2.read(10000, 'automate')

                        if event in (None, 'Cancel'):
                            break
                        elif event == 'Send Email':
                            sg.theme('Dark Amber')
                            layout = [
                                [sg.Frame(layout=[[sg.Text('Select a date or dates to receive emails', key='-TXT-')],
                                                  [sg.Input(key='-IN-', size=(20, 1)),
                                                   sg.CalendarButton('Start Date', close_when_date_chosen=True,
                                                                     target='-IN-')],
                                                  [sg.Input(key='-IN1-', size=(20, 1)),
                                                   sg.CalendarButton('End Date  ', close_when_date_chosen=True,
                                                                     target='-IN1-')],
                                                  [sg.Button("Send Email", key='Email', enable_events=True,
                                                             pad=(60, 0))]], size=(30, 0), title="Email", font="bold",
                                          title_color='seagreen')],
                                [sg.Frame(layout=[[sg.Text('Select a date or dates to View Graphs', key='-TXT1-')],
                                                  [sg.Input(key='-IN2-', size=(20, 1)),
                                                   sg.CalendarButton('Start Date', close_when_date_chosen=True,
                                                                     target='-IN2-')],
                                                  [sg.Input(key='-IN3-', size=(20, 1)),
                                                   sg.CalendarButton('End Date  ', close_when_date_chosen=True,
                                                                     target='-IN3-')],
                                                  [sg.Button("View Graph", key='Graph', enable_events=True,
                                                             pad=(60, 0))]], size=(30, 0),
                                          title="GRAPH", font="bold", title_color='gold')]
                                ]

                            windowx = sg.Window('Reporting Panel', layout, size=(350, 350))

                            while True:
                                event, values = windowx.read()
                                if event in (None, 'Cancel'):
                                    break
                                elif event == "Email":
                                   sendemail()
                                elif event == "Graph":
                                    draw()



                        elif event == 'ON1':
                            start_m1()

                        elif event == 'OFF1':
                            stop_m1()
                        elif event == 'ON2':
                            start_m2()
                        elif event == 'OFF2':
                            stop_m2()
                        elif event == 'ON3':
                            start_m3()
                        elif event == 'OFF3':
                            stop_m3()
                        elif event == 'limit1':
                            setlimit1()
                        elif event == 'limit2':
                            setlimit2()
                        elif event == 'limit3':
                            setlimit3()
                        elif event == 'automate':
                            display_data()



                    window2.close()
                else:
                    window['id1'].update('')
                    window['pass'].update('')
                    sg.popup("Log in failed,User Name or Password not correct")


            elif event == 'reset':
                checkk=sendandsave()
                if checkk==True:


                    layout = [
                        [sg.Text('Please enter the code sent to your email', font='bold', pad=(0, 20,20))],
                        [sg.Text("Security code ", justification="center", font='Bold'), sg.InputText(size=(20, 0), key='recover')],

                        [sg.Button("Reset", key='reset', enable_events=True)],


                    ]

                    window3 = sg.Window("Welcome", layout, size=(800, 400), element_justification='center', resizable=True)

                    while True:
                        event, values = window3.read()
                        if event in (None, 'Cancel'):
                            break
                        elif event== 'reset':

                            check=reset()
                            window3.close()
                            if check == True:

                                layout = [
                                    [sg.Text('Please enter change your password', font='bold', pad=(0,20))],
                                    [sg.Text("New Password ", justification="center", font='Bold'),
                                     sg.InputText(size=(20, 0), key='p1')],
                                    [sg.Text("Repeat Password ", justification="center", font='Bold'),
                                     sg.InputText(size=(20, 0), key='p2')],

                                    [sg.Button("Change password", key='change', enable_events=True)],

                                ]

                                window4 = sg.Window("Welcome", layout, size=(800, 400), element_justification='center',
                                                    resizable=True)

                                while True:
                                    event, values = window4.read()
                                    if event in (None, 'Cancel'):
                                        break
                                    elif event == 'change':
                                        change()
                                        window4.close()

                        else:
                            window3['recover'].update('')
                else:
                    pass

