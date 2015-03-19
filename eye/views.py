from django.shortcuts import render, get_object_or_404
from eye.models import Log, Domain
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
from backend import interface
import time
import commands

PATH_STATIC = os.getcwd()+'/eye/static/eye/'
PATH_IMAGE = 'eye/image/'

def seconds_to_str(seconds):
    """
    Transfer input seconds to formatted string: 2015-02-09 21:16:01
    """
    return time.strftime("(%Y-%m-%d) %H:%M:%S", time.localtime(seconds))

def str_to_seconds(time_str):
    """
    Transfer input seconds to formatted string: 2015-02-09 21:16:01
    """
    return int(time.mktime(time.strptime(time_str, "(%Y-%m-%d) %H:%M:%S")))

def index(request):
    """
    Begin Page with 3 entrances: Import Log, Select Domain, Draw
    """
    return render(request, "eye/index.html")

def log_index(request, duplicated_flag=False, path_null_flag=False):
    """
    View log list imported & add
    """
    log_list = Log.objects.order_by('-pub_date')
    context = {'log_list':log_list, 'duplicated_flag':duplicated_flag, 'path_null_flag':path_null_flag}
    return render(request, "eye/log_index.html", context)

def log_add(request):
    """
    Add log & transfer to .pd file according to input message
    """
    duplicated_flag = False
    path_null_flag = False

    if not request.method == 'POST':
        print 'impossible to here, log_add in not POST'
        return HttpResponseRedirect(reverse('eye:log_index'))
    path = request.POST['log_path']
    name = request.POST['log_name']
    key = request.POST['category_key']
    filter_key = request.POST['filter_key']

    index_time = request.POST['index_time']
    index_type = request.POST['index_type']
    index_sent = request.POST['index_sent']
    index_received = request.POST['index_received']
    index_latency = request.POST['index_latency']

    if not os.path.exists(path):
        path_null_flag = True

    elif not path == "":
        if len(Log.objects.filter(log_name=name)) == 0:
            new_log = Log(log_path=path,log_name=name,category_key=key,pub_date=timezone.now())
            new_log.index_time = index_time
            new_log.index_type = index_type
            #Special tackle when index_sent == ''
            if index_sent == '':
                index_sent = '-1'
            new_log.index_sent = index_sent
            new_log.index_received = index_received
            new_log.index_latency = index_latency
            new_log.save()

            #create corrsponding .pd file in /static/ask/pd_file
            pd_path = PATH_STATIC+'pd_file/'+name+'.pd'
            interface.export_pd(path, key, pd_path, index_time, index_type, \
                index_sent, index_received, index_latency, filter_key)

        else:
            duplicated_flag = True

#   return log_index(request, duplicated_flag, path_null_flag)
    return HttpResponseRedirect(reverse('eye:log_index'))

def domain_index(request):
    """
    View selected domain & add
    """
    log_list = Log.objects.order_by('-pub_date')
    imported_log_name_list = [log.log_name for log in log_list]
    domain_list = Domain.objects.order_by('-pub_date')

    context = {'imported_log_name_list':imported_log_name_list, 'domain_list':domain_list}

    return render(request, 'eye/domain_index.html', context)

def domain_add(request):
    """
    Add new domain & calculate its scale range
    """
    if not request.method == 'POST':
        print 'impossible to here, log_add in not POST'
        return HttpResponseRedirect(reverse('eye:domain_index'))

    object_log = Log.objects.get(log_name=request.POST['log_name'])
    if request.POST['category_name'] == 'common':
        category = 'non'
    else:
        category = object_log.category_key
    type_ = request.POST['type_name']

    new_domain_name = object_log.log_name+"_"+category+"_"+type_
    if not len(Domain.objects.filter(domain_name=new_domain_name)):   # not existed then add
        new_domain = Domain(pd_name=object_log,category_name=category,type_name=type_,pub_date=timezone.now())
        new_domain.save()

        #run the statistic & save in this new_domain
        pd_path = PATH_STATIC+'pd_file/'+object_log.log_name+'.pd'
        result_set = interface.export_domain(pd_path, category, type_)
        new_domain.time_min = result_set[1].split(':')[1]
        new_domain.time_max = result_set[1].split(':')[2]
        if not new_domain.type_name == 'DELETE':
            new_domain.size_min = result_set[2].split(':')[1]
            new_domain.size_max = result_set[2].split(':')[2]
        new_domain.latency_min = result_set[3].split(':')[1]
        new_domain.latency_max = result_set[3].split(':')[2]
        new_domain.total = result_set[4].split(':')[1]
        new_domain.domain_name = new_domain_name
        new_domain.save()

    return HttpResponseRedirect(reverse('eye:domain_index'))

def draw_index(request):
    """
    Plot chart according to specific range
    """
    imported_domain_list = Domain.objects.order_by('-pub_date')

    context = {'imported_domain_list':imported_domain_list}
    return render(request, 'eye/draw_index.html',context)

def draw(request):
    """
    Show the selected domain's range
    """
    show_flag = False
    delete_flag = False
    if request.method == "POST":
        show_flag = True
        domain_selected_name = request.POST['domain_selected']
        domain = Domain.objects.get(domain_name=domain_selected_name)
        imported_domain_list = Domain.objects.order_by('-pub_date')
        if domain.type_name == 'DELETE':
            delete_flag = True  # DELETE needs to mask "size scale" & "size range" 

        text = {'time_min':seconds_to_str(domain.time_min),'time_max':seconds_to_str(domain.time_max),\
        'size_min':round(domain.size_min,2),'size_max':round(domain.size_max,2),\
        'latency_min':round(domain.latency_min,2), 'latency_max':round(domain.latency_max,2),\
        'delete_flag':delete_flag,'domain_name':domain.domain_name,'total':domain.total,'id':domain.id}

        context = {'show_flag':show_flag,'imported_domain_list':imported_domain_list,'text':text}
        return render(request, 'eye/draw.html', context)

def get_input_range(request, domain, tip):
    """
    Return the suitable format for Plot: min,max
    """
    left = request.POST[tip+'_min']
    right = request.POST[tip+'_max']
    if left == '' and right == '':
        return ''

    if tip == 'time':
        bottom = domain.time_min
        top = domain.time_max
        if left == '':
            left = str(bottom)
        else:
            left = str(str_to_seconds(left))
        if right == '':
            right = str(top)
        else:
            right = str(str_to_seconds(right))
        if left == str(bottom) and right == str(top):
            return ''
    elif tip == 'size':
        bottom = round(domain.size_min,2)
        top = round(domain.size_max,2)
        if left == '':
            left = str(bottom)
        if right == '':
            right = str(top)
        if float(left) == bottom and float(right) == top:
            return ''
    elif tip == 'latency':
        bottom = round(domain.latency_min,2)
        top = round(domain.latency_max,2)
        if left == '':
            left = str(bottom)
        if right == '':
            right = str(top)
        if float(left) == bottom and float(right) == top:
            return ''
    else:
        return ''

    return left+","+right
    
def draw_plot(request, domain_id):
    """
    Plot the chart according to the input range
    """
    show_flag = False
    delete_flag = False
    size_range = ''
    if request.method == "POST":
        show_flag = True
        imported_domain_list = Domain.objects.order_by('-pub_date')
        domain = Domain.objects.get(id=domain_id)
        if domain.type_name == 'DELETE':
            delete_flag = True  # DELETE needs to mask "size scale" & "size range"
        #export .refine file according to input range
        x_ordinate = request.POST['x_ordinate']
        y_ordinate = request.POST['y_ordinate']
        y_min = request.POST['y_min']
        y_max = request.POST['y_max']

        time_range = get_input_range(request, domain, 'time')
        if not delete_flag:
            size_range = get_input_range(request, domain, 'size')
        latency_range = get_input_range(request, domain, 'latency')
        refine_path_directory = PATH_STATIC+'refine_file/'

        pd_path = PATH_STATIC+'pd_file/'+domain.pd_name.log_name+'.pd'
        dimension = x_ordinate+','+y_ordinate

        file_name = os.path.splitext(os.path.basename(pd_path))[0]
        diff = "."+domain.category_name+"."+domain.type_name+"."+dimension+"("+time_range+"_"+size_range+"_"+latency_range+")"
        refine_file_name = file_name+diff+".refine"
        output_path_image = PATH_STATIC+'image/'
        pic_name = file_name+diff+"("+y_min+","+y_max+")"+".png"

        # no cache picture & no cache .refine file then create .refine file
        if not os.path.exists(output_path_image+pic_name) and not os.path.exists(refine_path_directory+refine_file_name):
            refine_file_name = interface.export_refine(pd_path,domain.category_name,domain.type_name,dimension,\
                time_range,size_range,latency_range,refine_path_directory)
        
#       print refine_path_directory+refine_file_name
        x_label_tip = ''
        y_label_tip = ''
        if x_ordinate == 'time':
            x_label_tip = 'time'
        if y_ordinate == 'time':
            y_label_tip = 'time'

        # no cache picture then create picture
        if not os.path.exists(output_path_image+pic_name):
            pic_name = interface.export_plot("scatter", refine_path_directory+refine_file_name, \
                output_path_image, x_label_tip, y_label_tip, y_min, y_max)
        
        pic = PATH_IMAGE+pic_name
         
        text = {'time_min':seconds_to_str(domain.time_min),'time_max':seconds_to_str(domain.time_max),\
        'size_min':round(domain.size_min,2),'size_max':round(domain.size_max,2),\
        'latency_min':round(domain.latency_min,2), 'latency_max':round(domain.latency_max,2),\
        'delete_flag':delete_flag,'domain_name':domain.domain_name,'total':domain.total,'id':domain.id}

    context = {'imported_domain_list':imported_domain_list,'show_flag':show_flag, "pic":pic, 'text':text}
    return render(request, 'eye/draw_plot.html', context)

def back_to_menu(request):
    """
    Return to Menu 
    """
    return HttpResponseRedirect(reverse('eye:index'))

def pic_index(request):
    """
    Display all the Pics for bundle show
    """
    pic_flag = False
    cmd = "ls %s | grep .png" % (PATH_STATIC+'image/')
    status, output = commands.getstatusoutput(cmd)
    pic_list = output.split('\n')
    context = {'pic_list':pic_list,'pic_flag':pic_flag}
    return render(request,'eye/pic_index.html', context)

def pic_show(request):
    """
    Show the Pics selected
    """
    pic_flag = False
    context = {}
    pics = []

    cmd = "ls %s | grep .png" % (PATH_STATIC+'image/')
    status, output = commands.getstatusoutput(cmd)
    pic_list = output.split('\n')
    
    if request.method == 'POST':
        pics = request.POST.getlist('pics')
        
        if len(pics) > 0:
            pic_flag = True
            pics_selected = []
            for pic in pic_list:
                if pic in pics:
                    pics_selected.append(True)
                else:
                    pics_selected.append(False)
            for i in range(len(pic_list)):
                pic_list[i] = {'name':pic_list[i],'selected':pics_selected[i]}
            
            for i in range(len(pics)):
                pics[i] = PATH_IMAGE+pics[i]
        
        context = {'pic_flag':pic_flag,'pics':pics,'pic_list':pic_list}

    return render(request,'eye/pic_index.html', context)

def clear_pic(request):
    """
    Clear the cache for pic & .refine files
    """
    if request.method == 'POST':
        delete_list = []
        refine_list = os.listdir(PATH_STATIC+'refine_file')
        for tip in refine_list:
            if '.refine' in tip:
                delete_list.append(PATH_STATIC+'refine_file/'+tip)
        pic_list = os.listdir(PATH_STATIC+'image')
        for tip in pic_list:
            if '.png' in tip:
                delete_list.append(PATH_STATIC+'image/'+tip)

        for tip in delete_list:
            if os.path.isfile(tip):
                os.remove(tip)
        Domain.objects.all().delete()

    return HttpResponseRedirect(reverse('eye:index'))

def clear_pd(request):
    """
    Clear the cache for .pd files
    """
    if request.method == 'POST':
        delete_list = []
        pd_list = os.listdir(PATH_STATIC+'pd_file')
        for tip in pd_list:
            if '.pd' in tip:
                delete_list.append(PATH_STATIC+'pd_file/'+tip)

        for tip in delete_list:
            if os.path.isfile(tip):
                os.remove(tip)
        Log.objects.all().delete()

    return HttpResponseRedirect(reverse('eye:index'))









