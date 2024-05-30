import torch
from torch.optim import Optimizer
import numpy as np
from typing import Tuple
torch.set_default_dtype(torch.float64)
torch.manual_seed(0) 
printon=False
def mprint(*args):
    if(printon):
        print(*args)
def cubicreg1d(c,b,a,gamma=(np.finfo(np.float32).eps)**(1/8)):
    if(2*np.sqrt(np.abs(a*c))<gamma*np.abs(b)):
        x=4*np.abs(a*c)/(b**2)
        y=0.5*x-(1.0/8.0)*x**2+(1.0/16.0)*x**3-(5.0/128.0)*x**4
        
        if(b<0):
            h0=np.abs(b)*(2+y)/(2*a)
        else:
            h0=np.abs(b)*(y)/(2*a)
        if(c>0):
            h=-h0
        else:
            h=h0
    elif(c>0):
        h=-(-b+np.sqrt(b**2+4*np.abs(a*c)))/(2*a)# 提高这个计算的数值稳定性
    else:
        h=(-b+np.sqrt(b**2+4*np.abs(a*c)))/(2*a)
    return h

# def cubicreg1d(c,b,a,gamma=1e-5):
#     # if(np.sqrt(np.abs(a*c))<gamma*b):
#     #     if(np.abs(b)<gamma):
#     #         h=0
#     #     else:
#     #         h=(c/b)
#     if(c<0):
#         h=-(-b+np.sqrt(b**2+4*np.abs(a*c)))/(2*a)
#     else:
#         h=(-b+np.sqrt(b**2+4*np.abs(a*c)))/(2*a)
#     return h
def _search_alpha(jvp,vhvp,m,M):
        a=M*m
        alpha=cubicreg1d(jvp,vhvp,a)
        return alpha
def tuplemdot(m1: Tuple[torch.Tensor, ...], m2: Tuple[torch.Tensor, ...]) -> torch.Tensor:
    sum0=torch.tensor(0.0,device=m1[0].device)
    for m1a,m2b in zip(m1,m2):
        sum0+=torch.sum(m1a*m2b)
    return sum0
def tuplenorm(m: Tuple[torch.Tensor, ...])-> torch.Tensor:
    return torch.sqrt(tuplemdot(m,m))
def tuplescale(a,m):
    return tuple([a*ma for ma in m])
def tuplelinear(a,m,b,m2):
    return tuple([a*ma+b*mb for ma,mb in zip(m,m2)])


class cubiccgHsapprox(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,alphamin=10*(np.finfo(np.float32).eps),Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgHsapprox, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        self.alphamin=alphamin
        self.alphaprev=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],allow_unused=True,materialize_grads=True )
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
    ## 使用两步法确定步长
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=self.alphamin*self.param_groups[0]["lr"])  # 更新参数
        # hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.enable_grad():
                loss = closure()
        grads2 =torch.autograd.grad(loss,self.param_groups[0]['params'],allow_unused=True,materialize_grads=True )
        jvp2=tuplemdot(grads2,self.prev_direction) # jvp2=jvp1+alphamin*vhvp
        vhvp=(jvp2-jvp)/self.alphamin


        with torch.no_grad():
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(0.5*(jvp+jvp2).item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin
            if(vhvp<0):
                alpha=min(max(alpha,-10*self.alphaprev),10*self.alphaprev)-self.alphamin/2
            else:
                alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin/2
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],allow_unused=True,materialize_grads=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0,device=loss.device)
            sum1=torch.tensor(0.0,device=loss.device)
            for gradsa,da,gradsolda in zip(grads,self.prev_direction,self.prev_grad):
                sum0+=torch.sum(gradsa*(gradsa-gradsolda))
                sum1+=torch.sum(da*(gradsa-gradsolda))
            # if(sum1<0):
            #     pad=-1e-12
            # else:
            #     pad=1e-12
            beta=(sum0/(sum1))*np.sign(alpha)
            mprint("beta",beta)
            self.prev_direction=tuplelinear(-1.0,grads,beta,self.prev_direction)
            # mprint("Vertical detection",tuplemdot(self.prev_direction,grads)/(tuplenorm(self.prev_direction)*tuplenorm(grads)))
            if(loss>self.loss0):
                self.M=min((1+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
                self.alphaprev=abs(alpha)
            self.loss0=loss
        self.prev_grad=grads
        
        return loss,m,alpha,self.M   
 