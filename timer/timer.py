#coding=utf8
'''
Created on 2017-5-17

@author: xuwei

@summary: 定时任务对象，所有定时任务都继承该对象
'''
import time
import threading
# 这里月没有处理那么细致，2月需要注意
MONTH_LENGTH = [31,28,31,30,31,30,31,31,30,31,30,31]

class Timer(object):
    def __init__(self):
        # 当前任务名称
        self.taskname = ''
        self.isrunning = False
        # 当self.stop == True 时，该任务不再执行
        self.stop = False
        self.interval = None
        self.date = None
        self.week = None
        self.hour = 0
        self.minute = 0
        self.timeout = None
        self.runtime = 0
        self.starttime = 0
    
    def init_timer(self,**kwargs):
        """
        @summary: 初始化定时
        @param interval: 定时间隔，单位秒，与除了超时字段的其他字段互斥
        @param date: 一个月的某一号，与interval，week互斥
        @param week: 一周的某一天，与interval，date互斥
        @param hour: 某一时，对于date/week存在时，是必须字段
        @param minute: 某一分钟
        @param timeout: 任务超时时间（默认 9999999）
        """
        self.interval = kwargs.get('interval')
        self.date = kwargs.get('date')
        self.week = kwargs.get('week')
        if kwargs.get('hour'):
            self.hour = kwargs.get('hour')
        if kwargs.get('minute'):
            self.minute = kwargs.get('minute')
        self.timeout = kwargs.get('timeout')
        if not self.timeout:
            self.timeout = 9999999
        self.cal_last_run_time()
            
    def cal_date_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        nowmonth = int(time.strftime('%m'))
        nowdate = int(time.strftime('%d'))
        nowhour = int(time.strftime('%H'))
        nowminute = int(time.strftime('%M'))
        if self.date < nowdate and self.hour < nowhour:
            adddays = MONTH_LENGTH[nowmonth - 1] - (nowdate - self.date)
        elif self.date == nowdate and self.hour < nowhour and self.minute < nowminute:
            adddays = MONTH_LENGTH[nowmonth - 1]
        else:
            adddays = self.date - nowdate
        return todaytime + adddays * 86400 + self.hour * 3600 + self.minute * 60
            
    def cal_week_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        nowweek = int(time.strftime('%w'))
        nowhour = int(time.strftime('%H'))
        nowminute = int(time.strftime('%M'))
        if self.week < nowweek and self.hour < nowhour:
            adddays = 7 - (nowweek - self.week)
        elif self.week ==  nowweek and self.hour < nowhour and self.minute < nowminute:
            adddays = 7
        else:
            adddays = self.week - nowweek
        return todaytime + adddays * 86400 + self.hour * 3600 + self.minute * 60
    
    def cal_hour_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        nowhour = int(time.strftime('%H'))
        nowminute = int(time.strftime('%M'))
        if self.hour < nowhour:
            addhours = 24 - (nowhour - self.hour)
        elif self.hour == nowhour and self.minute < nowminute:
            addhours = 24
        else:
            addhours = self.hour - nowhour
        return todaytime + nowhour * 3600 + addhours * 3600 + self.minute * 60
    
    def cal_minute_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d %H'), '%Y-%m-%d %H'))
        nowminute = int(time.strftime('%M'))
        if self.minute <= nowminute:
            addminute = 60 - (nowminute - self.minute)
        else:
            addminute = self.minute - nowminute
        return todaytime + nowminute * 60 + addminute * 60
        
    def cal_last_run_time(self):
        """计算下一次运行的时间，在任务运行完毕或任务加载时执行"""
        nowtime = time.time()
        if self.interval and not self.runtime:
            self.runtime = nowtime
        elif self.interval and self.runtime:
            self.runtime = nowtime + self.interval
        elif self.date:
            self.runtime = self.cal_date_time()
        elif self.week:
            self.runtime = self.cal_week_time()
        elif self.hour:
            self.runtime = self.cal_hour_time()
        elif self.minute:
            self.runtime = self.cal_minute_time()
        else:
            raise Exception('wrong time format')
        print "self.runtime:",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.runtime))
        
    def _run(self):
        self.starttime = time.time()
        self.isrunning = True
        self.run()
        self.cal_last_run_time()
        self.isrunning = False
        
    def start(self):
        task_thread = threading.Thread(target=self._run)
        task_thread.setDaemon(True)
        task_thread.start()
        time.sleep(2)
        
    def run(self):
        """任务运行主函数，需要自己捕捉异常，否则可能导致该任务一直阻塞"""
        print 'do something...',time.strftime('%Y-%m-%d %H:%M:%S')
        
if __name__ == "__main__":
    T = Timer()
    T.init_timer(minute = 5, hour = 17, week = 7)
