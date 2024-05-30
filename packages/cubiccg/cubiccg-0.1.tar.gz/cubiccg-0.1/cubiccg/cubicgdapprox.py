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

#实现adam算法
class CustomAdam(torch.optim.Optimizer):
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8):
        defaults = dict(lr=lr, betas=betas, eps=eps)
        super(CustomAdam, self).__init__(params, defaults)

    def step(self, closure=None):
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad
                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    state['m'] = torch.zeros_like(p)
                    state['v'] = torch.zeros_like(p)

                m, v = state['m'], state['v']
                beta1, beta2 = group['betas']

                state['step'] += 1
                state['m'] = beta1 * m + (1 - beta1) * grad
                state['v'] = beta2 * v + (1 - beta2) * grad * grad

                m_hat = state['m'] / (1 - beta1 ** state['step'])
                v_hat = state['v'] / (1 - beta2 ** state['step'])

                update = -group['lr'] * m_hat / (torch.sqrt(v_hat) + group['eps'])
                p.data.add_(update)


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
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin
            if(vhvp<0):
                alpha=min(max(alpha,-10*self.alphaprev),10*self.alphaprev)-self.alphamin
            else:
                alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin
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
    
# beta=0 退化为梯度下降
class cubicGD(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubicGD, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0)
            sum1=torch.tensor(0.0)
            for gradsa,gradsolda in zip(grads,self.prev_grad):
                sum0+=torch.sum(gradsa*(gradsa-gradsolda))
                sum1+=torch.sum(gradsolda*gradsolda)
            beta=0
            mprint("beta",beta)
            self.prev_direction=tuplelinear(1,grads,beta,self.prev_direction)
            mprint("Vertical detection",tuplemdot(self.prev_direction,grads)/(tuplenorm(self.prev_direction)*tuplenorm(grads)))
            if(loss>self.loss0):
                self.M=min((1+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha
    
# 立方正则化共轭梯度法HS方向
class cubiccgHs(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgHs, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
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
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha,self.M   
    

class cubiccgPRP(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgPRP, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0)
            sum1=torch.tensor(0.0)
            for gradsa,gradsolda in zip(grads,self.prev_grad):
                sum0+=torch.sum(gradsa*(gradsa-gradsolda))
                sum1+=torch.sum(gradsolda*gradsolda)
            beta=(sum0/sum1)*np.sign(alpha)
            mprint("beta",beta)
            self.prev_direction=tuplelinear(-1.0,grads,beta,self.prev_direction)
            # mprint("Vertical detection",tuplemdot(self.prev_direction,grads)/(tuplenorm(self.prev_direction)*tuplenorm(grads)))
            if(loss>self.loss0):
                self.M=min((1+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha,self.M
    
class cubiccgMPRP(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgMPRP, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0)
            sum1=torch.tensor(0.0)
            sum2=torch.tensor(0.0)
            yk=tuplelinear(1.0,grads,-1,self.prev_grad)
            for gradsa,gradsolda,da in zip(grads,self.prev_grad,self.prev_direction):
                sum0+=torch.sum(gradsa*(gradsa-gradsolda))
                sum1+=torch.sum(gradsolda*gradsolda)
                sum2+=torch.sum(gradsa*da)
            beta=(sum0/sum1)
            theta=(sum2/sum1)
            mprint("beta",beta)
            dir0=tuplelinear(-1.0,grads,beta,self.prev_direction)
            self.prev_direction=tuplelinear(1.0,dir0,-theta,yk)
            # mprint("Vertical detection",tuplemdot(self.prev_direction,grads)/(tuplenorm(self.prev_direction)*tuplenorm(grads)))
            if(loss>self.loss0):
                self.M=min((0+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha,self.M

class cubiccgDESCENT(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgDESCENT, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0)
            sum2=torch.tensor(0.0)
            sum1=torch.tensor(0.0)
            for gradsa,da,gradsolda in zip(grads,self.prev_direction,self.prev_grad):
                sum1+=torch.sum(da*(gradsa-gradsolda))
                sum2+=torch.sum((gradsa-gradsolda)*(gradsa-gradsolda))
            tdk=2*sum2/sum1
            for gradsa,da,gradsolda in zip(grads,self.prev_direction,self.prev_grad):
                sum0+=torch.sum(gradsa*(gradsa-gradsolda-tdk*da))
            # if(sum1<0):
            #     pad=-1e-12
            # else:
            #     pad=1e-12
            beta=(sum0/(sum1))
            mprint("beta",beta)
            self.prev_direction=tuplelinear(-1.0,grads,beta,self.prev_direction)
           
            if(loss>self.loss0):
                self.M=min((1+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha
    

class cubiccgDY(Optimizer):
    def __init__(self, params, lr=1.0,M=1e-9,alphamax=10,Mmin=1e-9,Mmax=1e5,Mbeta=2,Mgamma=None):
        defaults = dict(lr=lr)
        super(cubiccgDY, self).__init__(params, defaults)
        self.prev_grad = None  # 使用字典存储每个参数的状态信息
        self.prev_direction=None
        # self.direction=None
        self.loss0=None
        self.Mbeta=max(Mbeta,1.0)
        self.Mmin=Mmin
        self.M=max(self.Mmin,M)
        self.Mmax=max(Mmax,self.M)
        self.alphamax=alphamax
        if(Mgamma is None):
            self.Mgamma=np.sqrt(1/self.Mbeta)
        else:
            self.Mgamma=min(Mgamma,1.0)

    def step(self, closure):
        if self.prev_direction is None:
            with torch.enable_grad():
                loss = closure()
            grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)
            with torch.no_grad():
                self.prev_direction=tuplescale(-1.0,grads)
                self.loss0=loss
            self.prev_grad=grads
        mprint("ck detection",tuplemdot(self.prev_direction,self.prev_grad)/tuplenorm(self.prev_grad)**2)
        jvp=tuplemdot(self.prev_grad,self.prev_direction)
        hvp=torch.autograd.grad(jvp,self.param_groups[0]['params'])
        with torch.no_grad():
            vhvp=tuplemdot(hvp,self.prev_direction)
            m=torch.sqrt(tuplemdot(self.prev_direction,self.prev_direction))
            alpha=_search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)
            mprint("alpha",alpha)
    # 确定步长
        
        for p,direction in zip(self.param_groups[0]['params'],self.prev_direction):
            p.data.add_(direction, alpha=alpha*self.param_groups[0]["lr"])  # 更新参数
        ## 计算新方向
        with torch.enable_grad():
                loss = closure()
        grads =torch.autograd.grad(loss,self.param_groups[0]['params'],create_graph=True)#计算新梯度
        ## 计算beta
        with torch.no_grad():
            sum0=torch.tensor(0.0)
            sum1=torch.tensor(0.0)
            for gradsa,da,gradsolda in zip(grads,self.prev_direction,self.prev_grad):
                sum0+=torch.sum(gradsa*gradsa)
                sum1+=torch.sum(da*(gradsa-gradsolda))
            beta=(sum0/sum1)
            mprint("beta",beta)
            c,flag= Armijo(loss,self.loss0,self.prev_grad,self.prev_direction,alpha)
            if(flag>0):
                mprint("Armijo c > ", c)
            elif(flag<0):
                mprint("Armijo c < ", c)
            else:
                mprint("Armijo " , -c, ",< c < ", c)
            sigma,flag2=    Wolfe(grads,self.prev_grad,self.prev_direction,alpha)
            if(flag2>0):
                mprint("Wolfe sigma > ", sigma)
            elif(flag2<0):
                mprint("Wolfe sigma < ", sigma)
            else:
                mprint("Wolfe " , -sigma, ",< sigma < ", sigma)
            self.prev_direction=tuplelinear(-1.0,grads,beta,self.prev_direction)
            # mprint("Vertical detection",tuplemdot(self.prev_direction,grads)/(tuplenorm(self.prev_direction)*tuplenorm(grads)))
            if(loss>self.loss0):
                self.M=min((1+self.M)*self.Mbeta,self.Mmax)
                mprint("Missing decrease, increase M to",self.M)
            else:
                self.M=max(self.M*self.Mgamma,self.Mmin)
            self.loss0=loss
        self.prev_grad=grads
        return loss,m,alpha,self.M
    


#  准则检验
## Armijo准则,Goldstein 准则都用这个检验
def Armijo(f1,f0,grad0,direction0,alpha):
    dgp=tuplemdot(direction0,grad0)
    ck=(f1-f0)/(alpha*dgp)
    if((alpha*dgp)<0):
        ck=(f1-f0)/(alpha*dgp)
        flag=-1 # 意义为c>ck
    elif((alpha*dgp)>0):
        ck=(f1-f0)/(alpha*dgp)
        flag=1# 意义为c>ck
    elif((f1-f0)>0):
        ck=-torch.inf
        flag=-1# 表示c不能取任意值（要比负无穷更小，这不可能）
    else:
        ck=torch.inf
        flag=0 #表示c可以取任意值
    return ck,flag

def Wolfe(grad1,grad0,direction0,alpha):
    dgp1=tuplemdot(direction0,grad1)
    dgp0=tuplemdot(direction0,grad0)
    dgp0=dgp0*np.sign(alpha)# 应当小于0
    dgp1=dgp1*np.sign(alpha)
    if(dgp0>0):
        sigma_k=dgp1/dgp0 # sigma<=sigma_k
        flag=-1
    elif(dgp0<0):
        sigma_k=dgp1/dgp0 # sigma>=sigma_k
        flag=1
    elif(dgp1>0):
        sigma_k=np.inf
        flag=0 #表示c可以取任意值
    else:
        sigma_k=-np.inf
        flag=-1 # 表示c不能取任意值（要比负无穷更小，这不可能）
    return sigma_k,flag

