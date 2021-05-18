import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymysql import *
from django.contrib import messages




def makeConnections():
    return connect(host='127.0.0.1', user='root', password='', database='missingPerson',
                   cursorclass=cursors.DictCursor)


def login(request):
    if 'admin' in request.session:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        query = f"select `email`, `username`, `name`, `mobile`, `type` from admin where email='{email}' and password='{password}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        print(resut)
        if len(resut) > 0:
            request.session['admin'] = resut[0]
            return redirect('dashboard')
        else:
            messages.warning(request, 'invalid Email or Password !!!')
            return redirect('loginPage')
    return render(request, 'adminWork/login.html')

def dashboard(request):
    return render(request,'adminWork/dashboard.html')


def signout(request):
    try:
        del request.session['admin']
    except:
        pass
    return redirect('loginPage')


def changePassword(request):
    """
    in this function we are workin for change password
    :param request:
    :return :
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')

        query = f"select * from admin where email='{email}' and password='{oldPassword}'"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        resut = cr.fetchall()
        if len(resut) > 0:
            query = "UPDATE `admin` SET `password`='{}' WHERE `email`='{}'".format(newPassword, email)
            cr.execute(query)
            conn.commit()
            conn.close()
            messages.success(request, "Successfully Update password")

            return redirect('changePassword')
        else:
            messages.warning(request, 'Plz enter correct old Password!!!')
            return redirect('changePassword')
    return render(request, 'adminWork/changePassword.html')

# Area work Started
def addArea(request):
    if request.method=='POST':
        name = request.POST['name']
        state = request.POST['state']
        query ="select * from `area` where name ='{}' and state='{}'".format(name,state)
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        result = cr.fetchall()
        if len(result)>0:
            messages.warning(request, 'Allready Added')
            return redirect('addArea')

        query = f"INSERT INTO `area`(`name`, `state`) VALUES ('{name}','{state}')"
        cr.execute(query)
        conn.commit()
        messages.success(request, 'SuccessFully added')
        return redirect('addArea')
    return render(request,'adminWork/addArea.html')

def viewArea(request):
    query = "SELECT * FROM `area`"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    result = cr.fetchall()
    return render(request, 'adminWork/viewArea.html',{'data':result})

def deleteArea(request):
    id = request.GET['id']
    query = "DELETE FROM `area` WHERE id='{}'".format(id)
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request,'Success Fully Deleted !')
    return redirect('viewArea')

# End of area work


def addStroy(request):
    return render(request, 'adminWork/addStory.html')

def viewStory(request):
    return render(request, 'adminWork/viewStory.html')
