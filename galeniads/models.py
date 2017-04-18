from django.db import models
from django.utils import timezone
import os

def get_upload_path_folder(instance, filename):
    upload_dir = os.path.join('folder', "%s" % instance.name, 'file_template')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

def get_upload_path_folder_template(instance, filename):
    upload_dir = os.path.join('folder', "%s" % instance.name, 'file_template')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

def get_upload_path_folder_file(instance, filename):
    upload_dir = os.path.join('folder', "%s" % instance.folder.name, 'file')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.name

class Account(models.Model):
    name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=50, null=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_from = models.DateTimeField(default=timezone.now)
    file_template =  models.FileField(upload_to=get_upload_path_folder_template)
    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=200, null=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_from = models.DateTimeField(default=timezone.now)
    src = models.FileField(upload_to=get_upload_path_folder_file)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
