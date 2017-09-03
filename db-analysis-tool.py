#1 import libraries to query PSQL


'''
tables make up
authors (
    author integer
    title text
    slug text
    body text
    time timestamp with time zone
    id integer
)

log (
    path text
    ip inet
    method text
    status text
    time timestamp with timezone
    id integer
)

authors (
    name text
    bio text
    id integer
)

'''


'''
Input: void
Output: void
Function: This function will report the current top 3 articles, the current
top authors, and errors that are over 1% of all requests.
'''
def DB_Status():
    #2 run a query to find the 3 top articles of all time
    #3 store in variable (top_3_articals)
    #4 run a query to find the top authors of all time.
    #5 store in variable (top_autohors)
    #6 run a query to find what days resulted in having their total requests error over 1%
    #7 store in variable (important_errors)
    #8 print out information in a readable format for the user
    print ("hello world")


if __name__ == "__main__":
    DB_Status()
