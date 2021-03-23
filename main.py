import csv
import pandas as pd
import emojiswitch as ej
import first_sentiment as fs
import second_summary as ss
import third_tag as tt
import fourth_textsim as ft
from time import ctime
import time
import threading



class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def dur( op=None, clock=[time.time()] ):
    if op != None:
        duration = time.time() - clock[0]
        print('%s finished. Duration %.6f seconds.' % (op, duration))
        clock[0] = time.time()


if __name__ == '__main__':
    """
        这里我认为我们可以将输入文件做一定的处理 可以符合我们的Powerpoint中输入形式 主要分为三列 
        (1)关键词/主题
        (2)标题
        (3)内容
        (4)文本相似度
    """
    # 我们读入本地的标准输入文件
    # 我们本地中有两个输入文件 inputdemo和inputData的文件
    dur()
    input_file = pd.read_csv('./inputdemo.csv')
    # 我们先对文本进行一定的预处理 我们需要将标题和内容列的文本把表情转换为中文
    # 我们这里利用了我们的emojiswitch将表情转换为中文，然后再调用API进行NLP处理
    # list1代表的是标题列 list2代表的是内容列 list3是话题/关键词
    list1 = []
    list2 = []
    list3 = []
    for k in input_file['关键词']:
        list3.append(k)

    for i in input_file['标题']:
        if pd.isna(i):
            list1.append(" ")
            continue
        else:
            i = ej.demojize(i,lang="zh")
            list1.append(i)

    for j in input_file['内容']:
        if pd.isna(j):
            list2.append(" ")
            continue
        else:
            j = ej.demojize(j, lang="zh")
            list2.append(j)

    dct = [list3,list1,list2]
    dct = pd.DataFrame(dct).T
    dct.columns = ['关键词','标题','内容']

    # 我们这里需要转转换思路 用字典会给后续循环调用带来麻烦

    # 最好是能一行行的循环访问，但是我们这里碰到一点并发的问题 所以根据我们的输入选项

    # 我们可以在这里加入一个选项就是我们可以利用switch语句去进行选择我们需要输出的的内容

    # 根据我们的输出内容分为四项（1）情绪判断以及置信区间 （2）摘要 （3）标签以及标签权重 （4）文本相似度

    """
        文本处理完毕 接下来我们需要调用接口进行处理 根据我们的输出项 我们的需要三种API
        第一种是情绪判断以及置信区间
        第二种是摘要
        第三种是标签及其权重
        第四种是文本相似度
    """

    fs_list = [[],[]]
    ss_list = []
    tt_list = [[],[]]
    ft_list = [[],[]]

    for i in range(0,5):

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>欢迎来到小红书数据分析平台 我们根据输入文件的话题标题内容三项，我们根据我们接口可以进行如下选择>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>输入1：分析兴趣     得到倾向以及倾向置信区间")
        print(">>>输入2: 分析摘要    得到最大值不超过50个字的摘要")
        print(">>>输入3: 分析文章标签 得到文章标签以及权重")
        print(">>>输入4: 分析相似文本 得到相似文本以及文本的相似度")
        print(">>>输入5：输出所有选项并且跳出循环 将输出结果写入到本地文件")
        print(">>>输入6: 结束循环 我们将输出结果写入到本地的文件")
        print(">>>我们最多只提供5次输入机会")
        temp = input("请输入您想进行的操作: ")
        if temp == "1":
            # 我觉得我们这里可以直接子函数内部循环 然后让函数返回一个字典
            # fs_list = []
            fs_list = fs.get_classify(list2)
            print(fs_list[1])
        elif temp == "2":
            # ss_list = []
            ss_list = ss.summary(list1,list2,50)
            print(ss_list)
        elif temp == "3":
            # tt_list = []
            tt_list = tt.tag(list1,list2)
            print(tt_list[0])
            print(tt_list[1])
        elif temp == "4":
            #文章的相似度接口有些特殊 我们不能直接用先用的列表我们首先需要把输入的数据按照关键词进行分类
            contem = list(dct.groupby('关键词'))
            # print(contem)
            ft_list = ft.textsim(contem)
        elif temp =="5":
            time_start = time.time()
            # threads = []
            # threads.append(MyThread(fs.get_classify, args=(list2,)))
            # threads.append(MyThread(ss.summary,args=(list1,list2,50)))
            # threads.append(MyThread(tt.tag,args=(list1,list2)))
            # threads.append(threading.Thread(target=ft.textsim,args=(contem,)))
            # test_list = []
            # for t in threads:
            #     t.start()
            #     t.join()
            #     print(t.get_result())
            more_th1 = MyThread(fs.get_classify, (list2,))
            more_th2 = MyThread(ss.summary, (list1,list2,50))
            more_th3 = MyThread(tt.tag, (list1,list2))

            more_th1.daemon = True
            more_th2.daemon = True
            more_th3.daemon = True

            # 启动线程
            more_th1.start()
            more_th2.start()
            more_th3.start()

            # 线程等待（即：等待三个线程都运行完毕，才会执行之后的代码）
            more_th1.join()
            more_th2.join()
            more_th3.join()
            # 输出线程执行方法后的的返回值
            fs_list = more_th1.get_result()
            ss_list = more_th2.get_result()
            tt_list = more_th3.get_result()

            # fs_list = fs.get_classify(list2)
            # # print(fs_list[1])
            # ss_list = ss.summary(list1, list2, 50)
            # # print(ss_list)
            # tt_list = tt.tag(list1, list2)
            # print(tt_list[0])
            # print(tt_list[1])
            contem = list(dct.groupby('关键词'))
            ft_list = ft.textsim(contem)
            print("all over %s" % ctime())
            break
        elif temp == "6":
            break
        else:
            print("请输入合法的指令")
    # print(list3)
    # print("<<<")
    # print(list1)
    # print("<<<")
    # print(list2)
    print("<<<")
    print(fs_list[0])
    print("<<<")
    print(fs_list[1])
    print("<<<")
    print(ss_list)
    print("<<<")
    print(tt_list[0])
    print("<<<")
    print(tt_list[1])
    print("<<<")
    print(ft_list[1])
    print("<<<")
    print(ft_list[0])

    # with open("./result.csv","w") as csvfile:
    #     writer = csv.writer(csvfile)
    #     #先写入列名
    #     writer.writerow(['关键词','标题','内容','倾向','倾向置信区间','摘要','标签','标签权重','相似文本','相似度'])
    dataframe = pd.DataFrame.from_dict({'关键词':list3,'标题':list1,'内容':list2,'倾向':fs_list[0],
                              '倾向置信区间':fs_list[1],'摘要':ss_list,'标签':tt_list[0],
                              '标签权重':tt_list[1],'相似文本':ft_list[1],'相似度':ft_list[0]},orient="index")
    dataframe.T.to_csv("./outputdemo.csv",sep=",",index=False)

    dur('all finished!')









