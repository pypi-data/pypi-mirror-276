import torch
from torch.optim import Optimizer
# , _get_value,_stack_if_compiling, _dispatch_sqrt, _default_to_fused_or_foreach,_get_scalar_dtype, _capturable_doc, _differentiable_doc, _foreach_doc,_fused_doc, _maximize_doc, _view_as_real
import numpy as np
from typing import Tuple
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


def search_alpha(jvp,vhvp,m,M):
        a=M*m
        alpha=cubicreg1d(jvp,vhvp,a)
        return alpha
def tuplemdot(m1, m2):
    sum0=torch.tensor(0.0,device=m1[0].device)
    for m1a,m2b in zip(m1,m2):
        sum0+=torch.sum(m1a*m2b)
    return sum0
def tuplenorm(m ):
    return torch.sqrt(tuplemdot(m,m))
def tuplescale(a,m):
    return tuple([a*ma for ma in m])
def tuplelinear(a,m,b,m2):
    return tuple([a*ma+b*mb for ma,mb in zip(m,m2)])

#实现adam算法
class CustomAdamcubic(torch.optim.Optimizer):
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8):
        defaults = dict(lr=lr, betas=betas, eps=eps)
        super(CustomAdamcubic, self).__init__(params, defaults)
        self.M=1
        self.alphamax=1
        self.alphaprev=0.5
        self.alphamin=1.3e-6
    # @_use_grad_for_differentiable
    def step(self, closure):
        with torch.enable_grad():
            loss=closure()
        update=[]
        for group in self.param_groups:
            grads =torch.autograd.grad(loss,group['params'],allow_unused=True,materialize_grads=True)
            for p,grad in zip(group['params'],grads):
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
                state['v'] = beta2 * v + (1 - beta2) * torch.sum(grad * grad)

                m_hat = state['m'] / (1 - beta1 ** state['step'])
                v_hat = state['v'] / (1 - beta2 ** state['step'])

                update.append(-group['lr'] * m_hat / (torch.sqrt(v_hat) + group['eps']))
            direction=tuple(update)
            jvp=tuplemdot(grads,direction)
    ## 使用两步法确定步长
        for p,d in zip(group['params'],direction):
            p.data.add_(d, alpha=self.alphamin)  # 更新参数
        with torch.enable_grad():
                loss = closure()
        grads2 =torch.autograd.grad(loss,group['params'],allow_unused=True,materialize_grads=True )
        jvp2=tuplemdot(grads2,direction) # jvp2=jvp1+alphamin*vhvp
        vhvp=(jvp2-jvp)/self.alphamin

        with torch.no_grad():
            m=torch.sqrt(tuplemdot(direction,direction))
            alpha=search_alpha(jvp.item(),vhvp.item(),m.item()**(3),self.M)
            alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin
            if(vhvp<0):
                alpha=min(max(alpha,-10*self.alphaprev),10*self.alphaprev)-self.alphamin
            else:
                alpha=min(max(alpha,-self.alphamax),self.alphamax)-self.alphamin
            # mprint("alpha",alpha)
    # 确定步长
        
        for p,d in zip(group['params'],direction):
            p.data.add_(d, alpha=alpha*group["lr"])  # 更新参数

        return loss

