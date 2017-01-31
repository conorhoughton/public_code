
def stretcher(snd,freq,new_length):

    old_length=double(snd.shape[0])/freq
    mu=new_length/old_length

    new_length_n=int(new_length*freq)

    new_snd=[]

    for t_n in range(0,new_length_n):
        
        new_t=double(t_n)/freq
        old_t=new_t/mu

        old_t_lower=int(old_t*freq)
        old_t_upper=old_t_lower+1

        lambda_lower=old_t-old_t_lower
        lambda_upper=1-lambda_lower

        s=lambda_upper*snd[old_t_lower]+lambda_lower*snd[old_t_upper]

        new_snd.append(s)
