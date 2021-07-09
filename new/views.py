from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from new.forms import UserForm
from new.models import Usermodel
from django import forms
from .forms import UserRegistration, PriForm
from .models import Usermodel, Privillages
from django.db import connection

#to add pri
def add_pri(request):
    print(request.session.get('user'),'          bjkebskjb')
    if request.session.get('user') == 'nirmal':
        
        if request.method == 'POST':
            fm = PriForm(request.POST)
            if fm.is_valid():
                fm.save()
                fm = PriForm()
                stud = Privillages.objects.all()


        else:

            fm = PriForm()
        stud = Privillages.objects.all()
    else:
        return HttpResponse('<h1>You are not authenticate</h1>')


    return render(request, 'add_pri.html',{'form' : fm,'stu' : stud})  

#This will add items and show all the items
def add_show(request):
    if request.session.get('user') == 'nirmal':
        if request.method == 'POST':
            fm = UserRegistration(request.POST)
            if fm.is_valid():
                fm.save()
                fm = UserRegistration()
                stud = Usermodel.objects.all()


        else:

            fm = UserRegistration()
        stud = Usermodel.objects.all()


        return render(request, 'addandshow.html',{'form' : fm,'stu' : stud})
    else:
        return HttpResponse('<h1>You are not authenticate</h1>')

#delete pri
def delete_pri(request,id):
    if request.method == 'POST':
        pi = Privillages.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/crudpri')
# This function will delete

def delete_data(request,id):
    if request.method == 'POST':
        pi = Usermodel.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/crud')


#update pri
def update_pri(request,id):
    if request.method == 'POST':
        pi = Privillages.objects.get(pk=id)
        fm = PriForm(request.POST , instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('addpri')
    else:
        pi = Privillages.objects.get(pk=id)
        fm = PriForm(instance=pi)
    return render(request,'update_pri.html', {'form' : fm})    
#This will update
def update_data(request,id):
    if request.method == 'POST':
        pi = Usermodel.objects.get(pk=id)
        fm = UserRegistration(request.POST , instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Usermodel.objects.get(pk=id)
        fm = UserRegistration(instance=pi)
    return render(request,'update.html', {'form' : fm})


def validate(request):
    #request.session['user'] = m.id
    data = Usermodel.objects.all()#usernamepass
    pri = Privillages.objects.all()
    pri_data = []
    for i in pri:
        pri_data.append(i.privillages_name)
    
    result = []
    for i in data:
        result.append(str(i.user_name) + str(i.password))
    #print(result)
    obj = Usermodel.objects.get(user_type='admin')
    obj.pri = ''
    obj.pri = pri_data
    flag = True
    if request.method == 'POST':
        
        #print('user is ',request.POST['users'])
        try:
            request.session['user'] = request.POST['username']
            if str(request.POST['username']) + str(request.POST['pass']) in result:
                type = ''
                for i in Usermodel.objects.filter(user_name=request.POST['username']):
                    type = i.user_type
                print(type)
                if type == 'admin':
                    data = Usermodel.objects.exclude(user_type=type)
                else:
                    data = Usermodel.objects.filter(user_type=type)
                return render(request, 'result.html',{'data':data,'type':type,'pri':pri})
            else:
                return render(request, 'result.html',{'ans':'User Name or Passwor is Invailid'})
        except:
            flag = False
            user_name = request.POST['users']
            pri_list = request.POST.getlist('d[]')
            #print(user_name)
            #print(pri_list)
            obj = Usermodel.objects.get(user_name=user_name)
            obj.pri = ''
            obj.pri = pri_list
            obj.save()
    #if flag: 
    
    return render(request, 'index.html')    