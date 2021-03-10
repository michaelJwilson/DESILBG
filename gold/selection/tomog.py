import numpy as np


def tomog(clauds):
    # Quality cuts
    quality = (clauds['u_err'] > 0.0) & (clauds['u_err'] < 10.0) & (clauds['u'] > 0.0) & (clauds['g'] > 0.0) & (clauds['r'] > 0.0) 
    quality = quality & (clauds['g_err'] > 0.0) & (clauds['r_err'] > 0.0)

    umg     = clauds['u'] - clauds['g']
    gmr     = clauds['g'] - clauds['r']
    
    # ---  Color boxes  ---
    color_box       = (umg>0.9) & (gmr<1.2) & (umg>1.5*gmr+0.75)
    
    color_box_ext_1 = (umg>0.4) & (umg<1.0) & (umg>2.4*gmr+0.3) & (gmr<0.15) & ~color_box
    color_box_ext_2 = (umg>0.7) & (umg<1.5) & (umg>2.4*gmr+0.3) & ~color_box & ~color_box_ext_1
    
    # r mag.
    r_range       = (clauds['r']>22.5) & (clauds['r']<24.5) & quality & (gmr>-0.5)

    # final selection
    sel_LBG       = color_box & r_range & (clauds['r_err'] < 0.4)
    
    sel_LBG_ext_1 = color_box_ext_1 & r_range & (clauds['r_err'] < 0.4)
    sel_LBG_ext_2 = color_box_ext_2 & r_range & (clauds['r_err'] < 0.4)
    
    sel           = sel_LBG | sel_LBG_ext_1 | sel_LBG_ext_2
    
    return sel
    
