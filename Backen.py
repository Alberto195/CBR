from urllib import request
import rarfile
import requests
from bs4 import BeautifulSoup
import ssl
import mysql.connector
import os
import pathlib
import csv
import dbf
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def dbf_to_csv(dbf_table_pth):  # Input a dbf, output a csv, same name, same path, except extension
    csv_fn = dbf_table_pth[:-4] + ".csv"  # Set the csv file name
    table = dbf.Table(dbf_table_pth, codepage='cp866')  # table variable is a DBF object
    with open(csv_fn, 'w', newline='', encoding='cp866') as f:  # create a csv file, fill it with dbf content
        writer = csv.writer(f, delimiter=',')
        table.open(mode=dbf.READ_WRITE)
        writer.writerow(table.field_names)  # write the column name
        if len(table.field_names) == 6:
            for record in table:  # write the rows
                a = []
                try:
                    a.append(record.regn)
                    a.append(record.code)
                    a.append(record.sim_r)
                    a.append(record.sim_v)
                    a.append(record.sim_itogo)
                    a.append(record.dt)
                    writer.writerow(a)
                except dbf.FieldMissingError:
                    break
        if len(table.field_names) == 2:
            for record in table:  # write the rows
                a = []
                try:
                    a.append(record.regn)
                    a.append(record.name_b)
                    writer.writerow(a)
                except dbf.FieldMissingError:
                    break
        elif len(table.field_names) == 3:
            for record in table:  # write the rows
                a = []
                try:
                    a.append(record.cont_sum_r)
                    a.append(record.cont_sum_v)
                    a.append(record.cont_sum)
                    writer.writerow(a)
                except dbf.FieldMissingError:
                    break

    return csv_fn  # return the csv name


def todb(url):
    global flag
    flag = False
    mydb = mysql.connector.connect(
        auth_plugin='mysql_native_password',
        user=user,
        password=password,
        database="all_in_one",
    )
    mycursor = mydb.cursor(buffered=True)

    """Проверка на дату"""
    query = "select * from all_dt"
    mycursor.execute(query)
    datafetch = mycursor.fetchall()
    t = datafetch[len(datafetch) - 1][1]
    dt = t.strftime('%Y%m%d')

    if url[22:30] != dt:
        """Добавление новой даты в all_dt"""
        url_date = url[22:26] + '-' + url[26:28] + '-' + url[28:30]
        next_id = len(datafetch) + 1
        next_id = str(next_id)
        flag = True

        sql = "INSERT INTO all_dt (id, Date) VALUES (" + next_id + ",'" + url_date + "')"
        mycursor.execute(sql)
        mydb.commit()

        '''Открываю сайт, качаю в Rar.rar файлы'''
        p = pathlib.Path('Graphics')
        p = str(p.absolute())
        p = p.replace("\\", "/")
        p = p[:-16] + 'Data/Rar.rar'

        r = requests.get(r'https://www.cbr.ru' + url, allow_redirects=True)
        with open(p, 'wb') as f:
            f.write(r.content)

        rf = rarfile.RarFile(p)
        for k in range(3):

            lastpath = rf.namelist()[k]
            file_path = p[:-7] + lastpath

            if not os.path.exists(file_path):
                rf.extractall(p[:-8])

            filen = lastpath[:-4]
            filet = lastpath[5:-4]
            path = p[:-7] + lastpath
            file_csv = dbf_to_csv(path)
            # file_test = 'C:/RAR_STUFF/12020_P11.csv'

            mainquerry = {'auth_plugin': 'mysql_native_password',
                          'user': user,
                          'password': password,
                          'database': "all_in_one",
                          'allow_local_infile': "True"}
            cnx = mysql.connector.connect(**mainquerry)
            curs = cnx.cursor(buffered=True)
            q0 = "CREATE TABLE IF NOT EXISTS " + filen + " like 42019" + filet + ";"
            q00 = "ALTER TABLE "+filen+" DROP column id;"
            q1 = "LOAD DATA LOCAL INFILE '" + file_csv + "' INTO TABLE " + filen
            q2 = " CHARACTER SET cp866"
            q3 = " FIELDS TERMINATED BY ','"
            q4 = " ENCLOSED BY '\"'"
            q5 = " LINES TERMINATED BY '\\r\\n'"
            q6 = " IGNORE 1 LINES;"
            querload = q1 + q2 + q3 + q4 + q5 + q6
            quercommit = 'commit;'
            curs.execute(q0)
            curs.execute(q00)
            curs.execute(querload)
            curs.execute(quercommit)
            curs.close()


def prepare(log1, log2):
    """constants"""
    global user
    global password
    cbr = ''
    user = log1[:-1]
    password = log2[:-1]
    #################
    '''Получение ссылок'''
    quote_page = 'https://www.cbr.ru/banking_sector/otchetnost-kreditnykh-organizaciy/'
    page = request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all('a'):
        if '.rar' in link.get('href') and '102-' in link.get('href'):
            cbr = link.get('href')
            break

    '''Обрабатываю ссылки в скачивание в бд и таблицы'''
    todb(cbr)

    return flag

