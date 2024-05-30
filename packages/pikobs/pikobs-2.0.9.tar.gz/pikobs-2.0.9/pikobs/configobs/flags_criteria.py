def flag_criteria(flags):
    """
    This function generates a filtering criteria expression based on flag selection.

    Arguments:
    flags (str): The selected flag option ('all', 'rejets', 'assim', 'qc', 'bias_corr', or 'obsselectionflags').

    Returns:

    str: A filtering criteria expression.
    """
    
    BIT17_QCVAR=131072
    BIT12_VUE=4096 
    BIT18_ORO=262144
    BIT9_REJ=512
    BIT16_REJOMP=65536
    BIT19_SURFACE=524288
    BIT11_SELCOR=2048  
    BIT7_REJ=128  
    BIT8_BLIST=256

    if flags == "all":
        FLAG = " flag >= 0 "
    elif "assimilee":
        FLAG=f" and (flag & {BIT12_VUE})= {BIT12_VUE} "
    elif "bgckalt":
        FLAG=f" and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR}=0 and (flag & {BIT8_BLIST})=0 "
    elif "bgckalt_qc":
        FLAG=f" and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR})=0 "
    elif "monitoring":
        FLAG=f" and (flag & {BIT9_REJ})= 0 and (flag & {BIT7_REJ})= 0 "
    elif "postalt":
        FLAG=f" and (flag & {BIT17_QCVAR})=0 and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR})=0 and (flag & {BIT8_BLIST})=0 "
    else:
        raise ValueError(f'Invalid flag option: {flags}')

    return FLAG
