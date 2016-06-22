

class Channel:

    def __init__(self,inf,tau,v_initial):

        self.inf=inf
        self.tau=tau

        self.initial=self.inf(v_initial)


    def derivative(self,v,l):
        
        return (self.inf(v)-l)/self.tau(v)
