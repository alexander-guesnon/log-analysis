import psycopg2

'''
Input: t3a (array of object(string, int)), ta(array of object(string, int)), ie
array of object(date time, float)
Output: void
Function: prints out the Top 3 Articles table, Top Authors table, and the
Important Errors table
'''
def print_results(t3a, ta, ie):
    Log_Output ="Db analisis\n";

    Log_Output = Log_Output + '''
---------------------------------------------
|               Top 3 Articles              |
|-------------------------------------------|
|             Articles             | Views  |
|----------------------------------+--------|
'''

    t3t_template = "| {:32} | {:6} |"

    for x in range(len(t3a)):
        Log_Output = Log_Output + t3t_template.format(t3a[x][0], t3a[x][1])+ "\n"
    Log_Output = Log_Output + "---------------------------------------------\n"

    Log_Output = Log_Output + '''
------------------------------------
|            Top Authors           |
|----------------------------------|
|         Authors         | Views  |
|-------------------------+--------|
'''
    ta_template="| {:23} | {:6} |"

    for x in range(len(ta)):
        Log_Output = Log_Output + ta_template.format(ta[x][0],ta[x][1]) + "\n"
    Log_Output = Log_Output + "------------------------------------\n"

    Log_Output = Log_Output + '''
----------------------------------------------------
|                 Important Errors                 |
|--------------------------------------------------|
|             date          |  failure_percentage  |
|---------------------------+----------------------|
'''
    ie_template = "| {:25} | {:19}% |"

    for x in range(len(ie)):
        Log_Output = Log_Output + ie_template.format( str(ie[x][0]),ie[x][1])+"\n"
    Log_Output = Log_Output + "----------------------------------------------------\n"
    print(Log_Output)


'''
Input: void
Output: void
Function: This function will report the current top 3 articles, the current
top authors, and errors that are over 1% of all requests.
'''
def DB_Status():
    try:
        conn=psycopg2.connect(database="news")
        cur=conn.cursor()
    except Exception, x:
        print ("I am unable to connect to the database:")
        print(x)
        return -1;

    try:
        cur.execute('''
                    SELECT articles.title,
                   Count(*) AS views
            FROM   articles,
                   (SELECT Substring(path, 10) AS path
                    FROM   log) AS modifiedLog
            WHERE  path != ''
                   AND modifiedLog.path = articles.slug
            GROUP  BY articles.title
            ORDER  BY views DESC
            LIMIT  3;
        ''')
    except Exception, x:
        print("Their was an error trying to querry for the top 3 articles" )
        print(x)
        return -1;

    top_3_articals = cur.fetchall()

    try:
        cur.execute(
        '''
            SELECT authors.name ,SUM(views) AS views
            FROM authors, (
                SELECT articles.author, articles.title ,COUNT(*) AS views
                FROM articles, (
                    SELECT SUBSTRING(path,10) AS path
                    FROM log
                ) AS modifiedLog
                WHERE path!='' AND modifiedLog.path=articles.slug
                GROUP BY articles.title, articles.author) AS articleviews
            WHERE articleviews.author=authors.id
            GROUP BY authors.name
            ORDER BY views DESC;
        '''
            )
    except Exception, x:
        print("top autohors failed to exicute")
        print(x)
        return -1;

    top_autohors=cur.fetchall()

    try:
        cur.execute('''
                SELECT final.date,
                       failure_percentage
                FROM   (SELECT success.date,
                               Round(100 * ( Cast(errors.count AS NUMERIC) / Cast (
                                             success.count AS NUMERIC) ),
                               2) AS failure_percentage
                        FROM   (SELECT Date_trunc('day', time) AS date,
                                       Count(status)
                                FROM   log
                                WHERE  status = '404 NOT FOUND'
                                GROUP  BY date
                                ORDER  BY date) AS errors,
                               (SELECT Date_trunc('day', time) AS date,
                                       Count(status)
                                FROM   log
                                WHERE  status = '200 OK'
                                GROUP  BY date
                                ORDER  BY date) AS success
                        WHERE  errors.date = success.date) AS final
                WHERE  failure_percentage > 1;
                ''')
    except Exception, x:
        print("important errors failed to exicute")
        print(x)
        return -1;

    important_errors=cur.fetchall()

    print_results(top_3_articals,top_autohors,important_errors);



if __name__ == "__main__":
    DB_Status()
