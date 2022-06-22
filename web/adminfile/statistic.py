from django.shortcuts import render
from web.models import *
from web.adminfile.context import *
from django.contrib.auth.decorators import login_required
from web.decorators import *
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import TruncDate

class StatisticAdmin:
    @login_required(login_url='signin')
    @checkadmin
    def statistic(request):
        if 'date_start' in request.GET and 'date_end' in request.GET:
            date_start = request.GET['date_start']
            date_end = request.GET['date_end']
            metrics = {
                            'order': Count('order_id'), 
                            'turnover': Sum('order_totalprice')
                        }
            result = Order.objects.all().filter(order_time__date__gte=date_start,order_time__date__lte=date_end).annotate(time=TruncDate('order_time')).order_by('time').values('time').annotate(**metrics)
            totalturnover = totalorder = 0.0
            for item in result:
                totalturnover += item.get('turnover')
                totalorder += item.get('order')
            # totalresult = Order.objects.all().filter(order_time__date__gte=date_start,order_time__date__lte=date_end).annotate(turnover=Sum('order_totalprice')).order_by('turnover').values('turnover')
            # print(totalresult)
        return render(request, 'admin/statistic.html', locals())