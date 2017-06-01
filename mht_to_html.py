import re
import email

def insert_image(htm_content,image_dict):
    '''
    @summary: 向HTML文本插入图片
    '''
    for key in image_dict:
        htm_content = re.sub(key,image_dict[key],htm_content)
    return htm_content

def Extractor(MHTContent):
    '''
    @summary: mht转html
    '''
    msg = email.message_from_string( MHTContent )
    htm_content = u""
    image_dict = {}
    for part in msg.walk():
        contenttype = part.get_content_type()
        if contenttype.strip() == "text/html":
            try:
                htm_content = part.get_payload( decode = True ).decode(part.get_charsets()[0],'ignore')
            except:pass
        if "image/" in contenttype:
            image_contnet = part.get_payload()
            image_name = part.get_param("name")
            image_cid = part.get('Content-ID')
            prefix = 'data:%s;base64,'%contenttype
            '''暂时只发现以name和cid引用图片块的这两种方式'''
            image_cid = image_cid.strip('<')
            image_cid = image_cid.strip('>')
            key1 = image_name
            key2 = 'cid:' + image_cid
            value = prefix + image_contnet
            if key1:
                image_dict[key1] = value
            image_dict[key2] = value
    htm_content = insert_image(htm_content, image_dict)
    htm_content = htm_content.replace(u'''<meta http-equiv="Content-Type" content="text/html; charset=gb2312">''', 
                                      u'''<meta http-equiv="Content-Type" content="text/html; charset=utf8">''')
    return  htm_content.encode('utf8')
