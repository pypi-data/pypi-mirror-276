# Model for gold fluorescence
from lmfit import Model, models
from matplotlib import pyplot as plt
import numpy as np
import scipy.constants as scc
import importlib.resources
from lmfit import Parameters
import xraydb as xdb
from pySWXF.fluor_fit import multilayer_ref_new_model, multilayer_model_Ti
from pySWXF import spec_utils, AuI_funs

g1 = models.GaussianModel(prefix='g1')
g2 = models.GaussianModel(prefix='g2')
q1 = models.QuadraticModel() 
peak_model = g1+g2+q1

# code to fit reflectivity and find offset

MULTILAYER_FIT_NEW = 'NM_clean_NIU_NOKW_Mar26_24_fit4.json'
MULTILAYER_FIT_OLD = 'niu_multilayer_fit_params_3_LBL.json'

def water_refract(th,Beam_Energy):
        alphac_water = np.sqrt(2*xdb.xray_delta_beta('H2O',1.00,Beam_Energy)[0])
        thc_water = alphac_water/scc.degree
        return np.sqrt(th**2  - thc_water**2)

def get_params(fitflag):
    if fitflag == 'NN':
        parfilename = MULTILAYER_FIT_NEW
    else:
        parfilename = MULTILAYER_FIT_OLD
    with importlib.resources.open_text('pySWXF', parfilename) as f:
        params = Parameters()
        params.load(f)
    return(params)

def get_offset_fit_D(th,I,dI,Beam_Energy, fitflag, showfit = True, verbose=True):
    if verbose:
        print('varying D instead of angle offset')
    params = get_params(fitflag)
    if fitflag == 'NN':
        if verbose: 
            print(f'Using flag {fitflag:s} New cell, New multilayer')
        th_refrac = water_refract(th,Beam_Energy)
        fitfun = multilayer_ref_new_model
    elif fitflag == 'OO':
        if verbose: 
            print(f'Using flag {fitflag:s} Old cell, Old multilayer')
            fitfun = multilayer_model_Ti
        if verbose: 
            print(f'Side entry sample cell: No refraction correction.')
        th_refrac = th
    else: 
        print(f'not configured for flag {fitflag:s}')
        exit
    for key, value in params.items():
        value.vary = False

    params['I0'].vary = True
    params['I0'].max = 1e9
    params['I0'].min = 100
    params['I0'].value = np.max(I)*3.5
    params['thoff'].vary = False
    params['res'].value = .001
    params['D'].vary = True
    D0 = params['D'].value

    if verbose: 
        print('fitting amplitude and offset')
        presim = fitfun.eval(params = params, theta = th_refrac, 
            Energy = Beam_Energy, water = True, bilayer = True, new_cell = False)
    cen_sim = np.sum(presim*th)/np.sum(presim)
    cen_dat = np.sum(I*th)/np.sum(I)
    params['thoff'].value = cen_dat-cen_sim

    result = fitfun.fit(
        I,theta = th_refrac, params = params, Energy = Beam_Energy,
        water = True, bilayer = True, new_cell = False, weights = I*0+1)
    
    D = result.params['D'].value
    
    if showfit:    
        ysim=result.eval(theta = th_refrac, 
            Energy = Beam_Energy, water = True, bilayer = True, new_cell = False)
        plt.plot(th,I,label='data')
        plt.plot(th,ysim,'-k',label='fit')
        plt.locator_params(axis='x', nbins=20)
        plt.grid()
        plt.xlabel('th (deg)')
        plt.ylabel('Reflected Intensity')
        plt.legend()
        print(f'D-spacing {D:7.3f} vs. D0 {D0:7.3f}')
    return(D, result)

def get_offset_fit(th,I,dI,Beam_Energy, fitflag, showfit = True, verbose=True):
    params = get_params(fitflag)
    if fitflag == 'NN':
        if verbose: 
            print(f'Using flag {fitflag:s} New cell, New multilayer')
        th_refrac = water_refract(th,Beam_Energy)
        fitfun = multilayer_ref_new_model
    elif fitflag == 'OO':
        if verbose: 
            print(f'Using flag {fitflag:s} Old cell, Old multilayer')
            fitfun = multilayer_model_Ti
        if verbose: 
            print(f'Side entry sample cell: No refraction correction.')
        th_refrac = th
    else: 
        print(f'not configured for flag {fitflag:s}')
        exit

    for key in params.keys():
        params[key].vary = False

    params['I0'].vary = True
    params['I0'].max = 1e9
    params['I0'].min = 100
    params['I0'].value = np.max(I)*3.5
    params['thoff'].vary = True
    params['thoff'].min =-.1
    params['thoff'].max = .1
    params['res'].value = .001

    if verbose: 
        print('fitting amplitude and offset')

    presim = fitfun.eval(params = params, theta = th_refrac, 
            Energy = Beam_Energy, water = True, bilayer = True, new_cell = False)
    cen_sim = np.sum(presim*th)/np.sum(presim)
    cen_dat = np.sum(I*th)/np.sum(I)
    params['thoff'].value = cen_dat-cen_sim

    result = fitfun.fit(
        I,theta = th_refrac, params = params, Energy = Beam_Energy,
        water = True, bilayer = True, new_cell = False, weights = I*0+1)
    
    thoff = result.params['thoff'].value
    
    if showfit:    
        ysim=result.eval(theta = th_refrac, 
            Energy = Beam_Energy, water = True, bilayer = True, new_cell = False)
        plt.plot(th,I,label='data')
        plt.plot(th,ysim,'-k',label='fit')
        plt.locator_params(axis='x', nbins=20)
        plt.grid()
        plt.xlabel('th (deg)')
        plt.ylabel('Reflected Intensity')
        plt.legend()
        print(f'angular offset = {thoff:7.3f}')
    return(thoff, result)

def get_gold_startparams(E,mca):   
    shp = np.shape(mca) 
    nscanpoints = shp[0]
    mca_sum = np.sum(mca,0)
    pars = peak_model.make_params()
    pars['g1center'].value = 13400
    pars['g1center'].vary = 0
    pars['g2center'].value = 13771
    pars['g2center'].vary = 0
    pars['g1sigma'].value = 114.8
    pars['g1sigma'].vary = 0
    pars['g2sigma'].value = 114.9
    pars['g2sigma'].vary = 0
    pars['g1amplitude'].value = np.sqrt(2*np.pi)*114.8*mca_sum[E>13400][0]/2
    pars['g2amplitude'].value =  pars['g1amplitude'].value/5
    pars['a'].value = 0
    pars['b'].value = -7.5
    pars['c'].value = 50000
    Erange = (E>13000)*(E<14100)
    result = peak_model.fit(mca_sum[Erange],params=pars,x=E[Erange])
    fitpars = result.params
    fitpars['a'].value /= nscanpoints 
    fitpars['b'].value /= nscanpoints 
    fitpars['c'].value  /= nscanpoints 
    fitpars['g1amplitude'].value /= nscanpoints 
    return(fitpars)

def get_gold_amplitude_pars(E,mca_data,pars):   
    Erange = (E>13000)*(E<14100)
    result = peak_model.fit(mca_data[Erange],params=pars,x=E[Erange])
    fitpars = result.params
    MCA_SLOPE = E[1]-E[0]
    peak_counts = (fitpars['g1amplitude'].value+fitpars['g2amplitude'].value)/MCA_SLOPE
    if fitpars['g1amplitude'].stderr is None:
        fitpars['g1amplitude'].stderr = 0
    if fitpars['g2amplitude'].stderr is None:
        fitpars['g2amplitude'].stderr = 0 
    peak_errs = np.sqrt((fitpars['g1amplitude'].stderr**2+fitpars['g2amplitude'].stderr**2))/MCA_SLOPE
    return(peak_counts,peak_errs)

quad_mod = models.QuadraticModel()
gaus_mod = models.GaussianModel()
Br_peak_model = quad_mod + gaus_mod

# Initialize parameters for the fit
def get_Br_amplitude(E,mca_data):
    pars = Br_peak_model.make_params()
    pars['amplitude'].value = 150000
    pars['amplitude'].min = 0
    pars['center'].value = 13400
    pars['sigma'].value = 50
    pars['a'].value = 0
    pars['b'].value = 0
    pars['c'].value = 5000
    dE = E[2]-E[1]
    x_center = 13359
    dx1f = 756.3
    dx2f = 302.6
    data_range = (E>x_center-dx1f)*(E<x_center+dx2f)
    X = E[data_range]
    this_result = Br_peak_model.fit(mca_data[data_range]/dE, x = X, params=pars)
    peak_counts = this_result.params['amplitude'].value
    if isinstance(this_result.params['amplitude'].stderr, float):
        peak_errs = this_result.params['amplitude'].stderr
    else:
        peak_errs = 0
    return peak_counts, peak_errs

def get_gold_amplitude(E,mca_data):   
    pars = peak_model.make_params()
    pars['g1center'].value = 13400
    pars['g1center'].vary = 0
    pars['g2center'].value = 13771
    pars['g2center'].vary = 0
    pars['g1sigma'].value = 114.8
    pars['g1sigma'].vary = 0
    pars['g2sigma'].value = 114.9
    pars['g2sigma'].vary = 0
    pars['g1amplitude'].value = np.sqrt(2*np.pi)*114.8*mca_data[E>13400][0]/2
    pars['g2amplitude'].value =  pars['g1amplitude'].value/5
    pars['a'].value = 0
    pars['b'].value = -7.5
    pars['c'].value = 50000
    Erange = (E>13000)*(E<14100)
    result = peak_model.fit(mca_data[Erange],params=pars,x=E[Erange])
    fitpars = result.params
    MCA_SLOPE = E[1]-E[0]
    peak_counts = (fitpars['g1amplitude'].value+fitpars['g2amplitude'].value)/MCA_SLOPE
    if fitpars['g1amplitude'].stderr is None:
        fitpars['g1amplitude'].stderr = 0
    if fitpars['g2amplitude'].stderr is None:
        fitpars['g2amplitude'].stderr = 0 
    peak_errs = np.sqrt((fitpars['g1amplitude'].stderr**2+fitpars['g2amplitude'].stderr**2))/MCA_SLOPE
    return(peak_counts,peak_errs)

def get_Zlist(N,D):
    # D = bilayer thickness
    # N slabs in bilayer
    edgelist = np.linspace(0,D,N+1)        # positions of interfaces of slabs
    Zlist = (edgelist[0:-1]+edgelist[1:])/2   # positions of centers of slabs
    return Zlist, edgelist

def multilayer_fluor_lay_N(theta,Avec,Imap,zmax):
    ''' multilayer_fluor_lay_N(theta,I0,thoff,bg,Avec)
    breaks up bilayer into N slabs wit N the dimension of Avec
    The A's are the amplitudes of the slabs
    '''
    # need to add feature to convolute with angular resolution
    alpha = theta*scc.degree
    Zlist, edgelist = get_Zlist(np.size(Avec), zmax)
    Ifield = Imap(Zlist, alpha)
    # sum up the product of the fluoresence from each slab times the amplitude in the slab
    y = np.sum(Ifield*np.expand_dims(Avec,1),0)
    return(y)

def plot_N_slab_result(result,NUM_SLABS, zmax):
    """
    Plot the fluorophore concentration across three slabs up to a maximum height.

    Parameters:
    result : object containing simulation parameters and results
    zmax : float, the maximum height to consider for plotting
    """
    # Constants
    ANGSTROM = scc.angstrom  # This assumes scc has been properly imported

    # Unpacking parameters
    A = [result.params[f'A{i}'].value for i in range(NUM_SLABS)]
    dA = [result.params[f'A{i}'].stderr for i in range(NUM_SLABS)]
    _, edgelist = get_Zlist(NUM_SLABS, zmax)

    # Check that edgelist is sufficiently long
    if len(edgelist) < NUM_SLABS + 1:
        raise ValueError("edgelist does not contain enough entries.")

    # Plotting
    for i, (tA,tdA) in enumerate(zip(A,dA)):
        edge1 = edgelist[i] / ANGSTROM
        edge2 = edgelist[i + 1] / ANGSTROM
        CEN = (edge1+edge2)/2
        plt.plot([edge1, edge1], [0, tA], '-k')
        plt.plot([edge1, edge2], [tA, tA], '-k')
        plt.plot([edge2, edge2], [tA, 0], '-k')
        if tdA  is not None:
            plt.errorbar([CEN],[tA],[tdA],fmt='ks')

    # now plot error bars

    plt.xlabel('height ($\\mathrm{\\AA}$)')
    plt.ylabel('fluorophore concentration')
    plt.title('Fluorophore Concentration Profile')

# Model for three slabs

def three_slab(theta,A0,A1,A2,Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2],Imap,zmax)

three_slab_model = Model(three_slab, independent_vars = ['theta', 'Imap', 'zmax'])

# Model for five slabs
def five_slab(theta,A0,A1,A2,A3, A4, Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2,A3, A4],Imap,zmax)

five_slab_model = Model(five_slab, independent_vars = ['theta', 'Imap', 'zmax'])


def fluor_multifit(N_align, N_fluor, dinfo):
    """
    Perform multifit for fluorescence data.

    Parameters:
    - N_align: List of alignment scan numbers.
    - N_fluor: List of fluorescence scan numbers.
    - dinfo: Dictionary containing relevant data information.

    Returns:
    - angles: Array of angles.
    - mca_amplitudes: Array of MCA amplitudes.
    - mca_errors: Array of MCA errors.
    - nflist: Comma-separated string of N_fluor values.
    """
    nflist = ", ".join(map(str, N_fluor))
    
    # Loop through all the data, offset and sum
    for i, (align_scan_number, fluorescence_scan_number) in enumerate(zip(N_align, N_fluor)):
        print(f'Working on dataset {i+1} align scan {align_scan_number} fluor scan {fluorescence_scan_number}')
        
        # Get reflectivity data
        data, _ = spec_utils.readscan(dinfo["align_filename"], align_scan_number)
        th = np.array(data['MU'])
        I = np.array(data['L_ROI1'])
        dI = np.sqrt(I)
        
        rr = (th>.4)*(th<.6)
        theta_offset, _ = AuI_funs.get_offset_fit(th[rr], I[rr], dI[rr], dinfo["Energy_Nov"], dinfo["fitflag"], showfit=False, verbose=True)
        
        # Get fluorescence data
        mca, _, _, angles, _, _, norm = spec_utils.get_fluor_data(dinfo["spec_filename"], dinfo["mca_filename"], fluorescence_scan_number)
        
        nscanpoints = mca.shape[0]
        mca_amplitudes = np.empty(nscanpoints)
        mca_errors = np.empty(nscanpoints)
        
        for ii in range(nscanpoints):
            if dinfo['fluorophore'] == 'Au':
                A, dA = AuI_funs.get_gold_amplitude(dinfo["E"], mca[ii, :])
            elif dinfo['fluorophore'] == 'Br':
                A, dA = AuI_funs.get_Br_amplitude(dinfo["E"], mca[ii, :])
            mca_amplitudes[ii] = A
            mca_errors[ii] = dA
        
        norm_factor = norm / np.average(norm)
        mca_amplitudes *= norm_factor
        mca_errors *= norm_factor
        
        if i == 0:
            thoff = theta_offset
            mca_amplitudes_0 = mca_amplitudes
            mca_errors_0 = mca_errors
            angles_0 = angles
        else:
            adjusted_angles = angles + theta_offset - thoff
            interpolated_amplitudes = np.interp(angles, adjusted_angles, mca_amplitudes)
            interpolated_errors = np.interp(angles, adjusted_angles, mca_errors)
            mca_amplitudes_0, mca_errors_0 = spec_utils.cbwe_s(mca_amplitudes_0, mca_errors_0, interpolated_amplitudes, interpolated_errors)
    
    return angles_0, mca_amplitudes_0, mca_errors_0, nflist
