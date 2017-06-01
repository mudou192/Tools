#coding=utf8
'''
Created on 2016-12-30

@author: xuwei

@summary: 
'''
import re,chardet,traceback
import threading
import win32com.client

lockObject = threading.Lock()
msWord = None

def Extractor(wordfile,txtfile):
    lockObject.acquire()
    wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")
    try:
        wordapp.Documents.Open(wordfile)
        wordapp.ActiveDocument.SaveAs(txtfile,FileFormat = win32com.client.constants.wdFormatText)
        wordapp.ActiveDocument.Close()
        with open(txtfile,'rb') as fp:
            Content = fp.read()
        try:
            encodeDict = chardet.detect( Content )
        except:
            encodeDict = {}
            encodeDict['encoding'] = 'gb18030'

        if encodeDict['encoding']:
            if not re.findall( '(?is)^utf', encodeDict['encoding'] ):
                encodeDict['encoding'] = 'gb18030'
        else:
            encodeDict['encoding'] = 'gb18030'
        try:
            Content = Content.decode(encodeDict['encoding'],'ignore')
        except Exception,e:
            pass
        with open(txtfile,'wb') as fp:
            fp.write(Content)
    except:
        traceback.print_exc()
        wordapp.Quit()
    finally:
        lockObject.release()
    
if __name__ == "__main__":
    Extractor(r"E:\work_space\ImportResume\turn_file_type\2112834156300808.doc",r'E:\work_space\ImportResume\turn_file_type\test.txt')
