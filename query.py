import datetime
import requests
import pandas as pd
from io import StringIO
import glob
import os
import json
def querySex(arg)->list:
    if arg == 'popular':
        arg = 'true'
    elif arg == 'newest':
        arg = 'false'
    else:
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
        r = requests.get(f'https://www.dcard.tw/service/api/v2/posts/{arg}', headers=headers)
        jsons = json.loads(r.text)
        'error' in jsons.keys()
        return jsons


        
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
    params={'limit':100, 'popular':arg}
    r = requests.get('https://www.dcard.tw/service/api/v2/forums/sex/posts', headers=headers, params=params)
    print(r.text)
    jsons = json.loads(r.text)
    posts = []
    for i in jsons:
        if (i['gender']) == 'F':
            tmp = {}
            if (i['media']):
                tmp['id'] = (i['id'])
                tmp['title'] = (i['title'])
                tmp['excerpt'] = (i['excerpt'])
                tmp['link'] = f"https://www.dcard.tw/f/sex/p/{i['id']}"
                s = ''
                for j in i['media']:
                    s = j['url'] + '\n'
                tmp['url'] = s
                posts.append(tmp)
    return posts
def queryCourse():

    try:
        json={"Semester":"1101","CourseNo":"","CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":1,"OnleyNTUST":1,"OnlyMaster":0,"Language":"zh"}
        r=requests.post('https://querycourse.ntust.edu.tw/querycourse/api/courses', json=json)
        df = pd.read_json(StringIO(r.text))
        df = df.drop(['Semester', 'RequireOption', 'AllYear', 'ThreeStudent', 'AllStudent', 'NTURestrict', 'Restrict2', 'NTNURestrict', 'CourseTimes', 'ClassRoomNo', 'ThreeNode', 'PracticalTimes', 'Dimension', 'CreditPoint', 'Contents'], axis = 1)
        df.loc[:, 'Rate'] =  df.Restrict1 /  df.ChooseStudent
        df = df.sort_values(by=['Rate'])
        df = df.drop(['Rate'], axis = 1)
        df.Node = df.Node.str.replace(',', '-')
        df = df[df.ChooseStudent < df.Restrict1]
        return (str(list(df.columns)) + str(df.values))
        
        
    except Exception as e:
        print(e)
        with open('err.log', 'a') as f:
            f.write(str(e))





if __name__ == '__main__':
    queryCourse()
