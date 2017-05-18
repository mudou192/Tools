#coding=utf8
'''
Created on 2017-5-17

@author: xuwei

@summary: 任务调度
'''
import time
import threading

class Wheel(object):
    def __init__(self,warn_call = None):
        # 超时警告回调函数
        self.warn_call = warn_call
        # 循环间隔时间
        self.sleep = 5
        self.tasks = {}
        
    def add_task(self,module,**kwargs):
        module.init_timer()
        if self.tasks:
            maxid = max(self.tasks)
        else:
            maxid = -1
        self.tasks[maxid + 1] = module
    
    def warn_timeout(self,taskname):
        if self.warn_call:
            self.warn_call('Timeout Warning: %s run timeout'%taskname) 
        
    def run(self):
        while 1:
            for task_id in self.tasks:
                nowtime = time.time()
                module = self.tasks[task_id]
                if module.stop or module.runtime > nowtime:
                    continue
                if module.isrunning and nowtime - module.starttime > module.timeout:
                    self.warn_timeout(module.taskname)
                    continue
                if not module.isrunning and nowtime > module.runtime:
                    module.start()
            time.sleep(self.sleep)
    
    def view_task(self):
        print "=" * 60
        for task_id in self.tasks:
            obj = self.tasks[task_id]
            taskname = obj.taskname
            stop = obj.strop
            state = obj.isrunning
            print "taskId: %3s  state:%8s    stop:%8s    taskname:%s"%(str(task_id),str(state),str(stop),str(taskname))
            
    def stop_command(self):
        cmd = raw_input('Please enter the task ID:')
        cmd = cmd.strip().lower()
        while 1:
            if not cmd.isalnum() or int(cmd) not in self.tasks:
                cmd = raw_input('Please enter the correct task ID:')
                cmd = cmd.strip().lower()
            elif cmd == 'q':
                break
            else:
                obj = self.tasks.get(int(cmd))
                if obj.strop:
                    obj.strop = False
                else:
                    obj.strop = True
    
    def command(self):
        cmd = raw_input('[Enter] view task    [s] stop/start command    [q] quit\n')
        cmd = cmd.strip().lower()
        while 1:
            if cmd == 's':
                self.stop_command()
                cmd = raw_input('[Enter] view task    [s] stop/start command    [q] quit\n')
            else:
                cmd = raw_input('[Enter] view task    [s] stop/start command    [q] quit\n')
    
    def start(self):
        task_thread = threading.Thread(target=self.run)
        task_thread.setDaemon(True)
        task_thread.start()
        self.command()
