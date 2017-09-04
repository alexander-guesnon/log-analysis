# 1 import libraries to query PSQL
'''
Input: void
Output: void
Function: This function will report the current top 3 articles, the current
top authors, and errors that are over 1% of all requests.
'''


def DB_Status():
    # 2 run a query to find the 3 top articles of all time
    '''
        SELECT articles.title ,COUNT(*) AS views FROM articles, (
            SELECT SUBSTRING(path,10) AS path
            FROM log
        )
        AS modifiedLog
        WHERE path!='' AND modifiedLog.path=articles.slug
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;
    '''

    # 3 store in variable (top_3_articals)
    # 4 run a query to find the top authors of all time.
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
    print ("hello world")


if __name__ == "__main__":
    DB_Status()
