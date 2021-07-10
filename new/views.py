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
    result = []
    for i in data:
        result.append(str(i.user_name) + str(i.password))
    #print(result)
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
                    data = Usermodel.objects.all()
                else:
                    data = Usermodel.objects.filter(user_type=type)
                return render(request, 'result.html',{'data':data,'type':type,'pri':pri})
            else:
                return render(request, '401.html')
        except:
            user_name = request.POST['users']
            pri_list = request.POST.getlist('d[]')
            #print(user_name)
            #print(pri_list)
            pri_list = str(pri_list)[1:-1]
            #print(pri_list,'   hj')
            obj = Usermodel.objects.get(user_name=user_name)
            s1 = obj.pri
            s = ''
            if obj.pri and pri_list:
                s += obj.pri
                s += ','
                s += pri_list
                obj.pri = s
                
                #obj.save()
            else:
                #s += obj.pri
                pass
            print(s)
                #obj.save()
            #s2 = str(str(set(str(s1)) + str(pri_list)))
            
            '''print(pri_list,'    from check')
            st = ''
            for i in pri_list:
                st += i
                print(i)
            fi = s1
            if st:
                fi += ','
                fi += st
            print(s1 + st, ' njekw')
            print(st)
            print(fi)'''
            
            #obj.pri = str(result)
            obj.save()
        
    return render(request, 'index.html')

def error_404(request , exception):
    return render(request , '404_page.html')

def check():
    pass

def error_500(request):
    return render(request , '500.html')