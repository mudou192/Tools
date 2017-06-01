#coding=utf8
'''
Created on 2015-12-22

@author: xhw

@explain: pass
'''
import BaseHTTPServer,SocketServer,cgi,os,urllib,sys
import mimetypes,shutil,posixpath
from cStringIO import StringIO
import HTMLParser


root = r'''E:\51\comlogo'''

class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.do_something_for_get()
            
    def do_POST(self):
        self.do_something_for_post()
        
    def do_something_for_get(self):
        relative_path = self.path[1:]
        relative_path = urllib.unquote(relative_path)
        absolute_path = os.path.join(root,relative_path)
        if os.path.isdir(absolute_path) or self.path == "/":
            try:
                self.file_list(absolute_path)
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        else:
            try:
                self.send_head(absolute_path)
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        
    def do_something_for_post(self):
        relative_path = self.path[1:]
        relative_path = urllib.unquote(relative_path)
        absolute_path = os.path.join(root,relative_path)
        self.save_file(absolute_path)
        
    def save_file(self,absolute_path):
        f = StringIO()
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<Html><h4>Upload finished</h4><br/><br/>")
        PostList = form.keys()
        field = PostList[0]
        field_item = form[field]
        if field_item.filename:
            filename = field_item.filename.split("\\")[-1]
            filename = filename.replace(" ","")
            filename = os.path.join(absolute_path,filename)
            h = HTMLParser.HTMLParser()
            filename = h.unescape(filename)
            if os.path.exists(filename):
                f.write('File <a href="%s">%s</a> The file already exists<br/>' % (urllib.quote(field_item.filename),cgi.escape(field_item.filename)))
            else:
                upfile=open(filename,'wb')
                while 1:
                    file_data=field_item.file.read(1024*4)
                    if not file_data:
                        upfile.close()
                        break
                    upfile.write(file_data)
                f.write('File <a href="%s">%s</a>Upload finished, Size buffer: %d bytes<br/>' % (field_item.filename,field_item.filename,os.path.getsize(filename)))
        f.write('<a href="%s">Back</a></html>'%self.path)
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()
        
    def file_list(self,absolute_path):
        try:
            list = os.listdir(absolute_path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write('''<form enctype="multipart/form-data" action="%s" method="post">\n<p>Choice File:<input type="file" name="file1"></p>\n<p><input type="submit" value="Upload"></p>\n</form>'''%self.path)
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(absolute_path, name)
            displayname = name
            if self.path[-1] == "/":
                linkname = self.path + name
            else:
                linkname = self.path + "/" + name
            if os.path.isdir(fullname):
                displayname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def send_head(self,absolute_path):
        ctype = self.guess_type(absolute_path)
        try:
            f = open(absolute_path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def guess_type(self,path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
    
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({'': 'application/octet-stream', '.py': 'text/plain', '.c': 'text/plain', '.h': 'text/plain',})
    
class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): pass
if __name__ == '__main__':
    server_address = ('0.0.0.0', 8033)
    httpd = ThreadingHTTPServer(server_address, WebHandler)
    print "Web Server On %s:%d" % server_address
    httpd.serve_forever()
