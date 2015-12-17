MONTH_DAY = [31,28,31,30,31,30,31,31,30,31,30,31]

def is_leap_year(year):
    year = int(year)
    return ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)

def decode_date(dateString, delimiter=''):
    if delimiter and dateString.find(delimiter) != -1: return map(int, dateString.split(delimiter))
    return map(int, (dateString[:4], dateString[4:6], dateString[6:]))

def encode_date(date, delimiter=''):
    return delimiter.join(map('{:0>2}'.format, date))

def get_next_date(dateString, delimiter=''):
    date = decode_date(dateString, delimiter)

    date[2] += 1
    day = MONTH_DAY[date[1]-1]
    if date[1] == 2 and is_leap_year(date[0]): day += 1
    if date[2] > day:
        date[1] += 1
        date[2] = 1
    if date[1] == 13:
        date[0] += 1
        date[1] = 1

    return encode_date(date, delimiter)

def get_date_list(from_date, to_date, delimiter=''):
    #NOTE: (zacky, MAY.19th) NEED TO ENSURE 'from_date' IS LESS THAN OR EQUAL TO 'to_date'.
    start = encode_date(decode_date(from_date, delimiter), delimiter)
    end = get_next_date(to_date, delimiter)
    while start != end:
        yield start
        start = get_next_date(start, delimiter)
