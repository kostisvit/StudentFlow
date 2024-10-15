from django.http import HttpResponse
from .resources import SubscriptionResource, StudentExportResource
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Subscription export
@login_required
def Export_data_subscription(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        #user = request.user
        student_resource = SubscriptionResource()

        dataset = student_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Subscrioptions_list.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="Subscrioptions_list.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="Subscrioptions_list.xls"'
            return response   

    return render(request, 'app/student/subscriptions_export.html')



@login_required
def Student_Export_data(request):
    if request.method == 'POST':

        file_format = request.POST['file-format']
        #user = request.user
        student_resource = StudentExportResource(request=request)

        dataset = student_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Student_list.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="Student_list.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="Student_list.xlsx"'
            return response   

    return render(request, 'app/student/student_export.html')