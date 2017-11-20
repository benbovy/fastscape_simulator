"""
A simple simulator of landscape evolution.
"""
import argparse

import numpy as np

import xsimlab
from xtopo.models.fastscape_base import fastscape_base_model


def run_fastscape(k_sp, k_diff, u_rate,
                  x_size=601, y_size=401, spacing=200.,
                  time_step=1e5, time_total=1e7):
    """
    Run "Fastscape" landscape evolution model.

    This version of Fastscape includes the following processes:

    - uniform, block uplift at a constant rate through time ;
    - bedrock channel erosion using the stream power law ;
    - hillslope erosion using linear diffusion.

    The total simulation time is 10 Myr.

    The simulation start with a random, nearly flat topography.
    Topographic elevation remains fixed at the domain boundary.

    Parameters
    ----------
    k_sp : float
        Stream power law coefficient. The drainage area and slope
        exponents of the stream power law are fixed to 0.4 and 1,
        respectively.
    k_diff : float
        Hillslope diffusivity (units: m**2/yr).
    u_rate : float
        Uplift rate (units: m/yr).

    Other parameters
    ----------------
    x_size : int, optional
        Grid size in x (i.e., number of columns).
    y_size : int, optional
        Grid size in y (i.e., number of rows).
    spacing : float, optional
        Uniform grid spacing in x and y (units: m).
    time_step : float, optional
        Simulation time step (units: yr).
    time_total : float, optional
        Total simulation duration (units: yr).

    Returns
    -------
    elevation : numpy.ndarray
        Topographic elevation at the end of the simulation (units: m).
        Array shape is (`y_size`, `x_size`).

    """
    in_ds = xsimlab.create_setup(
        model=fastscape_base_model,
        clocks={'time': {'end': time_total, 'step': time_step}},
        input_vars={
            'grid': {'x_size': x_size, 'y_size': y_size,
                     'x_spacing': spacing, 'y_spacing': spacing},
            'flow_routing': {'pit_method': 'mst_linear'},
            'block_uplift': {'u_coef': u_rate},
            'spower': {'k_coef': k_sp, 'm_exp': 0.4, 'n_exp': 1},
            'diffusion': {'k_coef': k_diff},
            'topography': {'elevation': (('y', 'x'), np.random.rand(y_size, x_size))}
        },
        snapshot_vars={
            None: {'grid': ('x', 'y'), 'topography': 'elevation'},
        }
    )

    out_ds = (in_ds.xsimlab.run(model=fastscape_base_model)
                           .set_index(y='grid__y', x='grid__x'))

    return out_ds.topography__elevation.values


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Run "Fastscape" landscape evolution model.')

    parser.add_argument(
        'k_sp', type=float, help='stream power law coefficient')
    parser.add_argument(
        'k_diff', type=float, help='hillslope diffusivity (m**2/yr)')
    parser.add_argument(
        'u_rate', type=float, help='uplift rate (m/yr)')
    parser.add_argument(
        '--x_size', type=int, default=601,
        help='grid size in x (i.e., number of columns). default: 601')
    parser.add_argument(
        '--y_size', type=int, default=401,
        help='grid size in y (i.e., number of rows). default: 401')
    parser.add_argument(
        '--spacing', type=float, default=200.,
        help='uniform grid spacing in x and y (m). default: 200')
    parser.add_argument(
        '--time_step', type=float, default=1e5,
        help='simulation time step (yr). default: 1e5')
    parser.add_argument(
        '--time_total', type=float, default=1e7,
        help='total simulation duration (yr). default: 1e7')
    parser.add_argument(
        '--output', default='out.npy',
        help='output filename. default: out.npy')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    out_topo = run_fastscape(args.k_sp, args.k_diff, args.u_rate,
                             args.x_size, args.y_size, args.spacing,
                             args.time_step, args.time_total)

    np.save(args.output, out_topo)
