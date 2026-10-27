import sys; sys.path.insert(0,'.')
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from layout import load, set_text
fonts=[('v1.100 (기존)','../../../data/FnGuide-Logotype-Font/fonts/FnGuideLogotype-Regular.otf','#9a9a9a'),('v1.200 (I 기둥 3.91 반영)','out/FnGuideLogotype-Regular.otf','#b9023d')]
lines=["API  FnIndex","HIEFLP  Index  ilnu"]
fig,ax=plt.subplots(figsize=(13,4.8)); ax.axis('off'); ax.set_aspect('equal')
import matplotlib as mpl; mpl.rcParams['font.family']='Malgun Gothic'
sc=0.05; y=0
for t in lines:
    for lab,p,col in fonts:
        F=load(p); ps,w=set_text(F,t,0,y+38,sc)
        for q in ps: ax.add_patch(PathPatch(q,fc=col,ec='none'))
        ax.text(250,y+30,lab,fontsize=10,color='#666')
        y+=44
    y+=8
ax.set_xlim(-5,420); ax.set_ylim(y,-5)
fig.savefig('../v1.200/preview/compare-I-applied.png',dpi=75,bbox_inches='tight')
