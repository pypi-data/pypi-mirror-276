# Model for gold fluorescence
from lmfit import Model, models, create_params, Parameters
from matplotlib import pyplot as plt
import numpy as np
import scipy.constants as scc
import importlib.resources
from lmfit import Parameters
import xraydb as xdb
from pySWXF import fluor_fit, refl_funs
from pySWXF.fluor_fit import multilayer_ref_new_model, multilayer_model_Ti
from pySWXF import spec_utils, AuI_funs
import re
import pandas as pd
from scipy.interpolate import RectBivariateSpline
from typing import Dict, Any, List, Tuple
import sys

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


def get_offset_fit(th, I, dI, Beam_Energy, fitflag, showfit=True, verbose=True):
    """
    Fit the offset in the reflection data for different experimental setups.

    Parameters:
    -----------
    th : array-like
        The angular positions of the measurements.
    I : array-like
        The measured reflected intensity.
    dI : array-like
        The uncertainties in the measured intensities (not used in the function, but included for completeness).
    Beam_Energy : float
        The energy of the incident beam.
    fitflag : str
        The fitting configuration flag. Options are:
        - 'NN': New cell, New multilayer.
        - 'OO': Old cell, Old multilayer.
    showfit : bool, optional
        Whether to display the fit plot. Default is True.
    verbose : bool, optional
        Whether to print detailed information during execution. Default is True.

    Returns:
    --------
    thoff : float
        The angular offset resulting from the fit.
    result : lmfit.model.ModelResult
        The result of the fit, containing the best-fit parameters and statistics.
    """
    
    params = get_params(fitflag)
    
    if fitflag == 'NN':
        if verbose: 
            print(f'Using flag {fitflag}: New cell, New multilayer')
        th_refrac = water_refract(th, Beam_Energy)
        fitfun = multilayer_ref_new_model
    elif fitflag == 'OO':
        if verbose: 
            print(f'Using flag {fitflag}: Old cell, Old multilayer')
            print('Side entry sample cell: No refraction correction.')
        th_refrac = th
        fitfun = multilayer_model_Ti
    else:
        print(f'Not configured for flag {fitflag}')
        sys.exit()
    
    for key in params.keys():
        params[key].vary = False

    params['I0'].vary = True
    params['I0'].max = 1e9
    params['I0'].min = 100
    params['I0'].value = np.max(I) * 3.5
    params['thoff'].vary = True
    params['thoff'].min = -0.1
    params['thoff'].max = 0.1
    params['res'].value = 0.001

    if verbose: 
        print('Fitting amplitude and offset')

    presim = fitfun.eval(params=params, theta=th_refrac, Energy=Beam_Energy, water=True, bilayer=True, new_cell=False)
    cen_sim = np.sum(presim * th) / np.sum(presim)
    cen_dat = np.sum(I * th) / np.sum(I)
    params['thoff'].value = cen_dat - cen_sim

    result = fitfun.fit(I, theta=th_refrac, params=params, Energy=Beam_Energy, water=True, bilayer=True, new_cell=False, weights=I * 0 + 1)
    thoff = result.params['thoff'].value
    
    if showfit:    
        ysim = result.eval(theta=th_refrac, Energy=Beam_Energy, water=True, bilayer=True, new_cell=False)
        plt.plot(th, I, label='data')
        plt.plot(th, ysim, '-k', label='fit')
        plt.locator_params(axis='x', nbins=20)
        plt.grid()
        plt.xlabel('th (deg)')
        plt.ylabel('Reflected Intensity')
        plt.legend()
        if verbose:
            print(f'Angular offset = {thoff:.3f}')
    
    return thoff, result



def setup_fit(dinfo):
    """
    Set up the fitting function and initial parameters based on the fluorophore.

    Parameters:
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - fit_fun (Model): Combined lmfit model.
    - pars (Parameters): Initial parameters for the model.
    - data_range (array-like): Range of data to fit.
    - amplitude_names (list): List of amplitude parameter names.
    """
    if dinfo['fluorophore'] == 'Br':
        quad_mod = models.QuadraticModel()
        gaus_mod = models.GaussianModel()
        fit_fun = quad_mod + gaus_mod
        pars = Parameters()
        pars.add('amplitude', value=150000, min=0)
        pars.add('center', value=13400)
        pars.add('sigma', value=115, vary=False)
        pars.add('a', value=0)
        pars.add('b', value=0)
        pars.add('c', value=5000)
        data_range = (dinfo['E'] > 13359 - 756.3) & (dinfo['E'] < 13359 + 302.6)
        amplitude_names = ["amplitude"]
    elif dinfo['fluorophore'] == 'gold':
        g1 = models.GaussianModel(prefix='g1_')
        g2 = models.GaussianModel(prefix='g2_')
        q1 = models.QuadraticModel()
        fit_fun = g1 + g2 + q1
        pars = Parameters()
        pars.add('g1_center', value=13400, vary=False)
        pars.add('g2_center', value=13771, vary=False)
        pars.add('g1_sigma', value=114.8, vary=False)
        pars.add('g2_sigma', value=114.8, vary=False)
        pars.add('g1_amplitude', value=2e5)
        pars.add('g2_amplitude', value=4e4)
        pars.add('a', value=0)
        pars.add('b', value=-7.5)
        pars.add('c', value=5000)
        data_range = (dinfo['E'] > 13000) & (dinfo['E'] < 14100)
        amplitude_names = ["g1_amplitude", "g2_amplitude"]
    return fit_fun, pars, data_range, amplitude_names

def get_fluor_amplitude(mca_data, dinfo, start_pars=None):
    """
    Get the fluorescence amplitude from the data.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.
    - start_pars (Parameters, optional): Starting parameters for the fit.

    Returns:
    - peak_counts (float): Sum of peak counts.
    - peak_errs (float): Sum of peak errors.
    """
    fit_fun, pars, data_range, amplitude_names = setup_fit(dinfo)
    if start_pars is not None:
        pars = start_pars
        for amplitude_name in amplitude_names:
            pars[amplitude_name].max = pars[amplitude_name].value * 4
            pars[amplitude_name].min = 0
    dE = dinfo['E'][1] - dinfo['E'][0]
    X = dinfo['E'][data_range]
    this_result = fit_fun.fit(mca_data[data_range] / dE, x=X, params=pars)
    peak_counts = sum(this_result.params[amplitude_name].value for amplitude_name in amplitude_names)
    peak_errs = np.sqrt(sum(
        (this_result.params[amplitude_name].stderr if isinstance(this_result.params[amplitude_name].stderr, float) else np.inf)**2
        for amplitude_name in amplitude_names
    ))
    return peak_counts, peak_errs

def get_start_pars(mca_data, dinfo):
    """
    Get the starting parameters for the fit.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - pars (Parameters): Fitted parameters.
    - this_result (ModelResult): Result of the initial fit.
    - amplitude_names (list): List of amplitude parameter names.
    """
    fit_fun, pars, data_range, amplitude_names = setup_fit(dinfo)
    dE = dinfo['E'][1] - dinfo['E'][0]
    X = dinfo['E'][data_range]
    mca_sum = np.sum(mca_data, 0)
    npt = mca_data.shape[0]
    this_result = fit_fun.fit(mca_sum[data_range] / dE, x=X, params=pars)
    pars = this_result.params
    for amplitude_name in amplitude_names:
        pars[amplitude_name].value /= npt
    return pars, this_result, amplitude_names

def show_fluor_fit(result, dinfo):
    """
    Show the fit result for fluorescence data.

    Parameters:
    - result (ModelResult): Result of the fit.
    - dinfo (dict): Dictionary containing experimental information.
    """
    result.fit()
    fit_fun, pars, data_range, amplitude_names = setup_fit(dinfo)
    result.plot_fit()
    E = result.userkws['x']
    ysim0 = result.eval()
    par0 = result.params
    for amplitude_name in amplitude_names:
        par0[amplitude_name].value = 0
    ysim1 = result.eval(params=par0)
    plt.plot(E, ysim0 - ysim1, '--g', label='Fluorescence Intensity')
    plt.legend()
    plt.ylabel('Counts/Second')
    plt.xlabel('Energy (eV)')
    plt.title(f'Fit to Fluorescence Peak {dinfo["fluorophore"]}')
    plt.show()

def get_fluorescence_data(mca_data, dinfo, norm=None, plot_fit=False):
    """
    Get fluorescence data and fit results.

    Parameters:
    - mca_data (array-like): MCA data to fit.
    - dinfo (dict): Dictionary containing experimental information.
    - norm (array-like, optional): Normalization factor.
    - plot_fit (bool, optional): Whether to plot the fit.

    Returns:
    - mca_amplitudes (array-like): MCA amplitudes.
    - mca_errors (array-like): MCA errors.
    """
    nscanpoints = mca_data.shape[0]
    mca_amplitudes = np.empty(nscanpoints)
    mca_errors = np.empty(nscanpoints)
    start_pars, start_result, amplitude_names = get_start_pars(mca_data, dinfo)
    if plot_fit:
        show_fluor_fit(start_result, dinfo)
    for ii in range(nscanpoints):
        A, dA = get_fluor_amplitude(mca_data[ii, :], dinfo, start_pars=start_pars)
        mca_amplitudes[ii] = A
        mca_errors[ii] = dA
    if norm is not None:
        norm_factor = norm / np.average(norm)
        mca_amplitudes *= norm_factor
        mca_errors *= norm_factor
    return mca_amplitudes, mca_errors

def plot_fluorescence(angles, mca_amplitudes, mca_errors, dinfo, fluorescence_scan_number, nflist=None):
    """
    Plot fluorescence data.

    Parameters:
    - angles (array-like): Angles of the measurement.
    - mca_amplitudes (array-like): MCA amplitudes.
    - mca_errors (array-like): MCA errors.
    - dinfo (dict): Dictionary containing experimental information.
    - fluorescence_scan_number (int): The scan number for fluorescence.
    - nflist (str, optional): List of scan numbers.
    """
    plt.errorbar(angles, mca_amplitudes, mca_errors, fmt='-ks')
    plt.xlabel('theta (deg)')
    plt.ylabel('fluorescence intensity (cps)')
    scanstring = nflist if nflist is not None else f'{fluorescence_scan_number}'
    plt.title(f"file: {dinfo['vortex_filename_stub']} scan: {scanstring}, {dinfo['fluorophore']}")
    plt.ylim(0.7 * np.min(mca_amplitudes), 1.3 * np.max(mca_amplitudes))
    plt.show()

def fluor_multifit(N_align, N_fluor, dinfo):
    """
    Perform multi-fit for fluorescence data.

    Parameters:
    - N_align (list): List of alignment scan numbers.
    - N_fluor (list): List of fluorescence scan numbers.
    - dinfo (dict): Dictionary containing experimental information.

    Returns:
    - angles_0 (array-like): Final angles.
    - mca_amplitudes_0 (array-like): Final MCA amplitudes.
    - mca_errors_0 (array-like): Final MCA errors.
    - nflist (str): List of fluorescence scan numbers.
    - thoff (float): offset angle from first fit.
    """
    nflist = ", ".join(map(str, N_fluor))
    last_align_scan_number = 0
    for i, (align_scan_number, fluorescence_scan_number) in enumerate(zip(N_align, N_fluor)):
        print(f'Working on dataset {i+1} align scan {align_scan_number} fluor scan {fluorescence_scan_number}')
        
        if align_scan_number != last_align_scan_number:
            print('Fitting alignment scan for angle offset')
            # Get reflectivity data
            data, _ = spec_utils.readscan(dinfo["align_filename"], align_scan_number)
            th = np.array(data['MU'])
            I = np.array(data['L_ROI1'])
            dI = np.sqrt(I)
            rr = (th > 0.4) & (th < 0.6)
            theta_offset, _ = AuI_funs.get_offset_fit(th[rr], I[rr], dI[rr], dinfo["Energy_Nov"], dinfo["fitflag"], showfit=False, verbose=True)
        else:
            print('Repeated alignment scan. No fit required')
        
        last_align_scan_number = align_scan_number

        mca_data, mca_sum, ndset, angles, npt, exposure_time, norm = spec_utils.get_fluor_data(
            dinfo["spec_filename"], dinfo["mca_filename"], fluorescence_scan_number)
        
        mca_amplitudes, mca_errors = get_fluorescence_data(mca_data / exposure_time, dinfo, norm=None, plot_fit=False)
        
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

        nnorm = norm / np.mean(norm)
    return angles_0, mca_amplitudes_0 / nnorm, mca_errors_0 / nnorm, nflist, thoff



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


def pars_to_layer(pars: Dict[str, Any], dinfo: Dict[str, Any]) -> Any:
    """
    Convert parameter values to layer information based on fit flag.

    Parameters:
    -----------
    pars : Dict[str, Any]
        Dictionary containing parameter values.
    dinfo : Dict[str, Any]
        Dictionary containing fitting information including the fit flag.

    Returns:
    --------
    layers : Any
        Layer information generated by the sample simulation function.
    """
    if dinfo['fitflag'] == 'NN':
        expected_params = {'d_overlay', 'sig_overlay', 'G', 'D', 'sig_W', 'sig_SiC', 'D_Cr', 'sig_Cr', 'sig_Si_Bot'}
        sample_fun = fluor_fit.sample_sim_new
        water_flag = True 
        bilayer_flag = True 
        new_cell_flag = False
    elif dinfo['fitflag'] == 'OO':
        expected_params = {'G', 'D', 'sig_Mo', 'sig_Si', 'overlay', 'sig_Si_top', 'D_Ti', 'sig_Ti', 'D_SiO2', 'sig_SiO2',
                           'D_SiO2_Bot', 'sig_SiO2_Bot', 'sig_Si_Bot'}
        sample_fun = fluor_fit.sample_sim
        water_flag = True 
        bilayer_flag = True 
        new_cell_flag = None
    else:
        raise ValueError(f"Unknown fitflag: {dinfo['fitflag']}")

    filtered_par = {key: value.value for key, value in pars.items() if key in expected_params}

    layers = sample_fun(**filtered_par, water=water_flag, bilayer=bilayer_flag, new_cell=new_cell_flag)
    return layers

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

def get_bilayer_position(layers: List[Tuple[str, float, float, float]]) -> Tuple[float, float]:
    """
    Calculate the position and thickness of the bilayer in the given list of layers.

    Parameters:
    -----------
    layers : List[Tuple[str, float, float, float]]
        A list of tuples, each containing (material, density, thickness, roughness).

    Returns:
    --------
    bilayer_top : float
        The depth at which the top of the bilayer is found.
    bilayer_thickness : float
        The total thickness of the bilayer.
    """
    depth = 0.0
    found_top = False
    bilayer_thickness = 0.0
    bilayer_top = 0.0

    for material, density, thickness, roughness in layers:
        if not found_top and material == 'CH2':
            bilayer_top = depth
            found_top = True

        depth -= thickness

        if material == 'CH2':
            bilayer_thickness += thickness

    return bilayer_top, bilayer_thickness

def get_standing_wave(
    dinfo: Dict[str, Any], 
    layers: Any, 
    bilayer_top: float, 
    bilayer_thickness: float, 
    result_reflectivity: Any, 
    thoff: float, 
    th_com: float, 
    plot_wave: bool = True
) -> RectBivariateSpline:
    """
    Calculate the standing wave field and optionally plot it.

    Parameters:
    -----------
    dinfo : Dict[str, Any]
        Dictionary containing fitting information and parameters.
    layers : Any
        Layer structure used in the reflection matrix calculation.
    bilayer_top : float
        The top position of the bilayer.
    bilayer_thickness : float
        The thickness of the bilayer.
    result_reflectivity : Any
        Result object containing fitted parameters.
    thoff : float
        The offset angle obtained from the reflectivity fit
    th_com : float
        The reflection center angle.
    plot_wave : bool, optional
        Whether to plot the standing wave field. Default is True.

    Returns:
    --------
    SW : RectBivariateSpline
        Bivariate spline object representing the standing wave field.
    """
    try:
        alpha = np.linspace(0.1, 1, 1000) * scc.degree

        if dinfo['fitflag'] == 'NN':
            alphap = AuI_funs.water_refract(alpha / scc.degree, dinfo['Energy_Nov']) * scc.degree
        else:
            alphap = alpha

        t, r, kz, X, rr, tp, zm = refl_funs.reflection_matrix(alphap, dinfo['Energy_Nov'], layers)
        heights0 = np.linspace(-1000, 500, 1000) * scc.angstrom

        If, Ef = refl_funs.standing_wave(heights0, t, r, kz, zm)
        offset = (bilayer_top - bilayer_thickness) * scc.angstrom
        SW = RectBivariateSpline(heights0 - offset, alpha+thoff*scc.degree, If)

        alpha_sim = np.linspace(0.1, 0.8, 1000) * scc.degree
        heights_sim = np.linspace(-500, 500, 1000) * scc.angstrom
        Isim = SW(heights_sim, alpha_sim)

        if plot_wave:
            plt.imshow(
                Isim, aspect='auto', extent=(alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree,
                                             heights_sim[0]/scc.angstrom, heights_sim[-1]/scc.angstrom),
                origin='lower'
            )
            plt.xlabel('MU (deg)')
            plt.ylabel('z (angstrom)')
            plt.title('Standing Wave Intensity')
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [0, 0], '--r', label='Bilayer bottom')
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [bilayer_thickness, bilayer_thickness], '-r', label='Bilayer top')

            d_overlay = result_reflectivity.params.get('d_overlay', result_reflectivity.params.get('overlay')).value
            plt.plot([alpha_sim[0]/scc.degree, alpha_sim[-1]/scc.degree], [-d_overlay, -d_overlay], '-y', label='Multilayer top')

            plt.plot([th_com, th_com], [heights_sim[0]/scc.angstrom, heights_sim[-1]/scc.angstrom], '-m', label='Reflection center')

            plt.legend()

        return SW
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Model for three slabs

def three_slab(theta,A0,A1,A2,Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2],Imap,zmax)

three_slab_model = Model(three_slab, independent_vars = ['theta', 'Imap', 'zmax'])

# Model for five slabs
def five_slab(theta,A0,A1,A2,A3, A4, Imap,zmax):
    return multilayer_fluor_lay_N(theta,[A0,A1,A2,A3, A4],Imap,zmax)

five_slab_model = Model(five_slab, independent_vars = ['theta', 'Imap', 'zmax'])


