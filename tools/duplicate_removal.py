import MySQLdb
def get_max_thread(dbname):
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='112358',db='business',port=3306)
        cur = conn.cursor()
        sql = 'select max(thread) from '+dbname
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result[0]:
            return result[0]
        else:
            return -1
    except MySQLdb.Error,msg:
        print "MySQL Error %d: %s" %(msg.args[0],msg.args[1])

def get_thread_from_exposure(url):
    if url.find('-') != -1:
        return url.split('-')[1]
    if url.find('=') != -1:
        return url.split('=')[-1]    
    return None    

def get_thread_from_news(url):
    pos = url.find('.html')
    if pos != -1: return url[:pos].split('/')[-1]

    return None