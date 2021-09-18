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
        json={"Semester":"1101","CourseNo":"","CourseName":"","CourseTeacher":"","Dimension":"","CourseNotes":"","ForeignLanguage":0,"OnlyGeneral":1,"OnleyNTUST":0,"OnlyMaster":0,"Language":"zh"}
        r=requests.post('https://querycourse.ntust.edu.tw/querycourse/api/courses', json=json)
        print(r.text)
        df = pd.read_json(StringIO(r.text))
        df = df.drop(['Semester', 'RequireOption', 'AllYear', 'ThreeStudent', 'AllStudent', 'NTURestrict', 'Restrict2', 'NTNURestrict', 'CourseTimes', 'ClassRoomNo', 'ThreeNode', 'PracticalTimes', 'Dimension', 'CreditPoint', 'Contents'], axis = 1)
        df.loc[:, 'Rate'] =  df.Restrict1 /  df.ChooseStudent
        df = df.sort_values(by=['Rate'])
        df = df.drop(['Rate'], axis = 1)
        df.Node = df.Node.str.replace(',', '-')
        df = df[df.ChooseStudent < df.Restrict1]
        time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        list_of_files = glob.glob('.\\tmp\\*')
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            last = pd.read_csv(latest_file)
            lastTime = latest_file.split('\\')[-1].rsplit('_', 1)[0]
            lastTime = datetime.datetime.strptime(lastTime, "%Y%m%d_%H%M%S")
            lastTime = str(lastTime)
            df.to_csv(f'./tmp/{time}_course.csv', index=False, encoding='utf-8')
            df = df[df.CourseNo.apply(lambda x: True if x not in list(last.CourseNo) else False)]


            if df.empty:
                added = 'None'
            else:
                added = str(df.values)

            return (lastTime, added, str(list(last.columns)) + str(last.values))
        return '', '', ''
        
        
    except Exception as e:
        print(e)
        with open('err.log', 'a') as f:
            f.write(str(e))





if __name__ == '__main__':
    queryCourse()
