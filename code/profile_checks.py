"""Brownian profile-mass and closed-form checks.

Usage: python -I code/profile_checks.py --out DIR  (writes DIR/brownian_profile_checks.json)
"""
import argparse
from pathlib import Path
import math,json
from scipy.integrate import quad
from scipy.special import ndtr, log_ndtr

def pars(mu,lam,sig):
 k=math.sqrt(mu*mu+2*lam*sig*sig)
 be=(k-mu)/(sig*sig)
 a=(k+mu)/(2*k)
 return k,be,a

def A(t,mu,lam,sig):
 k,be,a=pars(mu,lam,sig)
 return ndtr(k*math.sqrt(t)/sig)+(mu/k)*math.exp(-lam*t)*ndtr(-mu*math.sqrt(t)/sig)

def q(w,T,mu,lam,sig):
 k,be,a=pars(mu,lam,sig)
 if w>=0:return a*be*math.exp(-be*w)
 x=-w
 # stable evaluation of both reflection-principle terms
 term1=math.exp(be*x+log_ndtr(-(x+k*T)/(sig*math.sqrt(T))))
 term2=math.exp((be-2*k/sig**2)*x+log_ndtr(-(x-k*T)/(sig*math.sqrt(T))))
 return a*be*(term1+term2)

out=[]
for mu in [-2,-.5,0,.5,2]:
 for T in [.1,1,4]:
  lam,sig=.7,1.3
  neg=quad(lambda w:q(w,T,mu,lam,sig),-math.inf,0,epsabs=1e-11)[0]
  pos=quad(lambda w:q(w,T,mu,lam,sig),0,math.inf,epsabs=1e-11)[0]
  mass=neg+pos
  an=A(T,mu,lam,sig)
  out.append({'mu':mu,'T':T,'q_integral':mass,'A_formula':an,'abs_error':abs(mass-an)})
  assert abs(mass-an)<1e-9
for T in [.1,1,4]:
 lam=1
 w=math.sqrt(2*lam*T)
 ph=math.exp(-w*w/2)/math.sqrt(2*math.pi)
 numerical=A(T,0,lam,1)+lam/2*quad(lambda s:A(s,0,lam,1),0,T)[0]
 closed=(.75+lam*T/2)*ndtr(w)+math.sqrt(lam*T)/(2*math.sqrt(2))*ph+1/8
 out.append({'C0_T':T,'numerical':numerical,'closed':closed,'abs_error':abs(numerical-closed)})
 assert abs(numerical-closed)<1e-10
ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True,type=Path); args=ap.parse_args()
args.out.mkdir(parents=True,exist_ok=True)
t=args.out/'brownian_profile_checks.json'
if t.exists(): raise SystemExit(f'refusing to overwrite {t}')
t.write_text(json.dumps(out,indent=2)+'\n'); print(f'wrote {t}')
