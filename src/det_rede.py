#!/usr/bin/env python
# coding: utf-8

# In[6]:


from obspy.core import Stream, read
from obspy.signal.trigger import coincidence_trigger
from obspy.signal.trigger import classic_sta_lta
from obspy.signal.trigger import plot_trigger, trigger_onset

from pprint import pprint
import glob
import os
import sys

############################################################
# Dia juliano
j = "063"

# Caminho para os Dados
dados = "../DADOS/2022/"

# Pasta com os possíveis eventos recortados 
path = "../eventos/"

if not os.path.exists(path):
        os.mkdir(path)

##########################################
trigger_on = 5 # o código utiliza  
trigger_off = 2
sta = 0.5
lta = 10

# numero de estações minimas
n = 4
###########################################

fmin = 2
fmax = 20

# Rede e estações
rede = ['LS', 'NB']
estacoes = ['JAC']
############################################################

st = Stream()
files = []
for r in rede:
    files = files + glob.glob(dados + r + "/*/*HHZ*/*" + j)

for f in files:
    for e in estacoes:
        if(e in f):
            st += read(f)

#remove a tendência e filtra             
st.detrend()
st.filter('bandpass', freqmin=fmin, freqmax=fmax)

st2 = st.copy()
trig = coincidence_trigger("recstalta", trigger_on, trigger_off, st2, n, sta=sta, lta=lta,
                          details=True)
#pprint(trig)
    
for d in trig:
    
    start = d['time'] - 5
    end = start + 15
    
    pasta = path + j
    if not os.path.exists(pasta):
        os.mkdir(pasta)
    
    if not os.path.exists(pasta + "/coincidencia/" + str(d['time'])):
        os.makedirs(pasta + "/coincidencia/" + str(d['time']))
    for s in d['stations']:
        for f in files:
            if (s in f):
                st = read(f)
                tr = st.copy()
                tr.trim(start, end)
                tr.write(pasta + "/coincidencia/" + str(d['time'])+"/"+str(s) + ".HHZ", format='SAC')
                
                ff = f.replace('HHZ','HHN')
                st = read(ff)
                tr = st.copy()
                tr.trim(start, end)
                tr.write(pasta + "/coincidencia/" + str(d['time'])+"/"+str(s) + ".HHN", format='SAC')
                
                ff = f.replace('HHZ','HHE')
                ff.replace('HHN','HHE')
                st = read(ff)
                tr = st.copy()
                tr.trim(start, end)
                tr.write(pasta + "/coincidencia/" + str(d['time'])+"/"+str(s) + ".HHE", format='SAC')


# In[ ]:


estacoes


# In[ ]:


dados


# In[ ]:


dados + r + "/*/*HHZ*/*" + j


# In[ ]:




