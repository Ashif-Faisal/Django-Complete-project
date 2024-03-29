import os
import requests
import mysql.connector
from bs4 import BeautifulSoup
from datetime import date
from tabulate import tabulate
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import userProfileForm, createUserForm
from .functions import handle_uploaded_file
from .models import userprofile
from .serializers import PatientSerializer
from django.contrib.auth import logout
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.base import MIMEBase
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect

def _send_mail(my_body, employee, comment, id, team, creatoremail,latest_update):
        message = MIMEMultipart()
        # filename = ''
        # # attachment = open(os.path.dirname(os.path.abspath("__file__")), "rb")
        # attachment = ''
        # p = MIMEBase('application', 'octet-stream')
        # p.set_payload((attachment).read())
        # encoders.encode_base64(p)  # updated
        # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        # message.attach(p)
        sample_str = str(my_body)
        require_chars = sample_str[0:50]
        print(team)
        creatorEmail= creatoremail
        task_id = id
        message['Subject'] = '[TT- '+str(task_id)+'] ''' +require_chars
        message['From'] = 'cropticket@gmail.com'
        To_receiver = [team]
        Cc_receiver = [creatoremail]
        message['To'] = ";".join(To_receiver)
        message['Cc'] = ";".join(Cc_receiver)
        print(message['Cc'])
        receiver = To_receiver + Cc_receiver

        body = ''' Ticket Initiated by: <br>'''+ str(employee)+ ''' <br><br>Details: <br>'''+ sample_str+'''<br><br> Comments: <br>'''+str(comment)+'''<br><br> Last Update: <br>'''+str(latest_update)
        message.attach(MIMEText(body, "html"))
        msg_body = message.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(message['From'], 'lcoxoewiawemqbip')
        # server.login(message['From'], '')
        server.sendmail(message['From'], receiver, msg_body)
        server.quit()
        return "Mail sent successfully."


@login_required
def Tasksearch(request):
    task_list = userprofile.objects.all()
    user_filter = userprofile(request.GET, work_Stream=task_list)
    return render(request, 'taskview1.html', {'filter': user_filter})


@login_required
def action(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x = cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'unassignTaskV2.html')

@login_required
def edit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'edit.html', context)

@login_required
def editupdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")
        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")
        print(x)
        # return redirect('unassignTaskV2')

        return render(request, 'edit.html')


@login_required
def lastupdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_userprofile WHERE Updated_task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data, 'report': report, 'current_datetime':current_datetime}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'update.html', context)


# def ticketLastUpdate(request):
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s ORDER BY update_date DESC limit 1', [task_id])
#     report = cursor.fetchall()
#     print(report)
#     context = {'info': report}
#     return render(request, 'customerTicketStatus.html',context)

@login_required
def updateinfo(request):
    if request.method == 'POST':
        value = request.POST.get("value")
        print(value)
        latest_update = request.POST.get("task_details")
        task = request.POST.get("task")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")
        comment = request.POST.get("comment")
        Creator_email = request.POST.get("Creator_email")
        UpdateMakers = request.POST.get("UpdateMakers")

        user=  request.user
        print(user)

        if value=='Save':
            cursor = connection.cursor()
            y = cursor.execute("INSERT INTO support_portal_userprofile (latest_update, Updated_task_id, update_Date, UpdateMakers) VALUES (%s, %s, %s, %s)",[latest_update, task_id, update_date, UpdateMakers])
            if y:
                messages.success(request, "Last update entry successfully and this update send via Email..!!")

            cursor.execute("""UPDATE support_portal_userprofile SET approval= 'On Going', status= 'Pending' WHERE id= %s""" % (task_id))

            user = request.user
            print(user)

            cursor.execute('select email from auth_user where username= %s', [user])
            email = cursor.fetchall()
            for email in email:
                print(email[0])
            creatoremail = email[0]
            print("creatoremailll" + creatoremail)

            team = Creator_email
            print(latest_update)
            print(user)
            print(task_id)
            print(creatoremail)
            print(comment)

            _send_mail(task, user, comment, task_id, team, creatoremail, latest_update)

            context = {'updatedata': y}
            return render(request, 'unassignTaskV2.html', context)

        elif value=='Save & Closed':
            cursor = connection.cursor()
            y = cursor.execute("INSERT INTO support_portal_userprofile (latest_update, Updated_task_id, update_Date,UpdateMakers) VALUES (%s, %s, %s,%s)",[latest_update, task_id, update_date,UpdateMakers])
            if y:
                messages.success(request, "Last update entry successfully..!!")

            cursor.execute("""UPDATE support_portal_userprofile SET approval= 'Complete', status= 'Done' WHERE id= %s""" % (task_id))

            user = request.user
            print(user)

            cursor.execute('select email from auth_user where username= %s', [user])
            email = cursor.fetchall()
            for email in email:
                print(email[0])
            creatoremail = email[0]
            print("creatoremailll" + creatoremail)

            team= Creator_email
            print(latest_update)
            print(user)
            print(task_id)
            print(creatoremail)
            print(comment)

            _send_mail(task, user,comment, task_id,team, creatoremail,latest_update)
            context = {'updatedata': y}
            return render(request, 'unassignTaskV2.html', context)

@login_required
def details(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [id])
        data = cursor.fetchall()
        context = {'data': data}
        return render(request, 'details.html', context)

@login_required
def delete(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        x= cursor.execute('DELETE FROM support_portal_userprofile WHERE id= %s', [id])
        if x:
            messages.success(request, "Task Deleted Successfully..!!")
        return render(request, 'taskview1.html')


def taskInput(request):
    return render(request,'taskinput.html')


def homepage(request):
    return render(request, 'home.html')


def sample1(request):
    return render(request, 'sample1.html')


def taskview1(request):
    return render(request, 'taskview1.html')

@login_required
def taskstatusPerson(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM auth_user')
        data = cursor.fetchall()
        context = {'data': data}
        print(data)
        return render(request, 'taskstatusPerson.html',context)

@login_required
def taskstatus(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT username FROM auth_user')
        data = cursor.fetchall()
        context = {'info': data}
        print(data)
        # return render(request, 'taskstatusPerson.html', context)
        return render(request, 'taskstatus.html', context)

@login_required
def taskview(request):
    if request.method == 'POST':

        work_stream=request.POST.get("task")
        print(task)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s ', [task])
        data = cursor.fetchall()

        context = {'data': data}
        return render(request, 'unassignTaskV2.html',  context)

@login_required
def searchview(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        cursor = connection.cursor()
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        info = cursor.fetchall()
        context = {'data': data, 'info': info}
        return render(request, 'taskstatus.html',  context)


def diff_time(created_date, cursor):
    current_date = datetime.now()
    for item in created_date:
        x = item[0].strftime("%Y-%m-%d")
        cursor.execute(f'''select datediff('{current_date}','{x}') from support_portal_userprofile''')
        yield cursor.fetchall()


@login_required
def pendingTask(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        print(employee_id)
        cursor = connection.cursor()
        # cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE maker1 = %s and status='Pending'", [employee_id])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left "
                       "join (select	* from (select	MAX(id) as max_id, s.task_id as new_task_id	from "
                       "support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate "
                       "spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE a. maker1 = %s and status='Pending'",[employee_id])
        data = cursor.fetchall()
        # user dropdown menu
        cursor.execute('SELECT username FROM auth_user')
        alluser = cursor.fetchall()
        context = {'data': data, 'alluser': alluser}
        return render(request, 'unassignTask.html',  context)


def filterTask(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task_status = request.POST.get("task_status")
        print(employee_id)
        print(task_status)

        # groupname=request.user.groups.name
        getGroupName = request.user.groups.values_list('name', flat=True).first()
        print("This is group name")
        group=getGroupName
        print(getGroupName)


        # task_status = ''
        if employee_id != '' and task_status == 'null':
            cursor = connection.cursor()
            cursor.execute(
                """SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile  a left join (select * from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE (team='%s' or employee_id='%s')  and (approval="Not Started yet" or approval= "On Going") order by a.id DESC;""" % (group,employee_id))
            data = cursor.fetchall()
            # user dropdown menu
            cursor.execute('SELECT username FROM auth_user')
            alluser = cursor.fetchall()
            context = {'data': data, 'alluser': alluser}
            return render(request, 'unassignTaskV2.html', context)

        elif employee_id != '' and task_status == 'Pending':
            cursor = connection.cursor()
            cursor.execute(""" SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select * from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE (team='%s' or employee_id='%s') and a.status = '%s' and maker1='%s' and (a.approval="Not Started yet" or a.approval= "On Going") order by a.id DESC """ % (group,employee_id, task_status,employee_id))
            data = cursor.fetchall()
            # user dropdown menu
            cursor.execute('SELECT username FROM auth_user')
            alluser = cursor.fetchall()
            context = {'data': data, 'alluser': alluser}
            return render(request, 'unassignTaskV2.html', context)
        elif employee_id != '' and task_status == 'Done':
            print("employee_id not null and task_status equal Done")
            cursor = connection.cursor()
            cursor.execute(""" SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select * from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE team='%s' and a.maker1 = '%s' and a.status = '%s' order by a.id DESC """ % (group,employee_id, task_status,))
            data = cursor.fetchall()
            # user dropdown menu
            cursor.execute('SELECT username FROM auth_user')
            alluser = cursor.fetchall()
            context = {'data': data, 'alluser': alluser}
            return render(request, 'unassignTaskV2.html', context)

        elif employee_id != '' and task_status == 'Not Started yet':
            print("employee_id not null and task_status equal Done")
            cursor = connection.cursor()
            cursor.execute(
                """ SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select * from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE team='%s'and a.approval = '%s' order by a.id DESC """ % (group,task_status,))
            data = cursor.fetchall()
            # user dropdown menu
            cursor.execute('SELECT username FROM auth_user')
            alluser = cursor.fetchall()
            context = {'data': data, 'alluser': alluser}
            return render(request, 'unassignTaskV2.html', context)
        elif employee_id != '' and task_status == 'all':
            cursor = connection.cursor()
            # cursor.execute("SELECT * FROM myappdb.support_portal_userprofile s WHERE status = '%s' order by s.id DESC", [task_status])
            cursor.execute(""" SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select * from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE team='%s' and a.maker1 = '%s' order by a.id DESC """ % (group,employee_id))
            data = cursor.fetchall()
            # user dropdown menu
            cursor.execute('SELECT username FROM auth_user')
            alluser = cursor.fetchall()
            context = {'data': data, 'alluser': alluser}
            return render(request, 'unassignTaskV2.html', context)

# def pendingTask(request):
#     if request.method == 'POST':
#
#         pendingTask = request.POST.get("Pending")
#         userlist = userprofile.objects.filter(status=pendingTask)
#         context = {'data': userlist}
#         return render(request, 'pendingTask.html', context)


def search(request):
    return render(request, 'search.html')


def wellcome(request):
    return render(request, 'wellcome.html')

@login_required
def get_all_patient_info(request):
    # get all data from database
    all_patient_info = userprofile.objects.all()
    serializer = PatientSerializer(all_patient_info, many=True)
    return JsonResponse(serializer.data, safe=False)


# def report3(request):
#     cursor=connection.cursor()
#     cursor.execute('SELECT * FROM support_portal_userprofile')
#     userlist= cursor.fetchall()
#     context = {'data': userlist}
#     return render(request, 'report3.html', context)

# def report3(request):
#     datalist = userprofile.objects.all()
#     context = {'data': datalist}
#     return render(request, 'report3.html', context)

#
@login_required
def report2(request, acd):
    userlist=userprofile.objects.filter(acd=acd)
    context = {'data': userlist}
    return render(request, 'report.html', context)

@login_required
def report(request):
    userlist = userprofile.objects.all()
    context = {'data': userlist}
    return render(request, 'report3.html', context)


def regview(request):
    form = createUserForm()

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            if form.save():
                messages.success(request, "User Create Successfully..!!")
            return redirect('regview')

    cursor = connection.cursor()
    cursor.execute('select id from auth_user order by id DESC limit  1 ')
    last_user = cursor.fetchall()
    print(last_user)
    for i in last_user:
        print(i[0])
    lastCreatedUserId = i[0]
    print(lastCreatedUserId)


    group_id = request.POST.get("group_id")
    print(group_id)

    # group_id='1'
    # cursor = connection.cursor()
    # x = cursor.execute(
    #     "INSERT INTO auth_user_groups(user_id, group_id) VALUES (%s, %s)",
    #     [lastCreatedUserId, group_id])

    cursor = connection.cursor()
    cursor.execute('select * from auth_user order by id DESC')
    # cursor.execute('select * from auth_user')
    Alluser = cursor.fetchall()
    print(Alluser)

    context = {'form': form, 'Alluser': Alluser}
    return render(request, 'userReg.html', context)
    # return redirect('login')


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = None
            if user.groups.exists():
                group = user.groups.all()[0].name
            # if group == 'systems':
                return redirect('testpage')

            # if group == 'DataTeam':
            #     return redirect('sysnewticket')
            #
            # if group == 'TechOps':
            #     return redirect('sysnewticket')
            #
            # # if group == 'systems':
            # #     return redirect('newticket')
            #
            # # return redirect('dashboard')
            return redirect('newticket')

        else:
            messages.success(request, "Incorrect Username or Password")

    if request.user.is_authenticated:
        user = request.user
        if user.groups.exists():
            group = user.groups.all()[0].name
            return redirect('sysnewticket')
        return redirect('newticket')
    context = {}
    return render(request, 'login.html', context)


def bootstrap(request):
    return render(request, 'boot.html')


# def testpage(request):
#     # cursor = connection.cursor()
#     # cursor.execute('SELECT username FROM auth_user')
#
#     getGroupName = request.user.groups.values_list('name', flat=True).first()
#     CurrentUserGroup = getGroupName
#
#     context = {'CurrentUserGroup':CurrentUserGroup}
#     return render(request, 'base.html', context)


def errorpage(request):
    return render(request, 'error.html')

@login_required
def newticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    user = request.user
    print(user)

    cursor = connection.cursor()
    cursor.execute('select email from auth_user where username= %s',[user])
    get_email = cursor.fetchall()
    for get_email in get_email:
        print(get_email[0])
    get_email = get_email[0]
    print(f"TeamEmail" + get_email)

    cursor = connection.cursor()
    cursor.execute('select name from auth_group order by id ASC')
    get_group = cursor.fetchall()

    context = {'current_datetime': current_datetime,'get_group': get_group,'get_email':get_email}
    return render(request, 'newticket.html',context)


@login_required
def indexview(request):
    return render(request, 'index.html')


# @login_required
# @login_required(views.loginview())
@login_required
def infoview(request):
    form = userProfileForm()
    if request.method == 'POST':
        print(request.POST)
        form = userProfileForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if form.save():
                messages.success(request, "Task Added Successfully..!!")

    cursor = connection.cursor()
    cursor.execute('SELECT username FROM auth_user')
    x = cursor.fetchall()

    #current_datetime = datetime.now()

    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'form': form, 'data': x,'current_datetime': current_datetime}
    return render(request, 'info.html', context)


# def saveticket(request):
#     form = newticket()
#     if request.method == 'POST':
#         print(request.POST)
#         form = newticket(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             if form.save():
#                 messages.success(request, "Task Added Successfully..!!")
#
#     cursor = connection.cursor()
#     cursor.execute('SELECT username FROM auth_user')
#     x = cursor.fetchall()
#
#     context = {'form': form, 'data': x}
#     return render(request, 'newticket.html', context)


def saveticket(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        Creator_email = request.POST.get("Creator_email")
        print(Creator_email)
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x= cursor.execute("INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team, Creator_email) VALUES (%s, %s,  %s, %s, %s, %s, %s)",[employee_id, task, comment,request_date,approval, team, Creator_email])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id= i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s',[employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail= email[0]
        print("creatoremailll"+creatoremail)

        latest_update=''

        messages.success(request, "Ticket entry successfully..!!")

        cursor.execute('select email from auth_group where name= %s', [team])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        teamEmail = email[0]
        print(f"TeamEmail" + teamEmail)

        team = teamEmail

        # if team == 'systems':
        #     team = 'systems@surecash.net'
        # elif team=='TechOps':
        #     team = 'tech_ops@surecash.net'
        # elif team=='DataTeam':
        #     team = 'data@surecash.net'

        _send_mail(task, employee_id, comment, id, team,creatoremail,latest_update)
        return render(request, 'newticket.html')

#
# def task_id(request):
#     if request.method == 'POST':
#         cursor = connection.cursor()
#         cursor.execute('select id from support_portal_userprofile')
#         data = cursor.fetchall()
#         print(data)
#
#     return render(request, 'newticket.html')


def approved(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'approved.html',context)


def todayticket(request):
    if request.method == 'POST':

        cursor = connection.cursor()
        cursor.execute("select * from support_portal_userprofile where current_date and current_date order by request_date")
        data = cursor.fetchall()
        print(data)
        context = {'data': data}
        return render(request, 'approved.html',context)


@login_required
def datewiseticket(request):
    if request.method == 'POST':
        form_date = request.POST.get("form_date")
        to_date = request.POST.get("to_date")
        print(form_date)
        print(to_date)
        cursor = connection.cursor()
        cursor.execute('select * from support_portal_userprofile where request_date>= %s and request_date<= %s order by request_date DESC',[form_date, to_date])
        data = cursor.fetchall()
        print(data)
        context = {'data': data}
        return render(request, 'approved.html',context)


@login_required
def customerTicketStatus(request):
    user = request.user
    print(user)
    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE (approval="Not Started yet" or approval= "On Going" or approval= "Complete") and employee_id= %s order by request_date DESC',[user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'customerTicketStatus.html',context)

# def all_id(request):
#     cursor = connection.cursor()
#     # cursor.execute('SELECT id from support_portal_userprofile')
#     # all_id= cursor.fetchall()
#     # print(all_id)


@login_required
def customerTicketInfo(request):
    if request.method == 'POST':
        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and employee_id= %s and team="systems"', [status,employee_id])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'customerTicketStatus.html', context)


@login_required
def TicketStatus(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        return render(request, 'unassignTask.html', context)


@login_required
def customerTaskView(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()
        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()
        # cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        # report = cursor.fetchall()
        # print(report)
        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        cursor.execute('SELECT * FROM support_portal_userprofile WHERE Updated_task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)


        context = {'data': data, 'user': x, 'report': report, 'current_datetime': current_datetime}
        # context = {'data': data, 'report': report, 'current_datetime': current_datetime}
        return render(request, 'customerTaskView.html', context)


@login_required
def customerTicketApproval(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        print(employee_id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE approval="Waiting_For_Appoval" and employee_id= %s',[employee_id])
        data = cursor.fetchall()
        print(data)
        context = {'approval': data}
        return render(request, 'customerTicketStatus.html', context)


@login_required
def unassignTask(request):
    user = request.POST.get("employee_id")
    print(user)
    id = request.POST.get("id")
    print(id)
    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left join (select	* from (select	MAX(id) as max_id, s.task_id as new_task_id	from support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE team="systems" and (approval="Not Started yet" or approval= "On Going") order by request_date DESC;')
    data = cursor.fetchall()
    cursor.execute('select username from auth_user')
    alluser = cursor.fetchall();
    print(alluser)
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {'data': data, 'alluser': alluser}
    return render(request, 'unassignTask.html', context)
    # context = {'data': data,'alluser': alluser}
    # return render(request, 'unassignTask.html', context)
    cursor.execute('select username from auth_user')
    alluser = cursor.fetchall();
    print(alluser)
    context = {'data': data, 'alluser': alluser}
    return render(request, 'unassignTask.html', context)


@login_required
def pendingTicket(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        cursor = connection.cursor()
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status='Pending'")
        # cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile a left "
        #                "join (select	* from (select	MAX(id) as max_id, s.task_id as new_task_id	from "
        #                "support_portal_infoupdate s group by s.task_id ) as tt inner join support_portal_infoupdate "
        #                "spi on spi.id = tt.max_id) b on a.id = b.new_task_id WHERE a.status='Pending' order by a.request_date DESC;")
        data = cursor.fetchall()
        cursor.execute('SELECT username FROM auth_user')
        info = cursor.fetchall()
        context = {'data': data, 'info': info}
        return render(request, 'pendingTicket.html',  context)


@login_required
def allTask(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE status= %s')
        data = cursor.fetchall()
        context = {'data': data}
        return render(request, 'taskstatus.html',  context)


@login_required
def sysnewticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    cursor = connection.cursor()
    cursor.execute('select name from auth_group order by id ASC')
    get_group = cursor.fetchall()

    user = request.user
    print(user)

    cursor = connection.cursor()
    cursor.execute('select email from auth_user where username= %s', [user])
    get_email = cursor.fetchall()
    for get_email in get_email:
        print(get_email[0])
    get_email = get_email[0]
    print(f"TeamEmail" + get_email)

    context = {'current_datetime': current_datetime,'get_group':get_group,'get_email':get_email}
    return render(request, 'sysnewticket.html', context)


@login_required
def SysTicketSaved(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        # attachment = request.POST.get("attachment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        Creator_email = request.POST.get("Creator_email")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        # print(attachment)
        print(request_date)
        print(approval)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team, Creator_email) VALUES (%s, %s,  %s, %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team, Creator_email])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        # messages.success(request, "Ticket entry successfully..!!")

        cursor.execute('select email from auth_group where name= %s', [team])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        teamEmail = email[0]
        print(f"TeamEmail" + teamEmail)


        team = teamEmail

        # if team == 'systems':
        #     team = 'ashif.faisal0@gmail.com'
        # elif team == 'TechOps':
        #     team = 'faisal@surecash.net'
        # elif team == 'DataTeam':
        #     team = 'fahimm@surecash.net'

        latest_update=''
        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        _send_mail(task, employee_id, comment, id, team, creatoremail, latest_update)

        if x:
            messages.success(request, "Ticket entry successfully..!!")
            return redirect('sysnewticket')

        context = {'current_datetime': current_datetime}
        return render(request, 'sysnewticket.html', context)

       # _send_mail(task, employee_id, comment, id, team, creatoremail,latest_update)
       #  return render(request, 'sysnewticket.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def test(request):
    getGroupName = request.user.groups.values_list('name', flat=True).first()
    CurrentUserGroup = getGroupName

    context = {'CurrentUserGroup': CurrentUserGroup}
    return render(request, 'base.html', context)


def techTicketStatus(request):
    user = request.POST.get("employee_id")
    print(user)

    id = request.POST.get("id")
    print(id)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE team="TechOps" or (approval="Not Started yet" or approval= "On Going" or approval= "Complete")  and employee_id= %s order by request_date DESC',
        [user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'techTicketStatus.html', context)


def techAssignedTicket(request):
    cursor = connection.cursor()
    cursor.execute('select *,datediff(etd,current_date) as pending_days from support_portal_userprofile where (approval= "Not Started yet" or approval="On Going") and team="TechOps" order by request_date DESC')
    data = cursor.fetchall()
    print(data)
    context = {'data': data}
    return render(request, 'techAssignedTicket.html', context)


def dataticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'dataticket.html', context)


def techticket(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'techticket.html', context)

#
# def techTicketsave(request):
#     if request.method == 'POST':
#         employee_id = request.POST.get("employee_id")
#         task = request.POST.get("task")
#         comment = request.POST.get("comment")
#         # attachment = request.POST.get("attachment")
#         request_date = request.POST.get("request_date")
#         approval = request.POST.get("approval")
#         team = request.POST.get("team")
#         print(team)
#         print(employee_id)
#         print(task)
#         print(comment)
#         # print(attachment)
#         print(request_date)
#         print(approval)
#         cursor = connection.cursor()
#         x = cursor.execute(
#             "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",
#             [employee_id, task, comment, request_date, approval, team])
#
#         cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
#         thistuple = cursor.fetchall()
#         for i in thistuple:
#             print(i[0])
#
#         id = i[0]
#         print(id)
#
#         cursor.execute('select email from auth_user where username= %s', [employee_id])
#         email = cursor.fetchall()
#         for email in email:
#             print(email[0])
#
#         creatoremail = email[0]
#         print("creatoremailll" + creatoremail)
#
#         messages.success(request, "Ticket entry successfully..!!")
#         if team == 'systems':
#             team = 'systems@surecash.net'
#         elif team == 'TechOps':
#             team = 'tech_ops@surecash.net'
#         elif team == 'DataTeam':
#             team = 'data@surecash.net'
#         _send_mail(task, employee_id, comment, id, team, creatoremail)
#         return render(request, 'techticket.html')

def techEdit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'techEdit.html', context)

def techEditUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")
        # print(sr_name)
        # print(work_stream)
        # print(task)
        # print(value_hml)
        # print(request_by_actor)
        # print(request_date)
        # print(needed_date)
        # print(etd)
        # print(acd)
        # print(status)
        # print(maker1)
        # print(maker2)
        # print(checker)
        # print(outside_office_time)
        # print(add_to_google)
        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")

        print(x)
        return render(request, 'techEdit.html')



def techTicketLastUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data,'user':x, 'report': report, 'current_datetime':current_datetime}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'techUpdatePage.html', context)


def techUpdatePage(request):
    if request.method == 'POST':
        latest_update = request.POST.get("task_details")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")

        user=  request.user
        print(user)
        # user = request.POST.get("{{ user }}")
        # print("Ok"+user)
        # print(latest_update)
        # print(task_id)
        # print(update_date)
        cursor = connection.cursor()
        y= cursor.execute("INSERT INTO support_portal_infoupdate (latest_update, task_id, update_Date) VALUES (%s, %s, %s)",[latest_update, task_id, update_date])
        if y:
            messages.success(request, "Last update entry successfully..!!")

        cursor.execute("UPDATE support_portal_userprofile SET approval= 'On Going', maker1= %s WHERE id= %s", [user,task_id])

        context = {'updatedata': y}
        return render(request, 'techTicketStatus.html', context)

#
# def dataTicketSave(request):
#     if request.method == 'POST':
#         employee_id = request.POST.get("employee_id")
#         task = request.POST.get("task")
#         comment = request.POST.get("comment")
#         # attachment = request.POST.get("attachment")
#         request_date = request.POST.get("request_date")
#         approval = request.POST.get("approval")
#         team = request.POST.get("team")
#         print(team)
#         print(employee_id)
#         print(task)
#         print(comment)
#         # print(attachment)
#         print(request_date)
#         print(approval)
#         cursor = connection.cursor()
#         x = cursor.execute(
#             "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team) VALUES (%s, %s,  %s, %s, %s, %s)",
#             [employee_id, task, comment, request_date, approval, team])
#
#         cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
#         thistuple = cursor.fetchall()
#         for i in thistuple:
#             print(i[0])
#
#         id = i[0]
#         print(id)
#
#         cursor.execute('select email from auth_user where username= %s', [employee_id])
#         email = cursor.fetchall()
#         for email in email:
#             print(email[0])
#
#         creatoremail = email[0]
#         print("creatoremailll" + creatoremail)
#
#         messages.success(request, "Ticket entry successfully..!!")
#         if team == 'systems':
#             team = 'systems@surecash.net'
#         elif team == 'TechOps':
#             team = 'tech_ops@surecash.net'
#         elif team == 'DataTeam':
#             team = 'data@surecash.net'
#         _send_mail(task, employee_id, comment, id, team, creatoremail)
#         return render(request, 'dataticket.html')
#
#

def dataTicketStatus(request):
    user = request.POST.get("employee_id")
    print(user)

    id = request.POST.get("id")
    print(id)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE team="DataTeam" or (approval="Not Started yet" or approval= "On Going" or approval= "Complete")  and employee_id= %s order by request_date DESC',
        [user])
    data = cursor.fetchall()
    context = {'data': data}
    return render(request, 'dataTicketStatus.html', context)


def dataEdit(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        context = {'data': data,'owner':x}
        #cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'dataEdit.html', context)


def dataEditUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        sr_name = request.POST.get("sr_name")
        work_stream = request.POST.get("work_stream")
        task = request.POST.get("task")
        value_hml = request.POST.get("value_hml")
        urgent_yn = request.POST.get("urgent_yn")
        request_by_actor = request.POST.get("request_by_actor")
        needed_date = request.POST.get("needed_date")
        etd = request.POST.get("etd")
        status = request.POST.get("status")
        maker1 = request.POST.get("maker1")
        maker2 = request.POST.get("maker2")
        checker = request.POST.get("checker")
        outside_office_time = request.POST.get("outside_office_time")
        add_to_google = request.POST.get("add_to_google")
        approval = request.POST.get("approval")

        cursor = connection.cursor()
        x = cursor.execute("UPDATE support_portal_userprofile SET sr_name= %s,work_stream= %s, task= %s, value_hml= %s, urgent_yn= %s,request_by_actor= %s,needed_date= %s,etd= %s,status= %s,maker1= %s,maker2= %s,checker= %s,outside_office_time= %s,add_to_google= %s,approval= %s  WHERE id= %s", [sr_name, work_stream,task, value_hml,urgent_yn,request_by_actor,needed_date,etd,status,maker1,maker2,checker,outside_office_time,add_to_google,approval, id])
        # y = cursor.execute('SELECT * FROM support_portal_userprofile WHERE task_id=')
        if x:
            messages.success(request, "Assigned successfully..!!")

        print(x)
        return render(request, 'dataEdit.html')


def dataTicketLastUpdate(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        task_id = request.POST.get("id")
        print(id)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE id= %s ORDER BY request_date DESC limit 1', [id])
        data = cursor.fetchall()

        cursor.execute('SELECT username FROM auth_user')
        x = cursor.fetchall()

        cursor.execute('SELECT * FROM support_portal_infoupdate WHERE task_id= %s', [task_id])
        report = cursor.fetchall()
        print(report)

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        context = {'data': data, 'user': x, 'report': report, 'current_datetime': current_datetime}
        # cursor.execute("UPDATE support_portal_userprofile SET sr_name='sr_name' WHERE task_id= %s", [task_id])

        return render(request, 'dataUpdatePage.html', context)


def dataUpdatePage(request):
    if request.method == 'POST':
        latest_update = request.POST.get("task_details")
        task_id = request.POST.get("id")
        update_date = request.POST.get("update_Date")

        user=  request.user
        print(user)
        cursor = connection.cursor()
        y= cursor.execute("INSERT INTO support_portal_infoupdate (latest_update, task_id, update_Date) VALUES (%s, %s, %s)",[latest_update, task_id, update_date])
        if y:
            messages.success(request, "Last update entry successfully..!!")

        cursor.execute("UPDATE support_portal_userprofile SET approval= 'On Going', maker1= %s WHERE id= %s", [user,task_id])

        context = {'updatedata': y}
        return render(request, 'dataTicketStatus.html', context)



def techTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='TechOps'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'techTicketState.html',context)


def dataTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='DataTeam'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        context = {'data': data}
        # return render(request, 'approved.html', context)
        return render(request, 'dataTicketState.html',context)



def sysTicketState(request):
    if request.method == 'POST':

        status=request.POST.get("status")
        print(status)
        task_id=request.POST.get("id")
        employee_id=request.POST.get("employee_id")
        print(employee_id)

        cursor = connection.cursor()
        #cursor.execute('SELECT *,datediff(current_date,request_date) as pending_days FROM support_portal_userprofile WHERE status= %s', [status])
        cursor.execute("SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE status= %s and team='systems'", [status])
        data = cursor.fetchall()

        cursor.execute('SELECT latest_update FROM support_portal_infoupdate where task_id= %s',[task_id])
        last_update = cursor.fetchall()
        print(last_update)

        cursor.execute('select username from auth_user')
        alluser = cursor.fetchall();
        print(alluser)

        context = {'data': data,'alluser':alluser}
        # return render(request, 'approved.html', context)
        return render(request, 'sysTicketState.html',context)


def actionForData(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x= cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'dataTicketStatus.html')
    # return render(request, 'dataTicketStatus.html')


def actionForTech(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print("ok")
        cursor = connection.cursor()
       # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s', [task])
        x= cursor.execute("UPDATE support_portal_userprofile set status='Done', approval='Complete'  WHERE id= %s", [id])
        #print(x)
        if x:
            messages.success(request, "Task Closed Successfully..!!")
    return render(request, 'techTicketStatus.html')


def searchResult(request):
    if request.method == 'POST':

        task=request.POST.get("task")
        print(task)
        cursor = connection.cursor()
        task =  '%'+ task+'%'
        # cursor.execute('SELECT * FROM support_portal_userprofile WHERE task= %s ', [task])
        cursor.execute('SELECT * FROM support_portal_userprofile WHERE task like %s', [task])
        data = cursor.fetchall()

        context = {'data': data}
        return render(request, 'unassignTaskV2.html',  context)


def searchResultV2(request):
    if request.method == 'POST':
        query = request.POST.get("task")
        print(query)
        submitbutton = request.POST.get("Search")
        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)

            results = userprofile.objects.filter(lookups).distinct()
            print(results)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM support_portal_userprofile WHERE task like %%s% ', [results])
            data = cursor.fetchall()
            print(data)

            context={'data': data, 'submitbutton': submitbutton}
            return render(request, 'unassignTaskV2.html',  context)

        else:
            return render(request, 'unassignTaskV2.html')


def companyReg(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    context = {'current_datetime': current_datetime}
    return render(request, 'companyReg.html', context)


def companyInfoSave(request):
    if request.method == 'POST':
        company_name = request.POST.get("company_name")
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")
        print(company_name)
        print(email)
        print(phonenumber)

        cursor = connection.cursor()
        # data = cursor.execute('create table abccc (id int auto_increment primary key, ticketaname varchar(50))')
        y = cursor.execute(
            "INSERT INTO support_portal_companyinfo (company_name, email, phonenumber) VALUES (%s, %s, %s)",
            [company_name, email, phonenumber])



        company_id =cursor.execute ('select id from support_portal_companyinfo where company_name= %s',[company_name])

        company_id = cursor.fetchall()
        print(company_id)
        for i in company_id:
            print(i[0])
        company_id = i[0]
        print(company_id)


        context = {'company_id': company_id}
        return render(request, 'userCreate.html', context)

        # return redirect(userCreate)


def dbAccess(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    cursor = connection.cursor()
    cursor.execute('select name from auth_group order by id ASC')
    get_group = cursor.fetchall()

    context = {'current_datetime': current_datetime, 'get_group': get_group}
    return render(request, 'dbaccess.html', context)


def DbTicketSaved(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        application_project_name = request.POST.get("application_project_name")
        access_environtment = request.POST.get("access_environtment")
        access_privilege_type = request.POST.get("access_privilege_type")
        access_Duaration = request.POST.get("access_Duaration")
        why_access_needed = request.POST.get("why_access_needed")
        approved_by = request.POST.get("approved_by")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        print(request_date)
        print(approval)
        print(application_project_name)
        print(access_environtment)
        print(access_privilege_type)
        print(access_Duaration)
        print(why_access_needed)
        print(approved_by)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team, application_project_name, access_environtment, access_privilege_type, access_Duaration, why_access_needed, approved_by) VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team, application_project_name, access_environtment, access_privilege_type, access_Duaration, why_access_needed, approved_by])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        messages.success(request, "Ticket entry successfully..!!")

        cursor.execute('select email from auth_group where name= %s', [team])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        teamEmail = email[0]
        print(f"TeamEmail" + teamEmail)

        team = teamEmail

        # if team == 'systems':
        #     team = 'ashif.faisal0@gmail.com'
        # elif team == 'TechOps':
        #     team = 'tech_ops@surecash.net'
        # elif team == 'DataTeam':
        #     team = 'data@surecash.net'

        latest_update=''
        _send_mail(task, employee_id, comment, id, team, creatoremail,latest_update)
        # if x:
        #     messages.success(request, "Ticket entry successfully..!!")
        #     return redirect('dbAccess')

        return render(request, 'sysnewticket.html')



def DBaccessRequestForm(request):
    currentdate = datetime.now()
    current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

    cursor = connection.cursor()
    cursor.execute('select name from auth_group order by id ASC')
    get_group = cursor.fetchall()

    context = {'current_datetime': current_datetime,'get_group': get_group}
    return render(request, 'DBaccessRequestForm.html', context)


def NewDbTicketSaved(request):
    if request.method == 'POST':
        employee_id = request.POST.get("employee_id")
        task = request.POST.get("task")
        comment = request.POST.get("comment")
        request_date = request.POST.get("request_date")
        approval = request.POST.get("approval")
        team = request.POST.get("team")
        application_project_name = request.POST.get("application_project_name")
        access_environtment = request.POST.get("access_environtment")
        access_privilege_type = request.POST.get("access_privilege_type")
        access_Duaration = request.POST.get("access_Duaration")
        why_access_needed = request.POST.get("why_access_needed")
        approved_by = request.POST.get("approved_by")
        print(team)
        print(employee_id)
        print(task)
        print(comment)
        print(request_date)
        print(approval)
        print(application_project_name)
        print(access_environtment)
        print(access_privilege_type)
        print(access_Duaration)
        print(why_access_needed)
        print(approved_by)
        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO support_portal_userprofile(employee_id, task, comment,request_date, approval, team, application_project_name, access_environtment, access_privilege_type, access_Duaration, why_access_needed, approved_by) VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [employee_id, task, comment, request_date, approval, team, application_project_name, access_environtment, access_privilege_type, access_Duaration, why_access_needed, approved_by])

        cursor.execute('select id from myappdb.support_portal_userprofile order by request_date DESC limit  1')
        thistuple = cursor.fetchall()
        for i in thistuple:
            print(i[0])

        id = i[0]
        print(id)

        cursor.execute('select email from auth_user where username= %s', [employee_id])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        creatoremail = email[0]
        print("creatoremailll" + creatoremail)

        cursor.execute('select email from auth_group where name= %s', [team])
        email = cursor.fetchall()
        for email in email:
            print(email[0])

        teamEmail = email[0]
        print(f"TeamEmail" + teamEmail)
        team = teamEmail

        latest_update=''
        _send_mail(task, employee_id, comment, id, team, creatoremail,latest_update)
        return render(request, 'newticket.html')


def tableFormate(request):
    return render(request, 'tableFormate.html')


def ticketDashBoard(request):
    return render(request, 'ticketDashBoard.html')


def UserRegForm(request):
    return render(request, 'UserRegForm.html')


def UserRegSave(request):
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        user_types = request.POST.get("user_types")
        access = request.POST.get("access")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        active="1"

        currentdate = datetime.now()
        current_datetime = currentdate.strftime("%Y-%m-%d %H:%M:%S")

        # form = createUserForm()
        # if request.method == 'POST':
        #     form = createUserForm(request.POST)
        #     if form.is_valid():
        #         form.save()
        #         if form.save():
        #             messages.success(request, "User Create Successfully..!!")
        #         return redirect('login')

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO auth_user (username, first_name,last_name, email, is_superuser,is_staff,is_active,date_joined, password) VALUES (%s,%s, %s,%s, %s, %s,%s,%s, %s)",
            [user_name,first_name,last_name, email, user_types,access,active,current_datetime, password2])

        return redirect('login')
        # return render(request, 'UserRegForm.html')


def CreateGroup(request):
    cursor = connection.cursor()
    cursor.execute('select * from auth_group order by id DESC')
    AllGroup = cursor.fetchall()
    print(AllGroup)

    context = {'AllGroup': AllGroup}
    return render(request, 'CreateGroup.html', context)
    #
    # return render(request, 'CreateGroup.html')


def UserAssignToTeam(request):
    if request.method == 'POST':
        user_id = request.POST.get("id")
        print(user_id)
        cursor = connection.cursor()
        cursor.execute('select username from auth_user where id= %s', [user_id])
        username = cursor.fetchall()
        print(username)

        cursor = connection.cursor()
        cursor.execute('select * from auth_group order by id asc')
        get_group = cursor.fetchall()

        context = {'username': username,'get_group': get_group}
        return render(request, 'UserAssignToTeam.html', context)

        # group_id='1'
        # cursor = connection.cursor()
        # x = cursor.execute(
        #     "INSERT INTO auth_user_groups(user_id, group_id) VALUES (%s, %s)",
        #     [lastCreatedUserId, group_id])
    # return render(request, 'UserAssignToTeam.html')


def UserAssignToTeamName(request):
    if request.method == 'POST':
        user_name = request.POST.get("username")
        group_id = request.POST.get("group_id")

        cursor = connection.cursor()
        cursor.execute('select id from auth_user where username= %s', [user_name])
        user_id = cursor.fetchall()
        print(user_id)
        for i in user_id:
            print(i[0])
        user_id = i[0]
        print(user_id)

        print(user_id)
        print(group_id)

        cursor = connection.cursor()
        x = cursor.execute(
            "INSERT INTO auth_user_groups(user_id, group_id) VALUES (%s, %s)",
            [user_id, group_id])
        if x:
            messages.success(request, "Team assign successfully..!!")
        else:
            messages.success(request, "Thanks! user already assigned this team..!!")

        return redirect('regview')
        # return render(request, 'UserAssignToTeam.html')



def UserDelete(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)

        cursor = connection.cursor()
        x = cursor.execute('DELETE FROM auth_user WHERE id= %s', [id])
        # cursor = connection.cursor()
        # cursor.execute('DELETE FROM auth_user_groups WHERE user_id= %s', [id])
        # x= cursor.execute ('DELETE auth_user, auth_user_groups FROM auth_user INNER JOIN auth_user_groups on auth_user_groups.user_id = auth_user.id and auth_user.id=%s',[id])



        if x:
            messages.success(request, "User Deleted Successfully..!!")


        return redirect('regview')



def CreateGroupSave(request):
    if request.method == 'POST':
        group_name = request.POST.get("group_name")
        group_email = request.POST.get("group_email")
        print(group_name)
        print(group_email)

        cursor = connection.cursor()
        y = cursor.execute(
            "INSERT INTO auth_group (name,email) VALUES (%s, %s)",
            [group_name,group_email])

        if y:
            messages.success(request, "Group Created Successfully..!!")
        return redirect('CreateGroup')



def GroupEdit(request):
    if request.method == 'POST':
        group_id = request.POST.get("id")
        print(group_id)
        cursor = connection.cursor()
        cursor.execute('select * from auth_group where id= %s', [group_id])
        group_name_id = cursor.fetchall()
        print(group_name_id)


        cursor = connection.cursor()
        cursor.execute('select * from auth_group order by id DESC')
        AllGroup = cursor.fetchall()
        print(AllGroup)

        context = {'group_name_id': group_name_id, 'AllGroup': AllGroup}
        return render(request, 'GroupEdit.html', context)

    # return render(request, 'GroupEdit.html')

def GroupEditSave(request):
    if request.method == 'POST':
        group_name = request.POST.get("group_name")
        group_id = request.POST.get("group_id")
        group_email = request.POST.get("group_email")
        print(group_name)
        print(group_id)
        print(group_email)

        cursor = connection.cursor()
        y = cursor.execute("UPDATE auth_group SET name= %s,email= %s WHERE id= %s", [group_name,group_email,group_id])
        if y:
            messages.success(request, "Group Edit Successfully..!!")
        return redirect('CreateGroup')


def GroupDelete(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        print(id)

        cursor = connection.cursor()
        x = cursor.execute('DELETE FROM auth_group WHERE id= %s', [id])
        if x:
            messages.success(request, "Group Deleted Successfully..!!")


        return redirect('CreateGroup')


def settings(request):
    user = request.user
    print(user)

    cursor = connection.cursor()
    cursor.execute('select * from auth_user where username = %s',[user])
    user_id = cursor.fetchall()

    print(user_id)

    context = {'user_id': user_id}
    return render(request, 'settings.html',context)


def userManagementPage(request):

    return render(request, 'userManagementPage.html')


def changePassword(request):
    fm = PasswordChangeForm(request.user)
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            if fm.save():
                messages.success(request, "Changed Successfully..!!")
            return redirect('login')
    context = {'form': fm}
    return render(request, 'changePassword.html', context)


def changePasswordUser(request):
    fm = PasswordChangeForm(request.user)
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            if fm.save():
                messages.success(request, "Changed Successfully..!!")
            return redirect('login')
    context = {'form': fm}
    return render(request, 'changePasswordUser.html', context)


def userCreate(request):

    form = createUserForm()
    print(form)

    # print(f("id"+company_id))

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            if form.save():
                messages.success(request, "User Create Successfully..!!")
            return redirect('login')

    cursor = connection.cursor()
    cursor.execute('select id from auth_user order by id DESC limit  1 ')
    last_user = cursor.fetchall()
    print(last_user)
    for i in last_user:
        print(i[0])
    lastCreatedUserId = i[0]
    print(lastCreatedUserId)


    group_id = request.POST.get("group_id")
    print(group_id)

    # group_id='1'
    # cursor = connection.cursor() 
    # x = cursor.execute(
    #     "INSERT INTO auth_user_groups(user_id, group_id) VALUES (%s, %s)",
    #     [lastCreatedUserId, group_id])

    cursor = connection.cursor()
    cursor.execute('select * from auth_user order by id DESC')
    # cursor.execute('select * from auth_user')
    Alluser = cursor.fetchall()
    print(Alluser)

    context = {'form': form, 'Alluser': Alluser}
    return render(request, 'userCreate.html', context)


def CompanyCreatePage(request):
    return render(request, 'CompanyCreatePage.html')


def copy_userCreate(request):
    return render(request, 'copy_userCreate.html')

def userRegistration(request):
    form = createUserForm()

    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            if form.save():
                messages.success(request, "User Create Successfully..!!")
            return redirect('regview')

    return render(request, 'userRegistration.html')


def AssignedTask(request):
    user = request.user
    print(user)

    cursor = connection.cursor()
    cursor.execute('SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE maker1= %s ORDER BY request_date DESC', [user])
    data = cursor.fetchall()

    context = {'data': data}
    return render(request, 'AssignedTask.html', context)


def OwnTask(request):
    user = request.user
    print(user)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT *,datediff(etd,current_date) as pending_days FROM support_portal_userprofile WHERE employee_id= %s ORDER BY request_date DESC', [user])
    data = cursor.fetchall()

    context = {'data': data}
    return render(request, 'OwnTask.html', context)


def profileEdit(request):
    if request.method == 'POST':
        user_id = request.POST.get("id")
        print(user_id)
        cursor = connection.cursor()
        cursor.execute('select * from auth_user where id= %s', [user_id])
        user_info = cursor.fetchall()
        print(user_info)


        # cursor = connection.cursor()
        # cursor.execute('select * from auth_user order by id DESC')
        # AllGroup = cursor.fetchall()
        # print(AllGroup)

        context = {'user_info': user_info}
        return render(request, 'profileEdit.html',context)


def profileUpdate(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        userid = request.POST.get("id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        print(username)
        print(userid)
        print(first_name)
        print(last_name)
        print(email)

        cursor = connection.cursor()
        y = cursor.execute("UPDATE auth_user SET username= %s,email= %s,first_name= %s,last_name= %s WHERE id= %s", [username, email, first_name,last_name,userid ])
        if y:
            messages.success(request, "User Edit Successfully..!!")
        #return redirect('profileUpdate')
        return render(request, 'profileUpdate.html')


def importLink(request):
    return render(request, 'importLink.html')