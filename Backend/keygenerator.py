import random
from key_database import keyset
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
nums=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
kleen=[alpha,nums]
def generate_short_key(length)-> str:
    res=""
    while(len(res)<length):
        res+=(random.choice(kleen[random.randint(0,1)]))
        if len(res)==length:
            if res in keyset:
                res=""
            else:
                keyset.add(res)
    return res
