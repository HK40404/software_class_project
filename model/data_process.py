import pandas as pd
import re
import math

def get_class_table():
    '''
        1. 删除爬虫相关列；
        2. 删除课程时间、地点相关的列；
        3. 删除只有时间、地点的行；
        4. 清除专业列中的空白符，将远程授课改为布尔值；
        5. 把学分、学时拆为两列
    '''
    df = pd.read_csv('./scrape_table.csv')
    df = df.drop(columns=['web-scraper-order','web-scraper-start-url','order','week','weekday','classroom'])

    # headers = pd.DataFrame(columns=df.columns)
    # headers.to_csv('./clean_table.csv',mode='w', encoding='utf_8_sig', header=1, index=0)

    for i in range(0, df.shape[0]):
        r = df.loc[i]
        if isinstance(r['name'], str):
            continue
        else:
            # drop()删除之后，仍然占用一个索引
            # 如：drop(0)，之后，访问df.loc[0]会报错，
            # 对除0外的其他索引i，df.loc[i]依旧还是原来的数据
            df.drop(i, inplace=True) 
    
    df['remote'] = df['remote'].map(lambda x: 1 if x == "是" else 0)
    df['major'] = df['major'].map(lambda x: '' if isinstance(x, float) else re.sub('\s|\t|\n','',x))
    df['score'] = df['time/score'].map(lambda x: float(x.split('/')[1]))
    df['time/score'] = df['time/score'].map(lambda x: int(x.split('/')[0]))
    df.rename(columns={"time/score": "time"}, inplace=True) 
    cols = list(df)
    cols.insert(6, cols.pop(cols.index('score')))
    df = df.loc[:, cols]

    df.to_csv('./class_table.csv', mode='w', encoding='utf_8_sig', header=1, index=0)

def get_weekday(weekday):
    '''
        返回二进制的weekday
    '''
    weekday_bin = 0
    weekday = weekday.split(',')
    for w in weekday:
        if w[-1] == '一':
            weekday_bin += 1 << 1
        elif w[-1] == '二':
            weekday_bin += 1 << 2
        elif w[-1] == '三':
            weekday_bin += 1 << 3
        elif w[-1] == '四':
            weekday_bin += 1 << 4
        elif w[-1] == '五':
            weekday_bin += 1 << 5
        elif w[-1] == '六':
            weekday_bin += 1 << 6
        elif w[-1] == '日':
            weekday_bin += 1 << 7
    return weekday_bin

def get_week(week):
    '''
       返回二进制的week 
    '''
    week_bin = 0
    week = week.split(',')
    for n in week:
        if '-' in n:
            begin = int(n.split('-')[0])
            end = int(n.split('-')[1])
            for i in range(begin, end+1):
                week_bin += 1 << i
        else:
            nr = int(n)
            week_bin += 1 << nr
    return week_bin

def get_section(section):
    '''
        返回二进制的section
    '''
    bin_section = 0
    section = section.split(',')
    for sec in section:
        if '-' in sec:
            begin = int(sec.split('-')[0])
            end = int(sec.split('-')[1])
            for i in range(begin, end+1):
                bin_section += 1 << i
        else:
            nr = int(sec)
            bin_section += 1 << nr
    return bin_section

def bin_to_str(bin):
    '''
        解析二进制的数据，用于验证算法是否正确
    '''
    bin = int(bin)
    res = ""
    for i in range(1, 22):
        if bin & (1 << i):
            res += str(i) + " "
    return res

def get_time_table():
    '''
        1. 将时间、地点、课程编号移到正确位置 
        2. 删除时间、地点以外的列
        3. 合并可以合并的条目
        4. 将时间转为二进制形式存储
    '''
    df = pd.read_csv('./scrape_table.csv')
    for i in range(0, df.shape[0]):
        if not isinstance(df.loc[i]['name'], str):
            df.loc[i,'week'] = df.loc[i]['order']
            df.loc[i,'weekday'] = df.loc[i]['school']
            df.loc[i,'classroom'] = df.loc[i]['cid']
            df.loc[i,'cid'] = df.loc[i-1]['cid']
            
    df = df.drop(columns=['web-scraper-order','web-scraper-start-url','order','school','name','attribute','major','time/score','seats','selected','teachmethod','exam','professor','teacher','teachassist','remote'])
    
    df['section'] = df['weekday'].map(lambda x: x.split('(')[1][:-1])
    df['weekday'] = df['weekday'].map(lambda x: x.split('(')[0])
    df['week'] = df['week'].map(lambda x: x[1:-1])

    i = 1
    size = df.shape[0]
    while i < size:
        pre = df.loc[i-1]
        cur = df.loc[i]
        if cur['cid'] == pre['cid'] and cur['weekday'] == pre['weekday'] and \
        cur['classroom'] == pre['classroom'] and cur['week'] == pre['week']:
            df.loc[i,'section'] = pre['section'] + ',' + cur['section']
            df.drop(i-1, inplace=True) 

        elif cur['cid'] == pre['cid'] and cur['weekday'] == pre['weekday'] and \
        cur['classroom'] == pre['classroom'] and cur['section'] == pre['section']:
            df.loc[i,'week'] = pre['week'] + ',' + cur['week']
            df.drop(i-1, inplace=True) 

        elif cur['cid'] == pre['cid'] and cur['week'] == pre['week'] and \
        cur['classroom'] == pre['classroom'] and cur['section'] == pre['section']:
            df.loc[i,'weekday'] = pre['weekday'] + ',' + cur['weekday']
            df.drop(i-1, inplace=True) 
        i += 1

    df.to_csv('./time_table.csv', mode='w', encoding='utf_8_sig', header=1, index=0)
    df = pd.read_csv('./time_table.csv')

    for i in range(0, df.shape[0]):
        weekday = df.loc[i]['weekday']
        df.loc[i,'weekday'] = get_weekday(weekday)
        
        week = df.loc[i]['week']
        df.loc[i,'week'] = get_week(week)

        section = df.loc[i]['section']
        df.loc[i,'section'] = get_section(section)
    
    # df['val_week'] = df['bin_week'].map(lambda x: bin_to_str(x))
    # df['val_section'] = df['bin_section'].map(lambda x: bin_to_str(x))
    # df['val_weekday'] = df['bin_weekday'].map(lambda x: bin_to_str(x))

    cols = list(df)
    cols[-1], cols[-2] = cols[-2], cols[-1]
    df = df.loc[:, cols]

    df.to_csv('./time_table.csv', mode='w', encoding='utf_8_sig', header=1, index=0)

def get_detail_table():
    '''
        1. 删除爬虫相关列；
        2. 删除一些没意义的行；
        3. 
    '''
    # df = pd.read_csv('./scrape_details.csv')
    # for i in range(0, df.shape[0]):
    #     r = df.loc[i]
    #     if isinstance(r['detail'], str):
    #         continue
    #     else:
    #         df.drop(i, inplace=True) 
    # df = df.drop(columns=['web-scraper-order','web-scraper-start-url','link','link-href'])
    # df.to_csv('./detail_table_raw.csv', mode='w', encoding='utf_8_sig', header=1, index=0)
    
    df = pd.read_csv('./detail_table_raw.csv')

    maxs = [0, 0, 0, 0]
    for i in range(0, df.shape[0]):
        detail = df.loc[i]['detail']
        outline_i = detail.find("大纲内容")     # 每个课程详情页都有该字段
        textbook_i = detail.find("教材信息")    # 有的课程详情页没有该字段
        refbook_i = detail.find("参考书")       # 每个课程详情页都有该字段
        teacher_i = detail.find("课程教师信息")  # 每个课程详情页都有该字段
        
        outline = detail[outline_i:textbook_i] if textbook_i != -1 else detail[outline_i:refbook_i]
        outline = outline.strip()
        outline = re.sub("[^\S\n]",'',outline)
        outline = outline[5:]
        f = lambda x: "@" + x.group()
        outline = re.sub("第[\S]章", f, outline)
        outline = re.sub("\n", '，', outline)
        outline = re.sub("@", '\n', outline)
        df.loc[i,'outline'] = outline
        if len(outline) > maxs[0]: maxs[0] = len(outline)

        if textbook_i != -1:
            textbook = detail[textbook_i:refbook_i]
            textbook = textbook.strip()
            textbook = re.sub("[^\S\n]",'',textbook)
            textbook = re.sub("\n\n+",'@',textbook)
            textbook = re.sub("\n",'，',textbook)
            textbook = re.sub("@",'\n',textbook)
            textbook = re.sub("、，",'. ',textbook)
            textbook = textbook[5:]
            df.loc[i,'textbook'] = textbook
            if len(textbook) > maxs[1]: maxs[1] = len(textbook)
        else:
            df.loc[i,'textbook'] = ""

        refbook = detail[refbook_i:teacher_i]
        refbook = refbook.strip()
        refbook = re.sub("[^\S\n]",'',refbook)
        refbook = re.sub("\n\n+",'@',refbook)
        refbook = re.sub("\n",'，',refbook)
        refbook = re.sub("@",'\n',refbook)
        refbook = re.sub("、，",'. ',refbook)
        refbook = refbook[4:]
        df.loc[i,'refbook'] = refbook
        if len(refbook) > maxs[2]: maxs[2] = len(refbook)

        teacher = detail[teacher_i:]
        teacher = teacher.strip()
        teacher = re.sub("[^\S\n]",'',teacher)
        teacher = teacher[7:]
        teacher = re.sub("\n\n+",'\n',teacher)
        df.loc[i,'teacher'] = teacher
        if len(teacher) > maxs[3]: maxs[3] = len(teacher)

        # if(df.loc[i]['cid']=='085700M02005T'):
        #     print(refbook)
        
    print(maxs) # [2859, 157, 2649, 7396]
    df = df.drop(columns=['detail'])
    df.to_csv('./detail_table.csv', mode='w', encoding='utf_8_sig', header=1, index=0)


if __name__ == '__main__':
    # get_class_table()
    # get_time_table()
    get_detail_table()