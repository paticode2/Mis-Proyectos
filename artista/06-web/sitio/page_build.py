# Uso: python3 page_build.py archivo   -> archivo.html (img/) y, con un 2º argumento, una copia con fotos incrustadas
import re,base64,io,glob,sys
from PIL import Image
name=sys.argv[1]; T=open(f'{name}.template.html').read()
VID=r'\{\{VID:([\w-]+)\}\}'   # videos: img/<nombre>.mp4
open(f'{name}.html','w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',r'img/\1.jpg',re.sub(VID,r'img/\1.mp4',T)))
if len(sys.argv)>2: T=re.sub(VID,lambda m:'data:video/mp4;base64,'+base64.b64encode(open(f'img/{m.group(1)}.mp4','rb').read()).decode(),T)
if len(sys.argv)>2:
    cache={}
    def emb(m):
        k=m.group(1)
        if k not in cache:
            g=glob.glob(f'../../02-fotos-obras/web/{k}_*_web.jpg')
            f=g[0] if g else f'img/{k}.jpg'   # new photos live only in img/
            im=Image.open(f).convert('RGB'); im.thumbnail((720,720) if g else (1000,1000))
            b=io.BytesIO(); im.save(b,'JPEG',quality=78)
            cache[k]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
        return cache[k]
    open(sys.argv[2],'w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',emb,T))
