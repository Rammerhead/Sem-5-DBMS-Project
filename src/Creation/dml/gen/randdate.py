import random
import time
    
def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y/%m/%d %I:%M %p', prop)
    

def today():
    return (random_date("2022/1/1 1:30 PM", "2022/7/7 4:50 PM", random.random()).split()[0].replace("/", "-"))

def yesterday():
    return (random_date("2021/1/1 1:30 PM", "2021/7/7 4:50 PM", random.random()).split()[0].replace("/", "-"))


def main():
    return (random_date("1991/1/1 1:30 PM", "1998/1/1 4:50 AM", random.random()).split()[0].replace("/", "-"))

if __name__ == '__main__':
    #print(main())
    print(yesterday())
