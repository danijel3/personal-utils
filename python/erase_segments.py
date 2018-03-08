import argparse
import wavio
from scipy.io.wavfile import write
from pathlib import Path
import numpy as np

def read_paths(wav_scp,rebase=None):
    if rebase:
        assert type(rebase) is tuple, 'Rebase should be tuple (from->to)!'
    ret={}
    with open(wav_scp) as f:
        for l in f:
            t=l.strip().split(' ')
            path=t[1]
            if rebase:
                path=path.replace(rebase[0],rebase[1])
            ret[t[0]]=Path(path)
    return ret

def read_segments(path):
    ret={}
    with open(path) as f:
        for l in f:
            t=l.strip().split(' ')
            utt=t[0]
            s=float(t[1])
            e=float(t[2])
            if utt not in ret:
                ret[utt]=[]
            ret[utt].append((s,e))
    return ret

def normalize(y,maxval=29000):
    dt=y.dtype
    y-=(y.mean()).astype(dt)
    m=abs(y).max()
    y=(y.astype(float)*maxval/float(m)).astype(dt)
    return y

def find_zero_cross(y,s,shift):
    l=y.shape[0]
    for i in range(shift):        
        if s+i+1>=l:            
            return s+i-1        
        if y[s+i]<=0 and y[s+i+1]>0:            
            return s+i            
    return None

def erase(x,segs,rate,maxshift=0.1, utt=''):
    y=(x.copy()-x.mean()).astype(x.dtype)
    m=np.ones(x.shape).astype(bool)
    for seg in segs:
        s=int(seg[0]*rate)
        e=s+int(seg[1]*rate)
        
        if e<=s:
            continue
                
        ns=find_zero_cross(y,s,int(rate*maxshift))
        if ns == None:
            print("Warning: couldn't find start zero-cross for {}!".format(utt))
            ns=s
        if e<=ns:
            e=ns+1
        ne=find_zero_cross(y,e,int(rate*maxshift))
        if ne == None:
            print("Warning: couldn't find end zero-cross for {}!".format(utt))        
            ne=e
        
        m[ns:ne]=False  
        
    return y[m]


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('erase_segments')
    parser.add_argument('wav_scp')
    parser.add_argument('output_dir')
    parser.add_argument('--mod_scp',required=False)

    args=parser.parse_args()
    
    wav_scp=read_paths(args.wav_scp)
    erase_segs=read_segments(args.erase_segments)
    output_dir=Path(args.output_dir)
    
    if not output_dir.exists():
        output_dir.mkdir()
    
    for utt,segs in erase_segs.items():    
        if utt not in wav_scp:
            print(f'Error: missing file in wav_scp: {utt}')
            continue
            
        path=wav_scp[utt]
        
        y=wavio.read(str(path))
        
        yd=y.data
                
        yn=erase(yd,segs,y.rate,utt=utt)
        
        save_path=output_dir/path.name
        
        wav_scp[utt]=save_path
            
        write(save_path,y.rate,yn)
        
    if args.mod_scp:
        with open(args.mod_scp,'w') as f:
            for utt,path in wav_scp.items():
                f.write(f'{utt} {path.absolute()}\n')