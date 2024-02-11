import os
from pathlib import Path
import re
from tkinter import EXCEPTION
from loginsys import loginu
from atanish import extrat_stu,take_attendance,editatt,nosheets,copysheets
from datetime import timedelta
from flask import Flask, render_template, redirect, session, url_for, request
import bro


app = Flask(__name__,template_folder='template',static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=2)


@app.route('/')
def homepage():
    if 'username' in session:
        print(session['username'])
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        print(session['username'])
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        user_id = request.form['username']
        password=request.form['password']
        value,name=loginu(user_id,password)
        if value==True:
            session['username']=name
            session.permanent=True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        result=session['username']
        return render_template("dashboard.html",result=result)
    else: 
        return render_template("login.html")

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        return  redirect(url_for('login'))
    
    


@app.route('/select_session')
def select_session():
    if 'username' in session:
        files=os.listdir(f'{os.getcwd()}/Attendence_data')
        url='/select_sub'
        return render_template("selectsess.html",files=files,url=url)
    else:
        return  redirect(url_for('login'))


@app.route('/select_sub',methods=['GET', 'POST'])
def select_sub():
    if 'username' in session:
       if request.method == 'POST':
            sess=request.form.get('sess')
            course=request.form.get('Course')
            if sess=='2023':  
                    sub=os.listdir(f'{Path.cwd()}/Attendence_data/{sess}/{course}')
                    subject=[]
                    section=nosheets(f'{Path.cwd()}/Attendence_data/{sess}/{course}/{sub[0]}')
                    session['course']=f'{Path.cwd()}/Attendence_data/{sess}/{course}'
                    for i in sub:
                        file_name_without_extension,_=os.path.splitext(i)
                        subject.append(file_name_without_extension)
                    
                    print(subject,section)
                    url='/take_attendence'
                    return render_template("selectsub.html",subject=subject,section=section,url=url)
       else:
            sess='2023'
            sub=os.listdir(f'{os.getcwd()}/Attendence_data/{sess}/{course}')
            print(sub)
            return redirect(url_for('select_session'))

    else:
        return  redirect(url_for('login'))


# @app.route('/select_sub')
# def select_sub():
#     if 'username' in session:
#         result=session['username']
#         print(result)
#         return render_template("selectsub.html",result=result)
#     else:
#         return redirect(url_for('login'))


@app.route('/take_attendence',methods=['GET', 'POST'])
def take_attendence():
    if 'username' in session:
        if request.method == 'POST':
            section = request.form.get('section')
            subject= request.form.get('Subject')
            student=extrat_stu(f'{session['course']}/{subject}.xlsx',section)
            length=len(student)
            list=[student,length]
            session['subject']=f'{session['course']}/{subject}.xlsx'
            session['section']=section
            return render_template("take_att.html",list=list)

        else:
            result=session['username']
            return redirect(url_for('select_sub'))
    else:
        return redirect(url_for('login'))


# @app.route('/take_attendence',methods=['GET', 'POST'])
# def take_attendence():
#     if 'username' in session:
#         if request.method == 'POST':
#             section = request.form.get('section')
#             subject= request.form.get('Subject')
#             session['subject']=str(section+subject)
#             if 'subject' in session: 
#                 print(session['subject'])
#                 student=extrat_stu(f"{session['subject']}")
#                 length=len(student)
#                 list=[student,length]
#                 return render_template("take_att.html",list=list)
#             else:
#                 result=session['username']
#                 return redirect(url_for('select_sub'))
#         else:
#             result=session['username']
#             return redirect(url_for('select_sub'))
#     else:
#         return redirect(url_for('login'))
    


@app.route('/result',methods=['GET', 'POST'])
def result():
    if 'username' in session:
         
         if request.method == 'POST':
            pr=[]
            AB=[]
            UN=[]
            print(session['subject'])
            student=extrat_stu(session['subject'],session['section'])
            for i in student:
                if request.form.get(f'{i}')=='P':
                    pr.append(i)
                elif request.form.get(f'{i}')=='A':
                    AB.append(i)
                else:
                    UN.append(i)
            if 'subject' in session:
                take_attendance(session['subject'],session['section'],pr,AB)
        # Assuming your checkbox has the id "cb5"
                return f'{pr} ab {AB} unmarked{UN}'
    else:
        return redirect(url_for('login'))
    
@app.route('/editattsess')
def edit():
    if 'username' in session:
        files=os.listdir(f'{os.getcwd()}/Attendence_data')
        url='/editattend'
        return render_template("selectsess.html",files=files,url=url)
    else:
        return redirect(url_for('login'))


@app.route('/editattend',methods=['GET', 'POST'])
def editend():
    if 'username' in session:
        if request.method == 'POST':
            sess=request.form.get('sess')
            course=request.form.get('Course')
            sub=os.listdir(f'{Path.cwd()}/Attendence_data/{sess}/{course}')
            section=nosheets(f'{Path.cwd()}/Attendence_data/{sess}/{course}/{sub[0]}')
            subject=[]
            session['course']=f'{Path.cwd()}/Attendence_data/{sess}/{course}'
            for i in sub:
                file_name_without_extension,_=os.path.splitext(i)
                subject.append(file_name_without_extension)
            return render_template('editatt.html',subject=subject,section=section)
        else:
            redirect(url_for('editattsess'))
    else:
        return redirect(url_for('login'))

@app.route('/editattends',methods=['GET', 'POST'])
def editfin():
    if 'username' in session:
        if request.method == 'POST':
            course=request.form.get('Course')
            section = request.form.get('section')
            subject= request.form.get('Subject')
            Date=request.form.get('Date')
            roll=request.form.get('roll')
            value=request.form.get('att')
            file=f'{session['course']}/{subject}.xlsx'
            student=extrat_stu(file,section)
            try:
                studentname=student[int(roll)-1]
            except IndexError:
                return "roll number not found"
            teacher=session['username']
            return editatt(file,section,studentname,Date,value,teacher)
        elif request.method == 'GET':
            return render_template("editatt.html")
    else:
        return redirect(url_for('login'))
    
@app.route('/COPY')
def copy():
    if 'username' in session:
        files=os.listdir(f'{os.getcwd()}/Attendence_data')
        url='/selectsubj'
        return render_template("selectsess.html",files=files,url=url)
    else:
        return  redirect(url_for('login'))

    
@app.route('/selectsubj',methods=['GET', 'POST'])
def copysub():
    if 'username' in session:
       if request.method == 'POST':
            sess=request.form.get('sess')
            course=request.form.get('Course')
            if sess=='2023':  
                    sub=os.listdir(f'{Path.cwd()}/Attendence_data/{sess}/{course}')
                    subject=[]
                    section=nosheets(f'{Path.cwd()}/Attendence_data/{sess}/{course}/{sub[0]}')
                    session['course']=f'{Path.cwd()}/Attendence_data/{sess}/{course}'
                    for i in sub:
                        file_name_without_extension,_=os.path.splitext(i)
                        subject.append(file_name_without_extension)
                    
                    print(subject,section)
                    url='/copyfile'
                    return render_template("selectsub.html",subject=subject,section=section,url=url)
            else:
                return redirect(url_for('COPY')) 
    else:
        return redirect(url_for('login')) 
                                              
                    
@app.route('/copyfile',methods=['GET', 'POST'])
def copyfile():
    if 'username' in session:
        if request.method == 'POST':
            section = request.form.get('section')
            subject= request.form.get('Subject')
            path=f'{session['course']}/{subject}.xlsx'
            saved=f'{Path.cwd()}/static/copy.xlsx'
            copysheets(path,section,section,saved)
            return render_template("copy.html")
        else:
            return redirect(url_for('COPY')) 
        
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
