import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from pymysql import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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
    query = "SELECT * FROM `profile` WHERE `status` = 'Missing'  ORDER BY rand()"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    resut = cr.fetchall()

    return render(request, 'client/index.html',{'results':resut})


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
        query = f"INSERT INTO `profile`(`name`, `fatherName`, `address`, `identificationMarks`, `mobile`, `email`,  `status`, `area`, `SignUp`) VALUES ('{name}','{fname}','{address}','{identificationMarks}','{mobile}','{email}','{status}','{area}','{user}')"
        conn = makeConnections()
        cr = conn.cursor()
        cr.execute(query)
        id = cr.lastrowid
        filename = fs.save('missingPerson/' + str(id)+'.'+photo.name.split('.')[1], photo)
        upQuery = "UPDATE `profile` SET `photo`='{}' WHERE `id`='{}'".format(filename,id)
        cr.execute(upQuery)
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


def updatePostStatus(request):
    name = request.GET['name']
    query ="UPDATE `profile` SET `status`='Found' WHERE `id`='{}'".format(request.GET['id'])
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    messages.success(request,'Sucess fully update status {}'.format(name))
    return redirect('userProfile')

def deletePost(request):
    query = "DELETE FROM `profile` WHERE id='{}'".format(request.GET['id'])
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    conn.commit()
    return redirect('userProfile')

def topStoryFound(request):
    query = "SELECT * FROM `profile` WHERE `status` = 'Found'  ORDER BY rand()"
    conn = makeConnections()
    cr = conn.cursor()
    cr.execute(query)
    resut = cr.fetchall()
    return render(request, 'client/topstory.html',{'results':resut})


from haarCascade import get_cv2_image_from_base64_string,get_cropped_img_if_2_eye, MakeEncodeAndCFindCriminal

@csrf_exempt
def validateImages(request):
    print(request.POST)
    b64 = request.POST['b64']
    bash64_to_img = get_cv2_image_from_base64_string(b64)
    check_eyes = get_cropped_img_if_2_eye(bash64_to_img)
    if check_eyes:
        return HttpResponse('success')
    else:
        return HttpResponse("fail")


def searchMissingPerson(request):
    return render(request, 'client/SearchMissingPerson.html')


@csrf_exempt
def searchResultAction(request):
    b64 = request.POST['b64']
    bash64_to_img = get_cv2_image_from_base64_string(b64)
    obj = MakeEncodeAndCFindCriminal()
    result  = obj.search(bash64_to_img)
    if len(result)>0:
        return JsonResponse({'content':result})
    else:
        return JsonResponse({'content':'no'})


