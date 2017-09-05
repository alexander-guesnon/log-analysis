# 1 import libraries to query PSQL
import psycopg2

'''
Input: void
Output: void
Function: This function will report the current top 3 articles, the current
top authors, and errors that are over 1% of all requests.
'''

'''
              title               | views
----------------------------------+--------
 Candidate is jerk, alleges rival | 338647
 Bears love berries, alleges bear | 253801
 Bad things gone, say good people | 170098
(3 rows)

    [('Candidate is jerk, alleges rival', 338647L), ('Bears love berries, alleges bear', 253801L), ('Bad things gone, say good people', 170098L)]


'''


def print_results(t3a):
    print("test")
    #print top 3 tables
#        top_3_table= '''
#---------------------------------------------
#|               Top 3 Articles              |
#|-------------------------------------------|
#|             Articles             | Views  |
#|----------------------------------+--------|
#'''
#        t3t_template="| {:32} | {:6} |"
#        print (top_3_table),
#        for x in range(len(t3a)):
#            print(t3t_template.format(t3a[x][0], t3a[x][1]))
#        print("---------------------------------------------");
#print top authors

#print important errors

def DB_Status():

    try:
        conn = psycopg2.connect(
            "dbname='news' user='vagrant' host='localhost' password='password'")
        cur = conn.cursor()
    except:
        print "I am unable to connect to the database"

    # 2 run a query to find the 3 top articles of all time
    #try:
    #    cur.execute('''
    #                SELECT articles.title,
    #               Count(*) AS views
    #        FROM   articles,
    #               (SELECT Substring(path, 10) AS path
    #                FROM   log) AS modifiedLog
    #        WHERE  path != ''
    #               AND modifiedLog.path = articles.slug
    #        GROUP  BY articles.title
    #        ORDER  BY views DESC
    #        LIMIT  3;
    #    ''')
    #except:
    #    print("Their was an error trying to querry for the top 3 articles" )

    # 3 store in variable (top_3_articals)
    #top_3_articals = cur.fetchall()
    # 4 run a query to find the top authors of all time.

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
    except:
        print("top 3 articles failed to exicute")

    print(cur.fetchall())
    # 5 store in variable (top_autohors)
    # 6 run a query to find what days resulted in having their total requests error over 1%
    '''
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
    '''
    # 7 store in variable (important_errors)
    # 8 print out information in a readable format for the user

    #print_results(top_3_articals);



if __name__ == "__main__":
    DB_Status()
