from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from django import forms
from .models import *
import os
from django.conf import settings
from django.http import HttpResponse


# Additional function
def file_checker (file1, file2):
    #check the extension of file
    filename1, extension1 = file1.split(".", 1)
    filename2, extension2 = file2.split(".", 1)
    if (extension1 != extension2):
        return False
    else:
        return True

def authencticate_user(username, password):
    users = Account.objects.all()
    for user in users:
        if user.name == username and user.password == password:
            return True
    return False

def custom_redirect(url_name, *args, **kwargs):
    from django.core.urlresolvers import reverse
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

# View controller
def find_role_pk(role_name):
    roles = Role.objecst.all()
    for role in roles:
        if (role.name == role_name):
            return role
    return -1

def find_user_pk(username):
    users = Account.objects.all()
    for user in users:
        if (user.name == username):
            return user.id
    return -1

def index(request):
    template = 'galeniads/login.html'
    return render(request, template)

def home(request, id):
    template = 'galeniads/home.html'
    folders = Folder.objects.filter(owner=id)
    files = []
    folder_id = -1
    return render(request, template, {'folders' : folders, 'files' : files, 'user_id': id, 'folder_id': folder_id})

def register(request):
    #Still Dummy
    template = 'galeniads/register.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        #Saving the Account
        a = Account()
        a.name = username
        a.password = password
        role = get_object_or_404(Role, pk=1)
        a.role = role
        a.first_name = first_name
        a.last_name = last_name
        a.save()
        return redirect('galeniads:index')
    return render(request, template)

def login(request):
    template ='galeniads/login.html'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("test")
        if authencticate_user(username, password):
            id = find_user_pk(username)
            print(id)
            return redirect('galeniads:home', id=id)
        else:
            return redirect('galeniads:index')
    return render(request, template)

def account_manager(request):
    accounts = Account.objecst.all()
    template = 'galenidads/account_manager.html'
    return render(request, template, {'accounts': account})

def add_folder(request, id):
    template ='galeniads/home.html'
    if request.method == 'POST':
        name = request.POST['folder_name']
        file = request.FILES['file']
        owner = get_object_or_404(Account, pk=id)

        #create new folder
        f = Folder()
        f.name = name
        f.file_template = file
        f.owner = owner
        f.save()
        return redirect('galeniads:home', id=id)
    return render(request, template)

def add_file(request, id, pk):
    template ='galeniads/home.html'
    folder = get_object_or_404(Folder, pk=pk)
    file_template = folder.file_template
    user = get_object_or_404(Account, pk=id)
    if request.method == 'POST':
        src = request.FILES['file']
        if (file_checker(file_template.name, src.name)):
            #create file
            fl = File()
            fl.src = src
            fl.name = src.name
            fl.folder = folder
            fl.owner = user
            fl.save()
            return redirect('galeniads:view_file_in_folder', id=id, pk=pk)
        else:
            return redirect('galeniads:home', id=id)
    return render(request, template)

def download_file(request, id, pk, file_id):
    folder = get_object_or_404(Folder, pk=pk)
    file = get_object_or_404(File, pk=file_id)
    print(file)
    file_src = str(file.src)
    file_path = os.path.join(file_src)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return redirect('galeniads:home', id=id)
def edit_folder(request, id, pk):
    folder = get_object_or_404(Folder, pk=pk)
    if request.method == 'POST':
        folder.name = request.POST['folder_name_editted']
        folder.file_template = request.FILE['file_editted']
        folder.save()
        return redirect('galeniads:view_file_in_folder', id=id, pk=pk)

def view_file_in_folder(request, id, pk):
    template = 'galeniads/folder_views.html'
    user_id = id
    user = get_object_or_404(Account, pk=id)
    folder = get_object_or_404(Folder, pk=pk)
    files = File.objects.filter(folder=folder)
    folders = Folder.objects.filter(owner=id)
    return render(request, template, {'folders' : folders, 'current_folder' : folder, 'files' : files, 'user_id': user_id, 'folder_id': pk, 'current_user': user})
