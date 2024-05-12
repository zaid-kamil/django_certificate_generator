from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from .models import Dataset, Certificate, Report
from .forms import UploadForm, CertificateForm, ReportForm
from .certifcate import write_name
from .blockchain import Block, Blockchain, generate_unique_code
from .certifcate import write_name   
import datetime as date
import os
import pandas as pd
from django.contrib import messages

# Create your views here.
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('list')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def list_files(request):
    uploads = Dataset.objects.filter(user=request.user)
    return render(request, 'list.html', {'uploads': uploads})

def view_file(request, id):
    upload = Dataset.objects.get(id=id)
    if upload.file.name.endswith('.xlsx'):
        df = pd.read_excel(upload.file.path)
        return render(request, 'view.html', {'upload': upload, 'data': df.to_html(
            classes='table table-bordered table-striped table-hover text-center'
        )})
    else:
        messages.error(request, 'Invalid file format')
        return redirect('list')


def delete_file(request, id):
    upload = Dataset.objects.get(id=id)
    upload.delete()
    return redirect('list')

from datetime import datetime

@login_required
def generate_certificate(request, dataid):
    upload = Dataset.objects.get(id=dataid)
    df = pd.read_excel(upload.file.path)
    # make all columns lowercase
    df.columns = map(str.lower, df.columns)
    # get last generated certificate
    last_certificate = Certificate.objects.filter(user=request.user).last()
    previous_hash = last_certificate.hash if last_certificate else "0"
    # certificates = Certificate.objects.filter(user=request.user)
    for index, row in df.iterrows():
        name = row['name']
        course = row['course']
        date = row['date']
        if Certificate.objects.filter(name=name, course=course).exists():
            print(f'Certificate for {name} already exists')
            continue
        hash = generate_unique_code(name, course, date)
        certificate = Certificate(user=request.user, name=name, course=course, date=datetime.now(), dataset=upload, hash=hash, previous_hash=previous_hash)
        certificate.save()
        # certificate id 
        certificate_id = certificate.id # get the certificate id
        print(f'id: {certificate_id}')
        file = write_name(name, course, date, hash, id= certificate_id)
        certificate.file = file
        certificate.save()
        print(f'Certificate generated for {name}')
    return redirect('list_cert')



   

def list_certificates(request):
    certificates = Certificate.objects.filter(user=request.user)
    for certificate in certificates:
        certificate.url = "/static/"+certificate.file.url.split('/assets/')[-1]
    return render(request, 'list_cert.html', {'certificates': certificates})

from PIL import Image
def download_certificate(request, id):
    certificate = Certificate.objects.get(id=id)
    filename = "assets/"+ certificate.file.url.split('/assets/')[-1]
    # convert to pdf
    img = Image.open(filename)
    ext = filename.split('.')[-1]
    img.save(filename.replace(ext, 'pdf'), 'PDF')
    filename = filename.replace(ext, 'pdf')
    print(filename)
    response = HttpResponse(open(filename, 'rb').read())
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filename)
    return response

def view_certificate(request, id):
    certificate = Certificate.objects.get(id=id)
    certificate.url = "/static/"+certificate.file.url.split('/assets/')[-1]
    return render(request, 'view_certificate.html', {'certificate': certificate})

def verify_certificate(request):
    if request.method == 'POST':
        hash = request.POST['hash']
        certificate = Certificate.objects.filter(hash=hash).first()
        if certificate:
            certificate.url = "/static/"+certificate.file.url.split('/assets/')[-1]
            return render(request, 'verify.html', {'certificate': certificate, 'status': 'Certificate found'  })
        else:
            return render(request, 'verify.html', {'status': 'Certificate not found'})
    return render(request, 'verify.html')

def delete_certificate(request, id):
    certificate = Certificate.objects.get(id=id)
    certificate.delete()
    messages.success(request, 'Certificate deleted successfully')
    return redirect('list_cert')

def report_changes(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            messages.success(request, 'Report submitted successfully')
            return redirect('report')
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})

def list_reports(request):
    reports = Report.objects.all()
    for report in reports:
        certificate = Certificate.objects.filter(id=report.certificate_id).first()
        if certificate:
            report.url = "/static/"+certificate.file.url.split('/assets/')[-1]
            report.cid = certificate.id
        else:
            report.url = None
            report.cid = None
    return render(request, 'report_list.html', {'reports': reports})

def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    messages.success(request, 'Report deleted successfully')
    return redirect('list_reports')