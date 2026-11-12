import base64, io, glob, os
from PIL import Image
base='/home/user/Mis-Proyectos/artista'
s=open(f'{base}/07-exhibicion/fichas.template.html').read()
for i in range(1,15):
    f=glob.glob(f'{base}/02-fotos-obras/web/2026-{i:02d}_*_web.jpg')[0]
    im=Image.open(f).convert('RGB'); im.thumbnail((180,225))
    b=io.BytesIO(); im.save(b,'JPEG',quality=72)
    s=s.replace('{{t%02d}}'%i,'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode())
open(f'{base}/07-exhibicion/fichas.html','w').write(s)
print(len(s)//1024,'KB')
