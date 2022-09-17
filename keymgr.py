from pygame import key
from pygame import K_UP as up
from pygame import K_DOWN as down
from pygame import K_LEFT as left
from pygame import K_RIGHT as right
from pygame import K_w as w
from pygame import K_a as a
from pygame import K_d as d
from pygame import K_s as s

def calc_vect(keys,mod):
    output = (0,0,'',False)
    com_mod = mod[0]
    vol = mod[1]
    if keys[w] and keys[s] or keys[a] and keys[d] or keys[up] and keys[down] or keys[left] and keys[right]:
        output = (0,0,'',False)
        return output
    if keys[w] and not keys[s] and not keys[up] and not keys[down] or keys[up] and not keys[down] and not keys[w] and not keys[s]:
        output = (output[0],output[1]-vol,'back',True)
    if keys[s] and not keys[w] and not keys[up] and not keys[down] or keys[down] and not keys[up] and not keys[w] and not keys[s]:
        output = (output[0],output[1]+vol,'front',True)
    if keys[a] and not keys[d] and not keys[left] and not keys[right] or keys[left] and not keys[right] and not keys[a] and not keys[d]:
        output = (output[0]-vol,output[1],'left',True)
    if keys[d] and not keys[a] and not keys[left] and not keys[right] or keys[right] and not keys[left] and not keys[a] and not keys[d]:
        output = (output[0]+vol,output[1],'right',True)
    if keys[d] and keys[s] and not keys[a] and not keys[w] and not keys[left] and not keys[down] and not keys[right] and not keys[up] or keys[down] and keys[right] and not keys[up] and not keys[left] and not keys[w] and not keys[a] and not keys[s] and not keys[d] and not keys[left] and not keys[up]:
        output = (output[0]-com_mod,output[1]-com_mod,output[2],True)
    if keys[a] and keys[s] and not keys[d] and not keys[w] and not keys[left] and not keys[down] and not keys[right] and not keys[up] or keys[down] and keys[left] and not keys[up] and not keys[right] and not keys[w] and not keys[a] and not keys[s] and not keys[d] and not keys[right] and not keys[up]:
        output = (output[0]+com_mod,output[1]-com_mod,output[2],True)
    if keys[d] and keys[w] and not keys[a] and not keys[s] and not keys[left] and not keys[down] and not keys[right] and not keys[up] or keys[up] and keys[right] and not keys[down] and not keys[left] and not keys[w] and not keys[a] and not keys[s] and not keys[d] and not keys[left] and not keys[down]:
        output = (output[0]-com_mod,output[1]+com_mod,output[2],True)
    if keys[a] and keys[w] and not keys[d] and not keys[s] and not keys[left] and not keys[down] and not keys[right] and not keys[up] or keys[up] and keys[left] and not keys[down] and not keys[right] and not keys[w] and not keys[a] and not keys[s] and not keys[d] and not keys[right] and not keys[down]:
        output = (output[0]+com_mod,output[1]+com_mod,output[2],True)
    return output