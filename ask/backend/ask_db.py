#!/usr/bin/python

import commands
import getopt
import sys
import os

SUCCESS = 0
FAILURE = 1
COMMAND_PREFIX = "psql -U postgres %s -c \'%s\'"
COMMAND_QUERY = 'select %s from %s'
COMMAND_QUERY_BY_ID = 'select %s from %s where id in (%s)'
COMMAND_QUERY_BY_CUSTOMER_ID = 'select %s from %s where customer_id in (%s)'

PATH_CUSTOMER = os.getcwd()+'/ask/static/ask/conf/customer_list.prop'

def usage():
    """
    Print usage
    """
    print "show usage"

def getopts():
    """
    Get commands opt arguments
    """
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hi:a:", ["help", "dbname", "ask"])
        return opts
    except getopt.GetoptError:
        usage()
        sys.exit(FAILURE)

def strip_line(line):
    """
    Process " id |   customer_name    | system_version | rmg_count  " to list of them
    """
    info = line.split('|')
    for i in range(len(info)):
        info[i] = info[i].strip()
    return info

def write_to_file(title, contents, output_path='./text.db'):
    """
    Write the db query result to file in order to paste into excel
    """
    f_out = open(output_path, 'w')
    f_out.write("\t".join(title)+"\n")
    for content in contents:
        f_out.write("\t".join(content)+"\n")

    f_out.close()

def ask_db(db_name, domain, output_path='./text.db'):
    """
    Export customer db's info about domain(like 'systems' etc)
    """
    specific = "*"
    status, output = commands.getstatusoutput(COMMAND_PREFIX % (db_name, COMMAND_QUERY % (specific, domain)))
    lines = output.split('\n')
    title = strip_line(lines[0])
    contents = []
    for i in range(2, len(lines)):
        content = strip_line(lines[i])
        contents.append(content)

    write_to_file(title, contents, output_path)
    return title, contents

def ask_db_distinct(db_name, domain, output_path='./text.db', customer_file=PATH_CUSTOMER):
    """
    Export customer db's info about domain(like 'systems' etc) with distinct customer
    """
    #read in distinct customers
    f_in = open(customer_file, 'r')
    f_in.readline()
    f_in.readline()
    f_in.readline()
    id_list = []
    line = f_in.readline()
    while line:
        line = line.strip('\r\n')
        if line[0] == '#':
            break
        else:
            info = line.split(':')
            id_list.append(info[1])
            line = f_in.readline()

    specific = "*"

    if domain == 'systems':
        cmd = COMMAND_QUERY_BY_ID
    else:
        cmd = COMMAND_QUERY_BY_CUSTOMER_ID

    status, output = commands.getstatusoutput(COMMAND_PREFIX % \
        (db_name, cmd % (specific, domain, ','.join(id_list))))
    lines = output.split('\n')
    title = strip_line(lines[0])
    contents = []
    for i in range(2, len(lines)):
        content = strip_line(lines[i])
        contents.append(content)

    f_in.close()
    write_to_file(title, contents, output_path)
    return title, contents

def main():
    """
    The main
    """
    db_name = ""
    domain = ""
    db_flag = False
    ask_flag = False

    opts = getopts()
    for option, value in opts:
        if option in ('-h', '--help'):
            usage()
            sys.exit(SUCCESS)
        elif option in ('-i', '--dbname'):
            db_flag = True
            db_name = value
        elif option in ('-a', '--ask'):
            ask_flag = True
            domain = value

        else:
            usage()
            sys.exit(FAILURE)

    if db_flag and ask_flag:
        ask_db(db_name, domain)

    else:
        usage()
        sys.exit(FAILURE)

if __name__ == "__main__":
    main()