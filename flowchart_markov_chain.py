import csv
from collections import defaultdict
import numpy as np
import re


def read_flowchart(filename):
    in_file = open(filename, 'r')
    reader = csv.DictReader(in_file)
    case_list = []
    for row in reader:
        cur_dict = {}
        cur_dict['flowchart'] = row['ID']
        cur_dict['path'] = row['CONTENT']
        case_list.append(cur_dict)
    return case_list


def path_dict(case_list):
    path_dict = {}
    for item in case_list:
        temp = item['path'].split('#')[1].decode('utf8')
        p = ur'\d:(\w+)'
        temp = re.findall(p, temp, flags=re.U)
        for i in temp:
            if item['flowchart'] in path_dict:
                if i not in path_dict[item['flowchart']]:
                    path_dict[item['flowchart']][i] = temp.index(i)
            else:
                path_dict[item['flowchart']] = {}
                path_dict[item['flowchart']][i] = temp.index(i)
    return path_dict


def read_case(filename, path_dict):
    read_file = open(filename, 'r')
    content = csv.DictReader(read_file)
    status_list = []
    n = 0
    for row in content:
        cur_dict = {}
        cur_dict['ID'] = row['ID']
        cur_dict['flowchart'] = row['FLOWCHART_ID']
        cur_dict['node'] = row['NODE_NAME'].decode('utf8')
        cur_dict['time'] = row['START_TIME']
        n += 1
        status_list.append(cur_dict)
    status_list.sort(key=lambda x: x['time'])
    status_dict = defaultdict(lambda: defaultdict(list))
    for item in status_list:
        status_dict[item['flowchart']][item['ID']].append(item['node'])

    matrix_dict = {}

    for fc, subdict in status_dict.iteritems():
        cur_matrix = np.zeros((len(path_dict[fc]), len(path_dict[fc])))
        for v in subdict.values():
            v = map(lambda x: path_dict[fc][x], v)
            for (x, y) in zip(v, v[1:]):
                cur_matrix[x, y] += 1
        matrix_dict[fc] = cur_matrix
    return matrix_dict

if __name__ == '__main__':
    read_case('case_status_info_path.csv', path_dict(read_flowchart('flowcharts.csv')))
