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
        birthday = datetimeNew.date()
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
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        query = f"SELECT * FROM `signup` where email='{email}' and password ='{password}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        if len(resut) > 0:
            resut[0]['dob'] = str(resut[0]['dob'])
            request.session['user'] = resut[0]
            return redirect('home')
        else:
            messages.warning(request, 'invalid Email or Password !!!')
            return redirect('userlogin')

    return render(request, 'client/userlogin.html')


def userlogout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('home')


def home(request):
    return render(request, 'client/index.html')


def createPost(request):
    query = "SELECT * FROM `area`"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    resut = cr.fetchall()

    if request.method == 'POST':
        name = request.POST['name']
        fname = request.POST['fname']
        address = request.POST['address']
        mobile = request.POST['mobile']
        email = request.POST['email']
        identificationMarks = request.POST['identificationMarks']
        photo = request.FILES['photo']
        area = request.POST['area']
        status = 'Missing'
        user = request.session['user']['email']

        fs = FileSystemStorage()
        filename = fs.save('missingPerson/' + photo.name, photo)
        query = f"INSERT INTO `profile`(`name`, `fatherName`, `address`, `identificationMarks`, `mobile`, `email`, `photo`, `status`, `area`, `SignUp`) VALUES ('{name}','{fname}','{address}','{identificationMarks}','{mobile}','{email}','{filename}','{status}','{area}','{user}')"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        conn.commit()
        return redirect('createPost')
    return render(request, 'client/createPost.html', {'data': resut})

def userProfile(request):
    query ="SELECT * FROM `profile`  where SignUp='{}'".format(request.session['user']['email'])
    print(query)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    results = cr.fetchall()
    return render(request,'client/profile.html',{'results':results})

def deletePost(request):
    query = "DELETE FROM `profile` WHERE id='{}'".format(request.GET['id'])
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    return redirect('userProfile')
