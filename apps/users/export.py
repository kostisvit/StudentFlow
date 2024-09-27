from django.http import HttpResponse,JsonResponse
from .resources import UserResource
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Members export
@login_required
def Staff_export(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        user = request.user
        member_resource = UserResource()
        member_resource.user = user
        dataset = member_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Staff_list.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="Staff_list.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Staff_list.xls"'
            return response   

    return render(request, 'app/staff/staff_export.html')