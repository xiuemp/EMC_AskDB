import sqlite3

DEFAULT_DOMAIN = 'cves,level,hotfix,release,hotfix_st,release_st,description'

def read_db_single_column(db_path, table, domain, key, value):
	"""
	Return specific domain with the given condition
	"""
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	cu.execute('select %s from %s where %s = \'%s\'' % (domain, table, key, value))
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list


def read_db(db_path, table, domain='*'):
	"""
	Read db & export 
	"""
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	cu.execute('select %s from %s' % (domain, table))
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list

def read_db_by_like(db_path, searchme='', domain=DEFAULT_DOMAIN):
	"""
	Read db & export by like
	"""
	# if searchme == '':
	# 	searchme = 'CVE'
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	if searchme == '':
		cu.execute("select %s from report order by release desc,hotfix desc,\
			case level when 'H' then 1 when 'M' then 2 when 'L' then 3 when '' then 4 end" % (domain))
	else:
		cu.execute("select %s from report where cves like \'%%%s%%\'  order by release desc,hotfix desc,\
			case level when 'H' then 1 when 'M' then 2 when 'L' then 3 when '' then 4 end" % (domain,searchme))

	result_list = cu.fetchall()
	cu.close()
	cx.close()
	return result_list

def read_db_by_like_HF(db_path, searchme='HF', domain=DEFAULT_DOMAIN):
	"""
	Read db & export by like
	"""
	if searchme == '':
		searchme = 'HF'
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()

	cu.execute("select %s from report where hotfix like \'%%%s%%\' order by release desc,hotfix desc,\
			case level when 'H' then 1 when 'M' then 2 when 'L' then 3 when '' then 4 end" % (domain,searchme))
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list

def read_db_by_like_Release(db_path, searchme='', domain=DEFAULT_DOMAIN):
	"""
	Read db & export by like
	"""
	if searchme == '':
		searchme = ''
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	cu.execute("select %s from report where release like \'%%%s%%\' order by release desc,hotfix desc,\
			case level when 'H' then 1 when 'M' then 2 when 'L' then 3 when '' then 4 end" % (domain,searchme))
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list

def read_db_np(db_path):
	"""
	Return the records when hotfix_st == 'NP' & release_st == 'NP'
	"""
	domain = "name,cves,level,description"
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	cu.execute("select %s from report where hotfix_st='NP' and release_st='NP' order by \
			case level when 'H' then 1 when 'M' then 2 when 'L' then 3 when '' then 4 end" % (domain))
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list

def excute_sql(db_path, sql):
	"""
	Return the result by excuting input sql
	"""
	cx = sqlite3.connect(db_path)
	cu = cx.cursor()
	cu.execute(sql)
	result_list = cu.fetchall()
	
	cu.close()
	cx.close()
	return result_list