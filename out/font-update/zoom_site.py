import sys; sys.path.insert(0,'.')
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from layout import load, set_text
old=load('../../brand-site/fonts/FnGuideLogotype-Regular.otf'); new=load('out/FnGuideLogotype-Regular.otf')
lines=sys.argv[2:]; out=sys.argv[1]
fig,ax=plt.subplots(figsize=(13,len(lines)*2.6)); ax.axis('off'); ax.set_aspect('equal')
sc=0.05; y=0
for t in lines:
    for F,col in ((old,'#a0a0a0'),(new,'#b9023d')):
        ps,w=set_text(F,t,0,y+38,sc)
        for p in ps: ax.add_patch(PathPatch(p,fc=col,ec='none'))
        y+=44
    y+=8
ax.set_xlim(-5,330); ax.set_ylim(y,-5)
fig.savefig(out,dpi=75,bbox_inches='tight')
