from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from random import randint


# Create your views here.
def home(request):
    return render(request, "index.html")

@login_required(login_url='/login_user/')
def dashboard(request):
    new_admin = Complain.objects.filter(status="New")
    assign_admin = Complain.objects.filter(status="Approved")
    rejected_admin = Complain.objects.filter(status="Rejected")
    inprogress_admin = Complain.objects.filter(status="On The Way")
    completed_admin = Complain.objects.filter(status="Completed")
    total_driver = Driver.objects.all()
    bin_inprogress = Bin.objects.filter(status="On The Way")
    bin_cleaned = Bin.objects.filter(status="Completed")
    return render(request, "dashboard.html", locals())

@login_required(login_url='/login2_user/')
def dashboard2(request):
    total = Complain.objects.filter(register__user=request.user)
    new = Complain.objects.filter(status="New", register__user=request.user)
    completed = Complain.objects.filter(status="Completed", register__user=request.user)
    return render(request, "dashboard2.html", locals())

@login_required(login_url='/driver_login/')
def dashboard3(request):
    assign = Complain.objects.filter(driver__user=request.user)
    inprogress = Complain.objects.filter(status="On The Way", driver__user=request.user)
    completeddriver = Complain.objects.filter(status="Completed", driver__user=request.user)

    assignbin = Bin.objects.filter(driver__user=request.user)
    inprogressbin = Bin.objects.filter(status="On The Way", driver__user=request.user)
    completeddriverbin = Bin.objects.filter(status="Completed", driver__user=request.user)
    return render(request, "dashboard3.html", locals())

def login_user(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                messages.success(request, "Invalid User")
                return redirect('login_user')
        except:
            messages.success(request, "Invalid User")
            return redirect('login_user')
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('home')

def registration(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        uname = request.POST['username']
        pwd = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['contactnumber']
        user = User.objects.create_user(first_name=fname, last_name=lname, email=email, username=uname, password=pwd)
        Registration.objects.create(user=user, address=address, contactnumber=mobile)
        messages.success(request, "Registration Successful")
        return redirect('login2_user')
    return render(request, 'registration.html')

@login_required(login_url='/login2_user/')
def reg_user(request):
    data = Registration.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", d)

def login2_user(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('login2_user')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('dashboard2')
        else:
            messages.success(request, "Invalid User")
            return redirect('login2_user')
    return render(request, "login2.html")

def logout2_user(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('home')





def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@login_required(login_url='/login2_user/')
def add_complain(request):
    if request.method == "POST":
        area = request.POST['area']
        locality = request.POST['locality']
        landmark = request.POST['landmark']
        address = request.POST['address']
        note = request.POST['note']
        photo = request.FILES['photo']

        Complain.objects.create(complain=random_with_N_digits(10),area=area, locality=locality, landmark=landmark, address=address, note=note, photo=photo, register=Registration.objects.get(user=request.user), status='New')
        messages.success(request, "Add Complain Successful")
        return redirect('complainlist')
    return render(request, "add_complain_user.html")

@login_required(login_url='/login2_user/')
def complainlist(request):
    data = Complain.objects.all()
    d = {'data': data}
    return render(request, "views_lodged.html", d)

@login_required(login_url='/login2_user/')
def admincomplainlist(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    data = Complain.objects.filter()
    if action == "New Complain":
        data = data.filter(status="New")
    elif action == "All Complain":
        data = data.filter()
    elif action == "Approved":
        data = data.filter(status="Approved")
    elif action == "Rejected":
        data = data.filter(status="Rejected")
    elif action == "Completed":
        data = data.filter(status="Completed")
    elif action == "On The Way":
        data = data.filter(status="On The Way")
    if user:
        data = data.filter(register__user__id=user)
        data2 = data.filter().first()
    register = Registration.objects.filter(user=request.user)
    driver = Driver.objects.filter(user=request.user)
    if request.user.is_staff:
        return render(request, "admin_complain.html", locals())
    elif driver:
        data = data.filter(driver__user=request.user)
        return render(request, "complain_report_driver.html", locals())
    elif register:
        data = data.filter(register__user=request.user)
        return render(request, "complain_history_user.html", locals())

@login_required(login_url='/login2_user/')
def edit_complain(request, pid):
    if request.method == "POST":
        area = request.POST['area']
        locality = request.POST['locality']
        landmark = request.POST['landmark']
        address = request.POST['address']
        note = request.POST['note']
        try:
            photo = request.FILES['photo']
            Complain.objects.filter(id=pid).update(photo=photo)
        except:
            pass

        Complain.objects.filter(id=pid).update(area=area, locality=locality, landmark=landmark, address=address, note=note)
        messages.success(request, "Update Complain Successful")
        return redirect('complainlist')
    data = Complain.objects.get(id=pid)
    d = {'data': data}
    return render(request, "edit_complain_user.html", d)

@login_required(login_url='/login2_user/')
def delete_complain(request, pid):
    user = request.GET.get('user')
    data = Complain.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Complain Successful")
    if request.user.is_staff:
        if user:
            return redirect('/admincomplainlist/?user=17')
        return redirect('complainlist')
    else:
        return redirect('admincomplainlist')

@login_required(login_url='/login_user/')
def detail(request, pid):
    data = Complain.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        driver = request.POST['driver']
        status = request.POST['status']
        datadrive = Driver.objects.get(id=driver)
        data.driver = datadrive
        data.status = status
        data.save()
        Trackinghistory.objects.create(complain=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('detail', pid)
    traking = Trackinghistory.objects.filter(complain=data)
    driverdata = Driver.objects.filter()
    if request.user.is_staff:
        return render(request, "complain_detail_admin.html", locals())
    else:
        return render(request, "detail.html", locals())

@login_required(login_url='/login_user/')
def add_bin(request):
    if request.method == "POST":
        idname = request.POST['idname']
        area = request.POST['area']
        locality = request.POST['locality']
        landmark = request.POST['landmark']
        loadtype = request.POST['loadtype']
        period = request.POST['period']
        bus = request.POST['bus']
        assign = request.POST['assign']

        Bin.objects.create(idname=idname, area=area, locality=locality, landmark=landmark, loadtype=loadtype, period=period, bus=bus, driver=Driver.objects.get(id=assign), status='New')
        messages.success(request, "Add Bin Successful")
        return redirect('binlist')
    driver = Driver.objects.all()
    return render(request, "add_bin_admin.html", locals())

@login_required(login_url='/login_user/')
def binlist(request):
    data = Bin.objects.all()
    d = {'data': data}
    return render(request, "view_Bin.html", d)

@login_required(login_url='/driver_login/')
def driverbinlist(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    if request.user.is_staff:
        data = Bin.objects.filter()
    else:
        driver = Driver.objects.get(user=request.user)
        data = Bin.objects.filter(driver=driver)
    if action == "New":
        data = data.filter(status="New")
    elif action == "On The Way":
        data = data.filter(status="On The Way")
    elif action == "Completed":
        data = data.filter(status="Completed")
    elif action == "Total":
        data = data.filter()
    if user:
        data = data.filter(register__user__id=user)
    d = {'data': data}
    if request.user.is_staff:
        return render(request, "bin_admin.html", d)
    else:
        return render(request, "bin_driver.html", d)

@login_required(login_url='/login_user/')
def edit_bin(request, pid):
    if request.method == "POST":
        idname = request.POST['idname']
        area = request.POST['area']
        locality = request.POST['locality']
        landmark = request.POST['landmark']
        loadtype = request.POST['loadtype']
        period = request.POST['period']
        bus = request.POST['bus']
        assign = request.POST['assign']
        driver = Driver.objects.get(id=assign)


        Bin.objects.filter(id=pid).update(idname=idname, area=area, locality=locality, landmark=landmark, loadtype=loadtype, period=period, bus=bus, driver=driver)
        messages.success(request, "Bin Updated")
        return redirect('binlist')
    driver = Driver.objects.all()
    data = Bin.objects.get(id=pid)
    return render(request, "edit_bin.html", locals())

@login_required(login_url='/login_user/')
def delete_bin(request, pid):
    data = Bin.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Bin")
    return redirect('binlist')

@login_required(login_url='/login_user/')
def detail_driver(request, pid):
    data = Bin.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Trackinghistory.objects.create(bin=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('detail_driver', pid)
    traking = Trackinghistory.objects.filter(bin=data)
    if request.user.is_staff:
        return render(request, "bin_detail_admin.html", locals())
    else:
        return render(request, "bin_detail_driver.html", locals())


@login_required(login_url='/login_user/')
def add_driver(request):
    if request.method == "POST":
        idname = request.POST['idname']
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']

        user = User.objects.create_user(username=idname, first_name=name, email=email, password=password)
        Driver.objects.create(mobile=mobile,address=address,user=user)
        messages.success(request, "Add Driver Successful")
        return redirect('driverlist')
    return render(request, "add_driver_admin.html")

@login_required(login_url='/login_user/')
def driverlist(request):
    data = Driver.objects.all()
    d = {'data': data}
    return render(request, "view_driver.html", d)

@login_required(login_url='/login_user/')
def edit_driver(request, pid):
    if request.method == "POST":
        idname = request.POST['idname']
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        data = Driver.objects.get(id=pid)
        user = User.objects.filter(id=data.user.id).update(username=idname, first_name=name, email=email)
        Driver.objects.filter(id=pid).update(mobile=mobile)
        messages.success(request, "Driver Updated")
        return redirect('driverlist')
    data = Driver.objects.get(id=pid)
    d = {'data': data}
    return render(request, "edit_driver.html", d)

@login_required(login_url='/login_user/')
def delete_driver(request, pid):
    data = Driver.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Driver Successfull")
    return redirect('driverlist')


def driver_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)

        if user:
            login(request, user)
            messages.success(request, "User Login Successful")
            return redirect('dashboard3')
        else:
            messages.success(request, "Invalid User")
            return redirect('driver_login')
    return render(request, "driver_login.html")

@login_required(login_url='/login2_user/')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['secondname']
        email = request.POST['email']
        uname = request.POST['username']
        mobile = request.POST['contactnumber']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname, email=email, username=uname)
        Registration.objects.filter(user=request.user).update(contactnumber=mobile)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Registration.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/login_user/')
def change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('change_password')

    return render(request,'change_password_admin.html')

@login_required(login_url='/login2_user/')
def change_password2(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('change_password')

    return render(request,'change_password_user.html')

@login_required(login_url='/login_user/')
def report(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Complain.objects.filter(creationdate__gte=fromdate, creationdate__lte=todate)
        data2 = True
    return render(request, "report.html", locals())

@login_required(login_url='/login_user/')
def driverwise(request):
    data = None
    data2 = None

    if request.GET.get('fromdate'):
        data = Driver.objects.filter()
        data2 = True
    return render(request, "driverwise.html", locals())

@login_required(login_url='/login_user/')
def driverbin(request):
    data = None
    data2 = None

    if request.GET.get('fromdate'):
        data = Bin.objects.filter()
        data2 = True
    return render(request, "search_driver_bin.html", locals())

@login_required(login_url='/login2_user/')
def user_search(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Complain.objects.filter(complain__icontains=fromdate)
    return render(request, "user_search.html", locals())


@login_required(login_url='/driver_login/')
def driver_changhe_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('change_password')

    return render(request,'driver_changhe_password.html')


@login_required(login_url='/driver_login/')
def drivercomplainlist(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    driver = Driver.objects.get(user=request.user)
    data = Complain.objects.filter(driver=driver)
    if action == "New":
        data = data.filter(status="Approved")
    elif action == "On The Way":
        data = data.filter(status="On The Way")
    elif action == "Completed":
        data = data.filter(status="Completed")
    elif action == "Total":
        data = data.filter()
    if user:
        data = data.filter(register__user__id=user)
    d = {'data': data}
    return render(request, "complain_driver.html", d)

@login_required(login_url='/driver_login/')
def complain_detail_driver(request, pid):
    data = Complain.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Trackinghistory.objects.create(complain=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('complain_detail_driver', pid)
    traking = Trackinghistory.objects.filter(complain=data)
    return render(request, "complain_detail_driver.html", locals())

@login_required(login_url='/driver_login/')
def search_bin(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate= request.POST['fromdate']
        data2 = True
        data = Bin.objects.filter(idname__icontains=fromdate)
    if request.user.is_staff:
        return render(request, "search_bin_admin.html", locals())
    else:
        if request.method == "POST":
            data = data.filter(driver__user=request.user)
        return render(request, "search_bin_driver.html", locals())

@login_required(login_url='/login_user/')
def search_complain(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate= request.POST['fromdate']
        data2 = True
        data = Complain.objects.filter(complain__icontains=fromdate)

    return render(request, "Search_complain.html", locals())

@login_required(login_url='/login_user/')
def report_search_bin(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        data2 = True
        data = Bin.objects.filter(creationdate__date__gte=fromdate, creationdate__date__lte=todate)
    return render(request, "search_bin_date.html", locals())

@login_required(login_url='/driver_login/')
def search_complain_bin(request):
    data = None
    data2 = None

    if request.GET.get('fromdate'):
        data = Bin.objects.filter()
        data2 = True
    return render(request, "search_complain_bin.html", locals())

@login_required(login_url='/driver_login/')
def search_complain_driver(request):
    data = None
    data2 = None

    if request.GET.get('fromdate'):
        data = Driver.objects.filter()
        data2 = True
    return render(request, "search_complain_driver.html", locals())

@login_required(login_url='/driver_login/')
def complain_search_bin(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate= request.POST['fromdate']
        data2 = True
        data = Complain.objects.filter(complain__icontains=fromdate)

    return render(request, "complain_search_driver.html", locals())

@login_required(login_url='/login_user/')
def delete_user(request, pid):
    reg = Registration.objects.get(id=pid)
    user = User.objects.get(id=reg.user.id)
    user.delete()
    messages.success(request, "Deleted successfully")
    return redirect('reg_user')



