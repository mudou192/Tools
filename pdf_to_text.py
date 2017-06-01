#coding=utf8
'''
Created on 2017-1-3

@author: xuwei

@summary: 
'''
import threading
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

lockObject = threading.Lock()

def Extractor(sourcefile, outfile):
    lockObject.acquire()
    try:
        fp = file(sourcefile, 'rb')
        outfp=file(outfile,'w')
        #创建一个PDF资源管理器对象来存储共享资源
        #caching = False不缓存
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)
        #创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        #关闭输入流
        fp.close()
        #关闭输出流
        device.close()
        outfp.flush()
        outfp.close()
    except Exception, e:
        print "Exception:%s",e
    finally:
        #注意一定要释放锁，否则程序出异常时，会死掉
        lockObject.release()
        
if __name__ == "__main__":
    AA = Extractor("80.pdf",'test.txt')
