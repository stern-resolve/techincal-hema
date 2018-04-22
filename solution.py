# Technical Task Solution
import sys

# checked input files for formatting so we can make a few assumptions:
# line-terminator = '\n' (ASCII 0x0A)
LINETERM = '\n'
# field-delimited = ',' (ASCII 0x2C)
DELIMITER = ','
# files contain: one header record (line 0) and one data record (line 1)
# so, files appear to be conformant with RFC4180 and given simple formatting, we 
# can forego using the CSV module and directly operate on the data.

# notes:
# expected output appears to show results in sorted dictionary key order - not explicitly
# stated as a requirement, but don't want to fail on that so can use a class with __repr__ 
# to control attribute print order

# day meta data: op, sort_key
DAY_META_DATA = {
    "mon":("square", 1),
    "tue":("square", 2),
    "wed":("square", 3),
    "thu":("double", 4),
    "fri":("double", 5)
}
DAY_OPS = {
    "double":lambda v:v+v,
    "square":lambda v:v*v
}
# assumption based on data is that there are no stretches expanding to a single day, so
# e.g. mon-mon or tue-tue are not valid
DAYS = {
    "mon-tue":["mon","tue"],
    "mon-wed":["mon","tue","wed"],
    "mon-thu":["mon","tue","wed","thu"],
    "mon-fri":["mon","tue","wed","thu","fri"],
    "tue-wed":["tue","wed"],
    "tue-thu":["tue","wed","thu"],
    "tue-fri":["tue","wed","thu","fri"],
    "wed-thu":["wed","thu"],
    "wed-fri":["wed","thu","fri"],
    "thu-fri":["thu","fri"],
    "mon":["mon"],
    "tue":["tue"],
    "wed":["wed"],
    "thu":["thu"],
    "fri":["fri"]
}
class Day(object):

    def __init__(self,day_name):
        self.name = day_name
        self.value=0
        self.result=0
        self.description=""
        self.op_name, self.sort_key = DAY_META_DATA[self.name]
        self.op = DAY_OPS[self.op_name]

    #@property
    def set_value(self,value):
        self.value=value
        self.result = self.op(value)

    #@property
    def set_description(self,description):
        self.description=description

    def __repr__(self):
        return "{"+"'day' : {0}, 'description' : {1} {2}, '{3}' : {4}, 'value' : {5}".format(self.name, self.description, self.result, self.op_name, self.result, self.value) + "}"


# day meta data
TEST_DATA_1_HDR = ["mon","tue","some_column1","wed","thu","fri","description"]
TEST_DATA_1_DROW = [1,5,"data",2,3,3,"first_desc"]

TEST_DATA_2_HDR = ["mon-thu","fri","description","another_column2"]
TEST_DATA_2_DROW = [2,3,"second_desc","some_data"]

TEST_RESULTS_1 = [
    {'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
    {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
    {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
    {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
    {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}
 ]


TEST_OUTPUT_2 = [
    {'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
    {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
    {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}
]



def read_csv(filename):
# read_csv(file_name)
# reads csv data and returns:
# a list of column headings and
# a list of data rows (lists of lists) 
    
    #headings = []
    data_rows = []
    lines=0
    with open(filename,'r',encoding='utf-8') as csvfile:
        for line in csvfile:
            cols = line.rstrip().split(DELIMITER)
            if lines==0:
                headings = cols[:]
                lines+=1
            else:
                data_rows.append(cols[:])
    
    # end of file context, so file will be closed
    return headings,data_rows
  
def process_files(flist):
    results={}
    for filename in flist:
        res=process_file(filename)
        results[filename]=res
    return results

def process_file(filename):
    headings,data_rows = read_csv(filename)
    assert(len(headings)==len(data_rows[0]))
    assert(len(data_rows)==1)

    res=get_daily_data(headings,data_rows[0])
    return res

def get_daily_data(headings,data_row):
    # need to build a list of dicts
    # one dict for each of the days mon,tue,wed,thu,fri
    #five_days={"mon":{},"tue":{},"wed":{},"thu":{},"fri":{}}
    final=[]
    #any_day = {}
    description=""
    day_values={}
 #   day_result_ops={}
  #  day_results={}
    
    working=dict(zip(headings,data_row))

    for key,val in working.items():
        # read day values, expanding stretches as necessary
        if key in DAYS:
            # get all days covered by this day-name/stretch
            day_list = DAYS[key]
            for day_name in day_list:
                day_values[day_name]=int(val)
            continue

        if key == "description":
            description = val
            continue
        
        # all other keys ignored as per task brief

    assert ( "mon" in day_values and 
        "tue" in day_values and 
        "wed" in day_values and 
        "thu" in day_values and 
        "fri" in day_values)

    
    for day,val in day_values.items():
        #day_result_type = DAY_RESULT_OPS[day]
        #op = DAY_OPS[day_result_type]
        #day_results[day] = op(val)
        #day_result_ops[day]= day_result_type
        #day_result_type=day_result_ops[day]
        #day_data["day"]=day
        day = Day(day)
        day.set_value(val)
        day.description=description

        final.append(day)

    final.sort(key = lambda d:d.sort_key)
    
    return final

def tests():
    test_res = get_daily_data(TEST_DATA_1_HDR, TEST_DATA_1_DROW)
    assert(len(test_res) == len(TEST_RESULTS_1))
    
    print("All tests passed")
    
def standard_run():    
    filenames = ['1.csv','2.csv','3.csv']

    res=process_files(filenames)
    for filename,daily_data in res.items():
        print(filename)
        for day in daily_data:
            print(day)  #, sep='\n')
    #print(res)


def main():
    if len(sys.argv)>1:
        run_mode = sys.argv[1].lower().strip()
        if run_mode == "test":
            tests()
            return

    standard_run()




if __name__ == "__main__":
    main()