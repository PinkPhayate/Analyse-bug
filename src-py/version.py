import csv
def get_version_list() :
    f = open('./../slr-version.csv','rb')
    dataReader = csv.reader(f)
    list = []
    for row in dataReader :
        for index in row :
            list.append(index)
    f.close()
    return list

def get_version_short_list() :
    f = open('./../slr-versionc-short.csv','rb')
    dataReader = csv.reader(f)
    list = []
    for row in dataReader :
        for index in row :
            list.append(index)
    f.close()
    return list


def get_next_version(curr_ver):
    vers = get_version_short_list()
    nextVer = ''
    for ver in vers:
        if ver == curr_ver :
            return nextVer
        nextVer = ver
    f.close()

def get_prev_version (curr_ver):
    f = open('./../slr-version-short_bug.csv','rb')
    dataReader = csv.reader(f)
    list = []
    flag = False
    for row in dataReader :
        for index in row :
            if flag :
                return index
            if curr_ver == index :
                flag = True
    f.close()
def get_all_previous_version_list (curr_version) :
    f = open('./../slr-versionc-short.csv','rb')
    dataReader = csv.reader(f)
    list = []
    flag = False
    for row in dataReader :
        # print list
        for index in row :
            if index == curr_version:
                flag = True

            if flag :
                list.append(index)
    return list
    f.close()
