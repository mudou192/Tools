def guess_img_type(img_content):
      '''参考标准库 imghdr 写的，原模块只接收文件类型，感觉在原基础上改起来更麻烦，自己写个'''
      head = img_content[:32]
      if head[6:10] in ('JFIF','Exif'):
          return 'jpeg'
      if head[:8] == "\211PNG\r\n\032\n":
          return 'png'
      if head[:6] in ('GIF87a', 'GIF89a'):
          return 'gif'
      if head[:2] in ('MM', 'II'):
          return 'tiff'
      if head[:2] == '\001\332':
          return 'rgb'
      if head[0] == 'P' and head[1] in '14' and head[2] in ' \t\n\r':
          return 'pbm'
      if head[0] == 'P' and head[1] in '25' and head[2] in ' \t\n\r':
          return 'pgm'
      if head[0] == 'P' and head[1] in '36' and head[2] in ' \t\n\r':
          return 'ppm'
      if head[:4] == '\x59\xA6\x6A\x95':
          return 'rast'
      if head[:len('#define ')] == '#define ':
          return 'xbm'
      if head[:2] == 'BM':
          return 'bmp'
      return None
