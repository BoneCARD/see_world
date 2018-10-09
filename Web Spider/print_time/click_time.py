import datetime
import re
# import difflib
# cmp = difflib.Differ()
str_time1 = '2018-9-7'
str_time2 = 'Oct 3, 2018'
str_time3 = 'October 1, 2018'
str_time4 = '2018年1月5日'

# _ ==>>  _
# __ ==>> -
# ___ ==>> ,
# K ==>> 空格

def TY__m__d(n): ## 2018-10-03
    return (datetime.datetime.now() + datetime.timedelta(days=-n)).strftime("%Y-%m-%d")
def TbKd___KY(n): ## Oct 03, 2018
    return (datetime.datetime.now() + datetime.timedelta(days=-n)).strftime("%b %d, %Y")
def TBKd___KY(n): ## October 03, 2018
    return (datetime.datetime.now() + datetime.timedelta(days=-n)).strftime("%B %d, %Y")
def judef_lon(month):
    Month = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for mo in Month:
        if (month.encode('utf-8')==mo.encode('utf-8')):
            return True
    return False
def judef_sho(month):
    Month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    # print(month)
    for mo in Month:
        if(month.encode('utf-8')==mo.encode('utf-8')):
            return True
        # print("NO")
    return False

def judge(you,add=0,mhave_0=0,dhave_0=0):
    your = (datetime.datetime.now() + datetime.timedelta(days=-add))
    # print(you=='2018年8月31日')
    if((mhave_0!=1) & (dhave_0!=1)):    #0 0
        ########## 2018年1月4日
        if(re.search('([0-9]{4})年',you)):
            if(bool(re.search('(0[0-9])',your.strftime("%d"))) & bool(re.search('0([0-9])',your.strftime("%m")))):
                return (your.strftime("%Y")+'年'+re.findall('0([0-9])',your.strftime("%m"))[0]+'月'+re.findall('0([0-9])',your.strftime("%d"))[0]+'日')
            if (bool(re.search('(0[0-9])', your.strftime("%d")))):
                return (your.strftime("%Y") + '年' + your.strftime("%m") + '月' + re.findall('0([0-9])', your.strftime("%d"))[0] + '日')
            if (bool(re.search('0([0-9])', your.strftime("%m")))):
                return (your.strftime("%Y") + '年' + re.findall('0([0-9])', your.strftime("%m"))[0] + '月' + your.strftime("%d")+ '日')
        ########## 2018-1-3
        if (re.search('([0-9]{4})+-', you)):
            if(bool(re.search('(0[0-9])',your.strftime("%d"))) & bool(re.search('0([0-9])',your.strftime("%m")))):
                return (your.strftime("%Y")+'-'+re.findall('0([0-9])',your.strftime("%m"))[0]+'-'+re.findall('0([0-9])',your.strftime("%d"))[0])
            if (bool(re.search('(0[0-9])', your.strftime("%d")))):
                return (your.strftime("%Y") + '-' + your.strftime("%m") + '-' + re.findall('0([0-9])', your.strftime("%d"))[0])
            if (bool(re.search('0([0-9])', your.strftime("%m")))):
                return (your.strftime("%Y") + '-' + re.findall('0([0-9])', your.strftime("%m"))[0] + '-' + your.strftime("%d"))
            # return your.strftime("%Y-%m-%d")
        ########## October 3, 2018
        if (judef_lon(re.findall('[a-zA-Z]*', you)[0])):
            # print(2)
            if (re.findall('0([0-9])', your.strftime("%d"))):
                return (your.strftime("%B ")+ re.findall('0([0-9])', your.strftime("%d"))[0]+ your.strftime(", %Y"))
            else:
                return your.strftime("%B %d, %Y")
        ########## Oct 1, 2018
        if (judef_sho(re.findall('([a-zA-Z]{3})', you)[0])):
            # print(3)
            if (re.findall('0([0-9])', your.strftime("%d"))):
                return (your.strftime("%b ")+ re.findall('0([0-9])', your.strftime("%d"))[0]+ your.strftime(", %Y"))
            else:
                return your.strftime("%b %d, %Y")
    if((mhave_0==1) & (dhave_0==1)):    #1 1
        ########## 2018年01月04日
        if(re.search('([0-9]{4})年',you)):
            return (your.strftime("%Y")+'年'+your.strftime("%m")+'月'+your.strftime("%d")+'日')
        ########## 2018-10-03
        if (re.search('([0-9]{4})+-', you)):
            return your.strftime("%Y-%m-%d")
    if((mhave_0!=1) & (dhave_0==1)):    #0 1
        ########## 2018年1月04日
        # print(1)
        if (re.search('([0-9]{4})年([0-9]{1})月([0-9]{2})日', you)):
            if(re.findall('年0([0-9])',your.strftime("%m"))):
                return (your.strftime("%Y") + '年' + re.findall('0([0-9])',your.strftime("%m"))[0] + '月' + your.strftime("%d") + '日')
            else:
                return (your.strftime("%Y")+'年'+your.strftime("%m")+'月'+your.strftime("%d")+'日')
        ########## 2018-1-03
        if (re.search('([0-9]{4})+-', you)):
            if (re.findall('0([0-9])', your.strftime("%m"))):
                return (your.strftime("%Y") + '-' + re.findall('0([0-9])', your.strftime("%m"))[0] + '-' + your.strftime("%d"))
            else:
                return your.strftime("%Y-%m-%d")
        ########## October 03, 2018
        if (judef_lon(re.findall('[a-zA-Z]*', you)[0])):
            return your.strftime("%B %d, %Y")
        ########## Oct 03, 2018
        if (judef_sho(re.findall('([a-zA-Z]{3}) ', you)[0])):
            return your.strftime("%b %d, %Y")
    # if(dhave_0!=1):                     #1 0
        # ########## October 3, 2018
        # if (judef_lon(re.findall('[a-zA-Z]*', you)[0])):
        #     # print(2)
        #     if (re.findall('0([0-9])', your.strftime("%d"))):
        #         return (your.strftime("%B ")+ re.findall('0([0-9])', your.strftime("%d"))[0]+ your.strftime(", %Y"))
        #     else:
        #         return your.strftime("%B %d, %Y")
        # ########## Oct 1, 2018
        # if (judef_sho(re.findall('([a-zA-Z]{3})', you)[0])):
        #     # print(3)
        #     if (re.findall('0([0-9])', your.strftime("%d"))):
        #         return (your.strftime("%b ")+ re.findall('0([0-9])', your.strftime("%d"))[0]+ your.strftime(", %Y"))
        #     else:
        #         return your.strftime("%b %d, %Y")

    # ########## 2018-10-03
    # if(re.search('([0-9]{4})+-',you)):
    #     if(re.search('-([0-9]{2})',you)):
    #         # return (datetime.datetime.now().strftime("%Y-%m-%d"))
    #         # print('Y-m-d')
    #         return your.strftime("%Y-%m-%d")

    # ########## Oct 03, 2018
    # if(judef_sho(re.findall('([a-zA-Z]{3}) ',you)[0])):
    #     # return (datetime.datetime.now().strftime("%b %d, %Y"))
    #     stt = ''
    #     if(re.findall(' ([0-9]{2}),',you)):
    #         # print('b 0d, Y')
    #         return your.strftime("%b %d, %Y")
    #     else:
    #         if(re.findall('0([0-9])',your.strftime('%d'))):
    #             stt = stt + your.strftime("%b ") + re.findall('0([0-9])',your.strftime('%d'))[0] + your.strftime(", %Y")
    #             # print('b d, Y')
    #             return stt
    #         else:
    #             # print('b 0d, Y')
    #             return your.strftime("%b %d, %Y")
    # ########## October 03, 2018
    # if (judef_lon(re.findall('[a-zA-Z]*', you)[0])):
    #     # return your.strftime("%B %d, %Y")
    # ##############################
    #     stt = ''
    #     if (re.findall(' ([0-9]{2}),', you)):
    #         # print('B 0d, Y')
    #         return your.strftime("%B %d, %Y")
    #     else:
    #         if (re.findall('0([0-9])', your.strftime('%d'))):
    #             stt = stt + your.strftime("%B ") + re.findall('0([0-9])', your.strftime('%d'))[0] + your.strftime(", %Y")
    #             # print('B d, Y')
    #             return stt
    #         else:
    #             # print('B 0d, Y')
    #             return your.strftime("%B %d, %Y")
    ##############################
    print(you+" : 有新的时间格式了，回来加吧")
    return None

def day_span(you,mhave_0,dhave_0):

    n = 0
    while(str(you).encode('utf-8')!=str(judge(you,n,mhave_0,dhave_0)).encode('utf-8')):
        n = n + 1
        if (n==366):break
    else:
        print('span =', n)
        return n
    # try:
    #     n = 0
    #     while(str(you).encode('utf-8')!=str(judge(you,n,mhave_0,dhave_0)).encode('utf-8')):
    #         n = n + 1
    #         if (n==366):break
    #     else:
    #         print('span =', n)
    #         return n
    # except(IndexError):
    #     print("IndexError")
    #     return -1
    # print(you.encode('utf-8'),judge(you,n).encode('utf-8'))
    return -1

# print(day_span(str_time3))
if __name__ == '__main__':
    # print('day:',day_span(str_time3))
    # print(re.findall(' 0([0-9]),','Oct 03, 2018'))
    # print(re.findall('0([0-9])',(datetime.datetime.now() + datetime.timedelta(days=0)).strftime('%d')))
    # print(re.search('([0-9]{4})年([0-9]{2})月([0-9]{2})日',str_time4))
    add = 30
    # your = (datetime.datetime.now() + datetime.timedelta(days=-add))
    # print(your.strftime("%m %d, %Y"))
    print(judge(str_time1,add,0,0))