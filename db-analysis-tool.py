# 1 import libraries to query PSQL


'''
tables make up
articles (
    author integer
    title text
    slug text
    body text
    time timestamp with time zone
    id integer
)

 author |    title                           |  slug                     |                  lead                                                       |        body                               |             time              | id
--------+------------------------------------+---------------------------+-----------------------------------------------------------------------------+-------------------------------------------+-------------------------------+---
 3      | Bad things gone, say good people   | bad-things-gone           | All bad things have gone away, according to a poll of good people Thursday. | Bad things are a thing of the bad, bad... | 2016-08-15 18:55:10.814316+00 | 23
 4      | Balloon goons doomed               | balloon-goons-doomed      | The doom of balloon goons is true news.                                     | The goons are doomed, no matter how ...   | 2016-08-15 18:55:10.814316+00 | 24


               title                |           slug
------------------------------------+---------------------------
 Bad things gone, say good people   | bad-things-gone
 Balloon goons doomed               | balloon-goons-doomed
 Bears love berries, alleges bear   | bears-love-berries
 Candidate is jerk, alleges rival   | candidate-is-jerk
 Goats eat Google's lawn            | goats-eat-googles
 Media obsessed with bears          | media-obsessed-with-bears
 Trouble for troubled troublemakers | trouble-for-troubled
 There are a lot of bears           | so-many-bears


log (
    path text
    ip inet
    method text
    status text
    time timestamp with timezone
    id integer
)

                path                 |       ip       | method |    status     |          time          |   id
-------------------------------------+----------------+--------+---------------+------------------------+---------
 /                                   | 198.51.100.195 | GET    | 200 OK        | 2016-07-01 07:00:00+00 | 1678923
 /article/candidate-is-jerk          | 198.51.100.195 | GET    | 200 OK        | 2016-07-01 07:00:47+00 | 1678924
 /article/goats-eat-googles          | 198.51.100.195 | GET    | 200 OK        | 2016-07-01 07:00:34+00 | 1678925
 /article/goats-eat-googles          | 198.51.100.195 | GET    | 200 OK        | 2016-07-01 07:00:52+00 | 1678926
 /article/balloon-goons-doomed       | 198.51.100.195 | GET    | 200 OK        | 2016-07-01 07:00:23+00 | 1678927
 /article/balloon-goons-doomede      | 192.0.2.30     | GET    | 404 NOT FOUND | 2016-07-01 07:19:09+00 | 1679620




authors (
    name text
    bio text
    id integer
)

          name          |                                                bio                                                 | id
------------------------+----------------------------------------------------------------------------------------------------+----
 Ursula La Multa        | Ursula La Multa is an expert on bears, bear abundance, and bear accessories.                       |  1
 Rudolf von Treppenwitz | Rudolf von Treppenwitz is a nonprofitable disorganizer specializing in procrastinatory operations. |  2
 Anonymous Contributor  | Anonymous Contributor's parents had unusual taste in names.                                        |  3
 Markoff Chaney         | Markoff Chaney is the product of random genetics.                                                  |  4


SELECT time, status FROM log LIMIT 1000;

          time          |    status
------------------------+---------------
 2016-07-01 07:00:00+00 | 200 OK
 2016-07-01 07:00:47+00 | 200 OK
 2016-07-01 07:00:34+00 | 200 OK
 2016-07-01 07:00:52+00 | 200 OK
 2016-07-01 07:00:23+00 | 200 OK
 2016-07-01 07:00:05+00 | 200 OK
 2016-07-01 07:00:54+00 | 200 OK

https://www.postgresql.org/docs/9.2/static/functions-datetime.html
date_trunc(text, timestamp)	timestamp	Truncate to specified precision; see also Section 9.9.2	date_trunc('hour', timestamp '2001-02-16 20:38:40')	2001-02-16 20:00:00

SELECT date_trunc('day',time) FROM log LIMIT 1000;

       date_trunc
------------------------
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00
 2016-07-01 00:00:00+00

SELECT COUNT(*),status AS stuff FROM log GROUP BY status;

  count  |     stuff
---------+---------------
   12908 | 404 NOT FOUND
 1664827 | 200 OK
(2 rows)



SELECT date_trunc('day',time) AS date, COUNT(status)
FROM log
WHERE status='404 NOT FOUND'
GROUP BY date

          date          | count
------------------------+-------
 2016-07-28 00:00:00+00 |   393
 2016-07-22 00:00:00+00 |   406
 2016-07-26 00:00:00+00 |   396
 2016-07-29 00:00:00+00 |   382
 2016-07-06 00:00:00+00 |   420
 2016-07-02 00:00:00+00 |   389
 2016-07-17 00:00:00+00 |  1265
 2016-07-12 00:00:00+00 |   373
 2016-07-07 00:00:00+00 |   360
 2016-07-04 00:00:00+00 |   380


SELECT date_trunc('day',time) AS date, COUNT(status)
FROM log
WHERE status='200 OK'
GROUP BY date

          date          | count
------------------------+-------
 2016-07-01 00:00:00+00 | 38431
 2016-07-02 00:00:00+00 | 54811
 2016-07-03 00:00:00+00 | 54465
 2016-07-04 00:00:00+00 | 54523
 2016-07-05 00:00:00+00 | 54162
 2016-07-06 00:00:00+00 | 54354
 2016-07-07 00:00:00+00 | 54380
 2016-07-08 00:00:00+00 | 54666
 2016-07-09 00:00:00+00 | 54826
 2016-07-10 00:00:00+00 | 54118

https://www.postgresql.org/docs/9.3/static/functions-math.html
https://www.postgresql.org/docs/9.2/static/sql-createcast.html

SELECT cast(393 as float8) /cast (38431 as float8) AS gekk ;

SELECT round((cast(393 as numeric) /cast (38431 as numeric)), 3) AS
gekk;

 gekk
-------
 0.010
(1 row)


SELECT success.date ,round(
(cast(errors.count as numeric) /cast (success.count as numeric)), 3
) AS failure_percentage FROM (
    SELECT date_trunc('day',time) AS date, COUNT(status)
    FROM log
    WHERE status='404 NOT FOUND'
    GROUP BY date
    ORDER BY date
) AS errors, (
    SELECT date_trunc('day',time) AS date, COUNT(status)
    FROM log
    WHERE status='200 OK'
    GROUP BY date
    ORDER BY date
) AS success;

          date          | failure_percentage
------------------------+--------------------
 2016-07-01 00:00:00+00 |              0.007
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.011
 2016-07-01 00:00:00+00 |              0.011
 2016-07-01 00:00:00+00 |              0.009
 2016-07-01 00:00:00+00 |              0.011
 2016-07-01 00:00:00+00 |              0.011
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.010
 2016-07-01 00:00:00+00 |              0.011
 2016-07-01 00:00:00+00 |              0.010



SELECT success.date ,round(
(cast(errors.count as numeric) /cast (success.count as numeric)), 3
) AS failure_percentage FROM (
    SELECT date_trunc('day',time) AS date, COUNT(status)
    FROM log
    WHERE status='404 NOT FOUND'
    GROUP BY date
    ORDER BY date
) AS errors, (
    SELECT date_trunc('day',time) AS date, COUNT(status)
    FROM log
    WHERE status='200 OK'
    GROUP BY date
    ORDER BY date
) AS success;


 On which days did more than 1% of requests lead to errors
                  -------------



            SELECT final.date, failure_percentage FROM (SELECT success.date,
               Round(100*( Cast(errors.count AS NUMERIC) / Cast (
                       success.count AS NUMERIC)
                     ), 2) AS
               failure_percentage
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
                WHERE errors.date = success.date) AS final
                WHERE failure_percentage > 1;


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


    # 7 store in variable (important_errors)
    # 8 print out information in a readable format for the user
    print ("hello world")


if __name__ == "__main__":
    DB_Status()
