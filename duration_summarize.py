import csv
import datetime
from collections import defaultdict
import math
import operator


def time_transform(start_time, end_time):
    '''
    transform time into the correct form- datetime
    calculate the duration between times
    '''
    f = "%Y/%m/%d %H:%M:%S"
    start = datetime.datetime.strptime(start_time, f)
    end = datetime.datetime.strptime(end_time, f)
    diff = end - start
    return diff.total_seconds()/(24*3600)


def file_reader(filename):
    '''
    read in file
    convert data into a list of dict
    whose value contains flowchart, node_name, and duration
    '''
    in_file = open(filename, 'r')
    reader = csv.DictReader(in_file)
    duration_source_list = []
    for row in reader:
        cur_dict = {}
        if row['JSSJ']:
            cur_dict['time'] = time_transform(row['KSSJ'], row['JSSJ'])
        else:
            continue
        if row['YWLCMBBH']:
            cur_dict['flowchart'] = row['YWLCMBBH']
        if row['JDZT']:
            cur_dict['node'] = row['JDZT']
        duration_source_list.append(cur_dict)
    in_file.close()
    return duration_source_list


def group_durations(duration_source_list):
    '''
    convert data into a dict of dict, whose value is a list of duration
    '''
    whole_dict = defaultdict(lambda: defaultdict(list))
    for item in duration_source_list:
        whole_dict[item['flowchart']][item['node']].append(item['time'])
    return whole_dict


def sum_duration(whole_dict, filename):
    '''
    write in file with
    most frequent days for process a certain node status
    '''
    title = ['flowchart', 'node', 'days']
    with open(filename, 'wb') as f:
        f.write(u'\ufeff'.encode('utf8'))
        w = csv.DictWriter(f, fieldnames=title)
        w.writeheader()
        for flowchart in whole_dict:
            for node in whole_dict[flowchart]:
                info_dict = {}
                time_list = whole_dict[flowchart][node]
                time_dict = defaultdict(int)
                for time in time_list:
                    cur_time = math.floor(time)
                    time_dict[cur_time] += 1
                info_dict['flowchart'] = flowchart
                info_dict['node'] = node
                info_dict['days'] = max(time_dict.iteritems(), key=operator.itemgetter(1))[0]
                w.writerow(info_dict)


if __name__ == '__main__':
    filename = 'ajzt.csv'
    whole_dict = group_durations(file_reader(filename))
    sum_duration(whole_dict, 'result_test.csv')
