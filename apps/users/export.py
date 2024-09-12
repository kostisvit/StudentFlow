from django.http import HttpResponse,JsonResponse
#from .resources import MemberResource
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Members export
@login_required
def Export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        user = request.user
        member_resource = MemberResource()
        member_resource.user = user
        dataset = member_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Members_list.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="Members_list.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Members_list.xls"'
            return response   

    return render(request, 'app/export.html')