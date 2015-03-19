from django.shortcuts import render
from django.http import HttpResponse
import os
from backend import ask_db, db_check

PATH_STATIC = os.getcwd()+'/ask/static/ask/xls/'

def read_xls(path):
    """
    Read the DB's xls file & export the 2-dimension list recording the table
    """
    table = []
    f_in = open(path, 'r')
    line = f_in.readline()
    while line:
        row = []
        info = line.strip('\r\n').split('\t')
        for tip in info:
            row.append(tip)
        table.append(row)
        line = f_in.readline()

    return table

def console(request):
    """
    Define the console view behave
    """
    context = {}
    table = []
    table_flag = False
    distinct_flag = True
    tip_count = ''
    default_domain = 'systems'
    DB = 'customer.db'

    if request.method == 'POST':
        distinct_filter = request.POST['filter']
        domain = request.POST['domain']      
        default_domain = domain
        table_name = distinct_filter+"_"+domain+".xls"
        output_path = PATH_STATIC+table_name

        #create db file
        if distinct_filter == 'all':
            distinct_flag = False
            ask_db.ask_db(DB, domain, output_path)
        elif distinct_filter == 'distinct':
            distinct_flag = True
            db_check.main() #update distinct customers
            ask_db.ask_db_distinct(DB, domain, output_path)

        #read db file & display
        table = read_xls(PATH_STATIC+table_name)
        if not table == []:
            del table[-1]
            tip_count = table[-1][0][1:-1].replace('rows', 'records')
            del table[-1]

    if not table == []:
        table_flag = True
    context={'table_flag':table_flag, 'default_domain':default_domain, \
    'distinct_flag':distinct_flag, 'table':table, 'tip_count':tip_count}
    return render(request, "ask/console.html", context)
