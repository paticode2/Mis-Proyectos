import re,base64,io,glob,sys
from PIL import Image
T=open('collage.template.html').read()
# repo version: relative image paths
open('collage.html','w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',r'img/\1.jpg',T))
# artifact version: embedded thumbnails
cache={}
def emb(m):
    k=m.group(1)
    if k not in cache:
        f=glob.glob(f'../../02-fotos-obras/web/{k}_*_web.jpg')[0]
        im=Image.open(f).convert('RGB'); im.thumbnail((720,720))
        b=io.BytesIO(); im.save(b,'JPEG',quality=78)
        cache[k]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
    return cache[k]
open(sys.argv[1],'w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',emb,T))
