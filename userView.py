import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymysql import *
from django.contrib import messages

from django.core.files.storage import FileSystemStorage


def makeConnections():
    return connect(host='127.0.0.1', user='root', password='', database='missingPerson',
                   cursorclass=cursors.DictCursor)


def signupPage(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        birthday = request.POST['birthday']
        datetimeNew = datetime.datetime.strptime(birthday, '%d/%m/%Y')
        birthday =datetimeNew.date()
        gender = request.POST['gender']
        password = request.POST['password']
        profession = request.POST['profession']
        photo = request.FILES['image']
        query = "SELECT * FROM `signup` where email='{}'".format(email)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        if len(resut) > 0:
            messages.warning(request, 'allready exists!!')
            return redirect('signup-Page')
        else:
            fs = FileSystemStorage()
            filename = fs.save('signUp/' + photo.name, photo)
            query = f"INSERT INTO `signup`(`name`, `email`, `password`, `dob`, `gender`, `coverphoto`, `profession`) VALUES ('{name}','{email}','{password}','{birthday}','{gender}','{filename}','{profession}')"
            print(query)
            cr.execute(query)
            conn.commit()
            messages.success(request, 'SignUp success')
            return redirect('signup-Page')
    return render(request, 'client/signup.html')

def userlogin(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        query = f"SELECT * FROM `signup` where email='{email}' and password ='{password}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        if len(resut)>0:
            resut[0]['dob'] = str(resut[0]['dob'])
            request.session['user'] = resut[0]
            return redirect('home')
        else:
            messages.warning(request, 'invalid Email or Password !!!')
            return redirect('home')

    return render(request,'client/userlogin.html')

def userlogout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('home')

def home(request):
    return render(request,'client/index.html')

