# Uso: python3 page_build.py archivo   -> archivo.html (img/) y, con un 2º argumento, una copia con fotos incrustadas
import re,base64,io,glob,sys
from PIL import Image
name=sys.argv[1]; T=open(f'{name}.template.html').read()
open(f'{name}.html','w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',r'img/\1.jpg',T))
if len(sys.argv)>2:
    cache={}
    def emb(m):
        k=m.group(1)
        if k not in cache:
            f=glob.glob(f'../../02-fotos-obras/web/{k}_*_web.jpg')[0]
            im=Image.open(f).convert('RGB'); im.thumbnail((720,720))
            b=io.BytesIO(); im.save(b,'JPEG',quality=78)
            cache[k]='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
        return cache[k]
    open(sys.argv[2],'w').write(re.sub(r'\{\{IMG:([\d-]+)\}\}',emb,T))
