import numpy as np


def cor_ustar(clauds):
    a             =  0.11213993918965293
    b             = -0.014060976414076887
        
    # Note: no calculation of the error. 
    clauds['uSc'] = clauds['uS'] + a * (clauds['g'] - clauds['r']) + b

def combine_u(clauds):
    # combine u and u star
    u_comb     = np.zeros(len(clauds))
    u_comb_err = np.zeros(len(clauds))

    u1         = clauds['u']
    u1_err     = clauds['u_err']
     
    # NOTE: not correcting the error for the S transform. 
    u2         = clauds['uSc']
    u2_err     = clauds['uS_err']
        
    nfails     = 0
        
    for i in range (len(u_comb)):
        if   (u1_err[i]<0.0 and u2_err[i]>0.0):
            u_comb[i]     = u2[i]
            u_comb_err[i] = u2_err[i]
                    
        elif (u1_err[i]>0.0 and u2_err[i]<0.0):
            u_comb[i]     = u1[i]
            u_comb_err[i] = u1_err[i]
                
        elif (u1_err[i]>0.0 and u2_err[i]>0.0):
            w_u           = u1_err[i]**(-2.0)/ (u1_err[i]**(-2.0) + u2_err[i]**(-2.0))
            w_u2          = u2_err[i]**(-2.0)/ (u1_err[i]**(-2.0) + u2_err[i]**(-2.0))
                
            u_comb[i]     = w_u*u1[i] +  w_u2* u2[i]
            u_comb_err[i] = (u1_err[i]**(-2.0) + u2_err[i]**(-2.0))**(-1./2.)

        elif (u1_err[i]<0.0 and u2_err[i]<0.0):
            u_comb[i]     = -99
            u_comb_err[i] = -99

        else:            
            u_comb[i]     = -99
            u_comb_err[i] = -99            
            
            nfails       +=   1 

    print('Number of failures: {}'.format(nfails))

    clauds['uW']     = u_comb
    clauds['uW_err'] = u_comb_err

def select_tomog(clauds, components=False):
    # Update clauds in place.
    cor_ustar(clauds)
    combine_u(clauds)
    
    # Quality cuts
    quality = (clauds['uW_err'] > 0.0) & (clauds['uW_err'] < 10.0) & (clauds['uW'] > 0.0) & (clauds['g'] > 0.0) & (clauds['r'] > 0.0) 
    quality = quality & (clauds['g_err'] > 0.0) & (clauds['r_err'] > 0.0)

    umg     = clauds['uW'] - clauds['g']
    gmr     = clauds['g']  - clauds['r']
    
    # ---  Color boxes  ---
    # Original
    color_box       = (umg>0.9) & (gmr<1.2) & (umg>1.5*gmr+0.75)

    # Liu
    # color_box     = (umg>0.88) & (gmr<1.2) & (umg>1.99*gmr+0.68)
    
    color_box_ext_1 = (umg>0.4) & (umg<1.0) & (umg>2.4*gmr+0.3) & (gmr<0.15) & ~color_box
    color_box_ext_2 = (umg>0.7) & (umg<1.5) & (umg>2.4*gmr+0.3) & ~color_box & ~color_box_ext_1
    
    # r mag.
    r_range         = (clauds['r']>22.5) & (clauds['r']<24.5) & quality & (gmr>-0.5)

    # final selection
    sel_LBG       = color_box & r_range & (clauds['r_err'] < 0.4)
    
    sel_LBG_ext_1 = color_box_ext_1 & r_range & (clauds['r_err'] < 0.4)
    sel_LBG_ext_2 = color_box_ext_2 & r_range & (clauds['r_err'] < 0.4)
    
    sel           = sel_LBG | sel_LBG_ext_1 | sel_LBG_ext_2
    
    if not components:
        return clauds[sel]
    
    else:
        return clauds[sel_LBG], clauds[sel_LBG_ext_1], clauds[sel_LBG_ext_2]
