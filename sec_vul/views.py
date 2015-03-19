from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os
from backend import ask_db_sec_vul, sec_plot
import re

DB_PATH = '/var/security_vulnerability/vulnerability_db'
PATH_STATIC = os.getcwd()+'/sec_vul/static/sec_vul/'
PATH_IMAGE = 'sec_vul/panel/'

def get_specific_column_distinct(table,column):
    """
    Return the list of Hotfix
    """
    set_tmp = set()
    lst = ask_db_sec_vul.read_db(DB_PATH,table,column)
    for tip in lst:
        tip = list(tip)[0]
        if tip == '':
            continue
        set_tmp.update(tip.split())
    lst = list(set_tmp)
    lst.sort(reverse=True)
    return lst

def search_noplan():
    """
    Display all the items No plan to fix, when the cves is '', just replace by name column
    """
    table_NP = []
    result_list_NP = []

    result_list_original = ask_db_sec_vul.read_db_np(DB_PATH)
    for raw in result_list_original:
        name = raw[0]
        cves = raw[1].split('\n')
        level = raw[2]
        justification = raw[3]

        if raw[1] == '':
            cves = [name]
        if level == 'H':
            level = 'High'
        elif level == 'M':
            level = 'Medium'
        elif level == 'L':
            level = 'Low'  
        else:
            level = ''

        for cve in cves:
            row = [cve,level,justification]
            if row in result_list_NP:
                continue
            else:
                result_list_NP.append(row)

    for raw in result_list_NP:
        if not raw in table_NP:
            table_NP.append(list(raw))

    return table_NP


def each_search(searchme):
    """
    Tackle each element search job
    """
    table = []
    table_HP = []
    table_RP = []
    table_NP = []
    result_list = []
    result_list_HP = []
    result_list_RP = []
    result_list_NP = []

    #Judge the search domain: CVE, HF, Release
    domain_flag = 'CVE'
    if 'HF' in searchme and searchme.index('HF') == 0:
        domain_flag = 'HF'
    elif '.' in searchme:
        domain_flag = 'Release'

    if domain_flag == 'CVE':
        result_list_original = ask_db_sec_vul.read_db_by_like(DB_PATH, searchme)
    elif domain_flag == 'HF':
        result_list_original = ask_db_sec_vul.read_db_by_like_HF(DB_PATH, searchme)
    elif domain_flag == 'Release':
        result_list_original = ask_db_sec_vul.read_db_by_like_Release(DB_PATH, searchme)

    # split multiple cves
    for raw in result_list_original:
        if raw[0] == '':
            continue
        cves = raw[0].split('\n')
        level = raw[1]
        hotfix = raw[2]
        release = raw[3]
        hotfix_st = raw[4]
        release_st = raw[5]
        justification = raw[6]
        if hotfix_st == 'F' or release_st == 'F':
            status = 'F'
        elif hotfix_st == 'NP' and release_st == 'NP':
            status = 'NP'
        elif hotfix_st == 'P':
            status = 'HP'
        elif release_st == 'P':
            status = 'RP'
        else:
            status = 'ERROR'

        if not hotfix == '':
            expand_ver = ask_db_sec_vul.read_db_single_column(DB_PATH,'hotfix','expand_ver','hotfixno',hotfix)
            expand_ver = ' , '.join(expand_ver[0][0].split())
        else:
            expand_ver = ''
        if level == 'H':
            level = 'High'
        elif level == 'M':
            level = 'Medium'
        elif level == 'L':
            level = 'Low'  
        else:
            level = ''

        if status == 'HP':
            for cve in cves:
                row = [cve,level,expand_ver]
                if row in result_list_HP:
                    continue
                if domain_flag == 'CVE':
                    if searchme in cve:
                        result_list_HP.append(row)
                else:
                    result_list_HP.append(row)

        if status == 'F':
            for cve in cves:
                row = [cve,level,expand_ver,release]
                if row in result_list:
                    continue
                if domain_flag == 'CVE':
                    if searchme in cve:
                        result_list.append(row)
                else:
                    result_list.append(row)
        elif status == 'NP':
            for cve in cves:
                row = [cve,level,justification]
                if row in result_list_NP:
                    continue
                if domain_flag == 'CVE':
                    if searchme in cve:
                        result_list_NP.append(row)
                else:
                    result_list_NP.append(row)
        
        elif status == 'RP' or status == 'HP':
            for cve in cves:
                row = [cve,level,release]
                if row in result_list_RP:
                    continue
                if domain_flag == 'CVE':
                    if searchme in cve:
                        result_list_RP.append(row)
                else:
                    result_list_RP.append(row)

    for raw in result_list:
        if not raw in table:
            table.append(list(raw))

    for raw in result_list_NP:
        if not raw in table_NP:
            table_NP.append(list(raw))

    for raw in result_list_HP:
        if not raw in table_HP:
            table_HP.append(list(raw))

    for raw in result_list_RP:
        if not raw in table_RP:
            table_RP.append(list(raw))

    return table, table_HP, table_RP, table_NP


def console(request):
    """
    Define the console view behave
    """
    table_flag = True
    table_HP_flag = True
    table_RP_flag = True
    table_NP_flag = True

    heads = ['CVE','Risk Rating','Hotfix','Release']
    heads_HP = ['CVE','Risk Rating','Hotfix']
    heads_RP = ['CVE','Risk Rating','Release']
    heads_NP = ['CVE', 'Risk Rating', 'Justification']
    table, table_HP, table_RP, table_NP = each_search('')
    table_NP = search_noplan()
    tip_count = len(table)
    tip_count_HP = len(table_HP)
    tip_count_RP = len(table_RP)
    tip_count_NP = len(table_NP)
    # if tip_count > 0:
    #     table_flag = True
    # if tip_count_HP > 0:
    #     table_HP_flag = True
    # if tip_count_RP > 0:
    #     table_RP_flag = True
    # if tip_count_NP > 0:
    #     table_NP_flag = True

    HF_list = get_specific_column_distinct('report','hotfix')
    R_list = get_specific_column_distinct('report','release')

    context = {'table_flag':table_flag, 'heads':heads, 'table':table, 'tip_count':tip_count, \
    'table_NP_flag':table_NP_flag,'default_search':'','HF_list':HF_list,'R_list':R_list,'heads_NP':heads_NP,\
    'table_NP':table_NP,'tip_count_NP':tip_count_NP,'table_HP_flag':table_HP_flag,'heads_HP':heads_HP,\
    'table_HP':table_HP,'tip_count_HP':tip_count_HP,'table_RP_flag':table_RP_flag,'heads_RP':heads_RP,\
    'table_RP':table_RP,'tip_count_RP':tip_count_RP}
    return render(request, 'sec_vul/console.html', context)

def db(request):
    """
    Define the console view behave
    """
    report_heads = []
    report_table = []
    report_count = 0
    report_list = ask_db_sec_vul.read_db(DB_PATH, 'report')

    hotfix_heads = []
    hotfix_table = []
    hotfix_count = 0
    hotfix_list = ask_db_sec_vul.read_db(DB_PATH, 'hotfix')

    report_heads = ['name','detail','cves','rpms','level','tools','tools_ver',\
        'db_ver','scan_date','hotfix','hotfix_st','release','release_st','description']
    for raw in report_list:
        report_count += 1
        report_table.append(list(raw))

    hotfix_heads = ['hotfixno','version','expand_ver','release_date', 'status']
    for raw in hotfix_list:
        hotfix_count += 1
        hotfix_table.append(list(raw))

    context = {'report_heads':report_heads, 'report_table':report_table, 'report_count':report_count,\
    'hotfix_heads':hotfix_heads,'hotfix_table':hotfix_table,'hotfix_count':hotfix_count}
    return render(request, 'sec_vul/db.html', context)

def overview(request):
    """
    Charts panel
    """
    total_cves = []
    context = {}
    pie_dict_hotfix = {}
    pie_dict_release = {}
    pie_dict_level = {}
    HF_NULL = 'None'
    Release_NULL = 'None'
    Level_NULL = 'None'
    HF_H = {}
    HF_M = {}
    HF_L = {}
    R_H = {}
    R_M = {}
    R_L = {}
    HF_set = set()
    R_set = set()

    result_list = ask_db_sec_vul.read_db(DB_PATH, 'report', "cves,hotfix,release,level")
    for row in result_list:
        if row[0] == '':
            continue
        else:
            cves = row[0].split('\n')
            total_cves = total_cves + cves
            hotfix = row[1]
            if hotfix == '':
                hotfix = HF_NULL
            HF_set.add(hotfix)
            release = row[2].split()
            if release == []:
                release = [Release_NULL]
            R_set.update(release)
            level = row[3]

            if hotfix in pie_dict_hotfix:
                pie_dict_hotfix[hotfix] = pie_dict_hotfix[hotfix] + cves
            else:
                pie_dict_hotfix[hotfix] = cves

            for each_release in release:
                if each_release in pie_dict_release:
                    pie_dict_release[each_release] = pie_dict_release[each_release] + cves
                else:
                    pie_dict_release[each_release] = cves
    
            if level == 'H':
                if 'High' in pie_dict_level:
                    pie_dict_level['High'] = pie_dict_level['High'] + cves
                else:
                    pie_dict_level['High'] = cves

                if hotfix in HF_H:
                    HF_H[hotfix] = HF_H[hotfix] + cves
                else:
                    HF_H[hotfix] = cves
                for each_release in release:
                    if each_release in R_H:
                        R_H[each_release] = R_H[each_release] + cves
                    else:
                        R_H[each_release] = cves

            elif level == 'M':
                if 'Medium' in pie_dict_level:
                    pie_dict_level['Medium'] = pie_dict_level['Medium'] + cves
                else:
                    pie_dict_level['Medium'] = cves
                if hotfix in HF_M:
                    HF_M[hotfix] = HF_M[hotfix] + cves
                else:
                    HF_M[hotfix] = cves
                for each_release in release:
                    if each_release in R_M:
                        R_M[each_release] = R_M[each_release] + cves
                    else:
                        R_M[each_release] = cves

            elif level == 'L':
                if 'Low' in pie_dict_level:
                    pie_dict_level['Low'] = pie_dict_level['Low'] + cves
                else:
                    pie_dict_level['Low'] = cves
                if hotfix in HF_L:
                    HF_L[hotfix] = HF_L[hotfix] + cves
                else:
                    HF_L[hotfix] = cves
                for each_release in release:
                    if each_release in R_L:
                        R_L[each_release] = R_L[each_release] + cves
                    else:
                        R_L[each_release] = cves

            else:
                if Level_NULL in pie_dict_level:
                    pie_dict_level[Level_NULL] = pie_dict_level[Level_NULL] + cves
                else:
                    pie_dict_level[Level_NULL] = cves

    #Count distinct num
    total_count = len(set(total_cves))
    for key in pie_dict_hotfix.keys():
        pie_dict_hotfix[key] = len(set(pie_dict_hotfix[key]))
    for key in pie_dict_release.keys():
        pie_dict_release[key] = len(set(pie_dict_release[key]))
    for key in pie_dict_level.keys():
        pie_dict_level[key] = len(set(pie_dict_level[key]))
    for key in HF_H.keys():
        HF_H[key] = len(set(HF_H[key]))
    for key in HF_M.keys():
        HF_M[key] = len(set(HF_M[key]))
    for key in HF_L.keys():
        HF_L[key] = len(set(HF_L[key]))
    for key in R_H.keys():
        R_H[key] = len(set(R_H[key]))
    for key in R_M.keys():
        R_M[key] = len(set(R_M[key]))
    for key in R_L.keys():
        R_L[key] = len(set(R_L[key]))

    if HF_NULL in pie_dict_hotfix:
        del pie_dict_hotfix[HF_NULL] # Don't take care of None HF in HF distribution
    total_HF = 0
    for key in pie_dict_hotfix.keys():
        total_HF += pie_dict_hotfix[key]
    heads_hotfix = ['Hotfix Status',total_HF]

    if Release_NULL in pie_dict_release:
        del pie_dict_release[Release_NULL]
    total_Release = 0
    for key in pie_dict_release.keys():
        total_Release += pie_dict_release[key]
    heads_release = ['Release Status',total_Release]

    if Level_NULL in pie_dict_level:
        del pie_dict_level[Level_NULL] # Don't take care of None HF in HF distribution
    total_Level = 0
    for key in pie_dict_level.keys():
        total_Level += pie_dict_level[key]
    heads_level = ['Risk Rating Status',total_Level]

    image_path = PATH_STATIC+'panel/'
    file_name_hotfix = sec_plot.pie(heads_hotfix, pie_dict_hotfix, image_path)
    file_name_release = sec_plot.pie(heads_release, pie_dict_release, image_path)
    file_name_level = sec_plot.pie(heads_level, pie_dict_level, image_path)
    pic = []
    pic.append(PATH_IMAGE+file_name_hotfix)
    pic.append(PATH_IMAGE+file_name_release)
    pic.append(PATH_IMAGE+file_name_level)

    HF_heads = ['Hotfix','High','Medium','Low','release_date']
    R_heads = ['Release','High','Medium','Low']
    for key in HF_set:
        fill_0(key, HF_H)
        fill_0(key, HF_M)
        fill_0(key, HF_L)
    for key in R_set:
        fill_0(key, R_H)
        fill_0(key, R_M)
        fill_0(key, R_L)

    HF_Table = []
    R_Table = []
    HF_list = list(HF_set)
    HF_list.sort(reverse=True)
    HF_Date = {}
    for hotfix in HF_list:
        if hotfix == 'None':
            continue
        date_str = ask_db_sec_vul.read_db_single_column(DB_PATH,'hotfix','release_date','hotfixno',hotfix)
        HF_Date[hotfix] = date_str[0][0]

    R_list = list(R_set)
    R_list.sort(reverse=True)
    for key in HF_list:
        if not key == 'None':
            HF_Table.append([key, HF_H[key], HF_M[key], HF_L[key], HF_Date[key]])
    for key in R_list:
        if not key == 'None':
            R_Table.append([key, R_H[key], R_M[key], R_L[key]])


    context = {'pic':pic, 'HF_heads':HF_heads, 'R_heads':R_heads, 'HF_Table':HF_Table, 'R_Table':R_Table}
    return render(request, 'sec_vul/overview.html', context)

def fill_0(key, dict):
    """
    Fill in 0 if dict hasn't input key
    """
    if not key in dict:
        dict[key] = 0

def back_to_menu(request):
    """
    Return Menu 
    """
    return HttpResponseRedirect(reverse('sec_vul:console'))


def search(request):
    """
    Search db by input like cve & export "cve,level,hotfix,release"
    """
    table_flag = False
    table_HP_flag = False
    table_RP_flag = False
    table_NP_flag = False
    
    table = []
    table_HP = []
    table_RP = []
    table_NP = []
    table_tmp = []
    table_tmp_HP = []
    table_tmp_RP = []
    table_tmp_NP = []
    tip_count = 0
    tip_count_HP = 0
    tip_count_RP = 0
    tip_count_NP = 0
    and_count = 0
    HF_list = get_specific_column_distinct('report','hotfix')
    R_list = get_specific_column_distinct('report','release')
    search_str = ''
    
    if request.method == 'POST':
        heads = ['CVE','Risk Rating','Hotfix','Release']
        heads_HP = ['CVE', 'Risk Rating', 'Hotfix']
        heads_RP = ['CVE', 'Risk Rating', 'Release']
        heads_NP = ['CVE', 'Risk Rating', 'Justification']
        search_str = request.POST['searchme']

        #Tackle multiple search, split by space or comma is "OR", split by & is "AND"
        if '&' in search_str:
            search_list = search_str.split('&')
            for searchme in search_list:
                and_count += 1
                each_table, each_table_HP, each_table_RP, each_table_NP = each_search(searchme)
                table_tmp = table_tmp + each_table
                table_tmp_HP = table_tmp_HP + each_table_HP
                table_tmp_RP = table_tmp_RP + each_table_RP
                table_tmp_NP = table_tmp_NP + each_table_NP

            #GET items duplicated in all each_table
            for row in table_tmp:
                if table_tmp.count(row) == and_count and not row in table:
                    table.append(row)
                    tip_count += 1
            for row in table_tmp_HP:
                if table_tmp_HP.count(row) == and_count and not row in table_HP:
                    table_HP.append(row)
                    tip_count_HP += 1
            for row in table_tmp_RP:
                if table_tmp_RP.count(row) == and_count and not row in table_RP:
                    table_RP.append(row)
                    tip_count_RP += 1
            for row in table_tmp_NP:
                if table_tmp_NP.count(row) == and_count and not row in table_NP:
                    table_NP.append(row)
                    tip_count_NP += 1

        else:
            search_list = re.split(" |,", search_str)
            for searchme in search_list:
                each_table, each_table_HP, each_table_RP, each_table_NP = each_search(searchme)
                #Distinct the combine search list
                for row in each_table:
                    if not row in table:
                        table.append(row)
                        tip_count += 1
                for row in each_table_HP:
                    if not row in table_HP:
                        table_HP.append(row)
                        tip_count_HP += 1
                for row in each_table_RP:
                    if not row in table_RP:
                        table_RP.append(row)
                        tip_count_RP += 1
                for row in each_table_NP:
                    if not row in table_NP:
                        table_NP.append(row)
                        tip_count_NP += 1

    else:
        return HttpResponseRedirect(reverse('sec_vul:console'))

    if tip_count > 0:
        table_flag = True
    if tip_count_HP > 0:
        table_HP_flag = True
    if tip_count_RP > 0:
        table_RP_flag = True
    if tip_count_NP > 0:
        table_NP_flag = True
    context = {'table_flag':table_flag, 'heads':heads, 'table':table, 'tip_count':tip_count, \
    'table_NP_flag':table_NP_flag,'default_search':search_str,'HF_list':HF_list,'R_list':R_list,'heads_NP':heads_NP,\
    'table_NP':table_NP,'tip_count_NP':tip_count_NP,'table_HP_flag':table_HP_flag,'heads_HP':heads_HP,\
    'table_HP':table_HP,'tip_count_HP':tip_count_HP,'table_RP_flag':table_RP_flag,'heads_RP':heads_RP,\
    'table_RP':table_RP,'tip_count_RP':tip_count_RP}
    return render(request, 'sec_vul/console.html', context)


def db_sql(request):
    """
    Return result as the input sql 
    """
    table_sql_flag = False
    report_heads = []
    report_table = []
    table_sql = []
    report_count = 0
    report_list = ask_db_sec_vul.read_db(DB_PATH, 'report')

    hotfix_heads = []
    hotfix_table = []
    hotfix_count = 0
    hotfix_list = ask_db_sec_vul.read_db(DB_PATH, 'hotfix')

    report_heads = ['name','detail','cves','rpms','level','tools','tools_ver',\
        'db_ver','scan_date','hotfix','hotfix_st','release','release_st','description']
    for raw in report_list:
        report_count += 1
        report_table.append(list(raw))

    hotfix_heads = ['hotfixno','version','expand_ver','release_date', 'status']
    for raw in hotfix_list:
        hotfix_count += 1
        hotfix_table.append(list(raw))

    if request.method == 'POST':
        sql = request.POST['sql']
        result_list = ask_db_sec_vul.excute_sql(DB_PATH,sql)
        for raw in result_list:
            table_sql.append(list(raw))

        if len(table_sql) > 0:
            table_sql_flag = True


    context = {'report_heads':report_heads, 'report_table':report_table, 'report_count':report_count,\
        'hotfix_heads':hotfix_heads,'hotfix_table':hotfix_table,'hotfix_count':hotfix_count,\
        'table_sql_flag':table_sql_flag,'table_sql':table_sql}
    return render(request, 'sec_vul/db.html', context)

