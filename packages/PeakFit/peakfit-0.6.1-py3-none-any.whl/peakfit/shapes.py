import lmfit as lf
import nmrglue.analysis.lineshapes1d as ls
import numpy as np


def pvoigt2d(x, y, x0, y0, x_fwhm, y_fwhm, x_eta, y_eta):
    shapex = ls.sim_pvoigt_fwhm(x, x0, x_fwhm, x_eta)
    shapey = ls.sim_pvoigt_fwhm(y, y0, y_fwhm, y_eta)
    return shapex * shapey


def create_params(peaks, spectra, clargs):
    ucx = spectra.ucx
    ucy = spectra.ucy

    nz, ny, nx = spectra.data.shape

    hz2pt_x = abs(ucx.f(1, "hz") - ucx.f(0, "hz"))
    hz2pt_y = abs(ucy.f(1, "hz") - ucy.f(0, "hz"))

    hz2ppm_x = abs(ucx.ppm(ucx.f(1, "hz")))
    hz2ppm_y = abs(ucy.ppm(ucy.f(1, "hz")))

    vary_position = not clargs.fixed

    params = lf.Parameters(usersyms={"ucx": ucx, "ucy": ucy})

    for index, (x0_ppm, y0_ppm) in enumerate(peaks[["x0_ppm", "y0_ppm"]].values):
        pre = f"p{index}_"

        x0, x0min, x0max = x0_ppm + np.array([0.0, -10.0, 10.0]) * hz2ppm_x
        y0, y0min, y0max = y0_ppm + np.array([0.0, -10.0, 10.0]) * hz2ppm_y

        params.add(f"{pre}x0", value=x0, min=x0min, max=x0max, vary=vary_position)
        params.add(f"{pre}y0", value=y0, min=y0min, max=y0max, vary=vary_position)

        params.add(f"{pre}x0_pt", expr=f"ucx.f({pre}x0, 'ppm') % {nx}")
        params.add(f"{pre}y0_pt", expr=f"ucy.f({pre}y0, 'ppm') % {ny}")

        params.add(f"{pre}x_fwhm", value=15.0, min=0.1, max=200.0)
        params.add(f"{pre}y_fwhm", value=15.0, min=0.1, max=200.0)

        params.add(f"{pre}x_fwhm_pt", expr=f"{pre}x_fwhm * {hz2pt_x}")
        params.add(f"{pre}y_fwhm_pt", expr=f"{pre}y_fwhm * {hz2pt_y}")

        # By default, the shape is gaussian (eta = 0.0)
        if clargs.pvoigt:
            vary_eta = True
            value_eta = 0.5
        elif clargs.lorentzian:
            vary_eta = False
            value_eta = 1.0
        else:
            vary_eta = False
            value_eta = 0.0

        params.add(f"{pre}x_eta", value=value_eta, min=-1.0, max=+1.0, vary=vary_eta)
        params.add(f"{pre}y_eta", value=value_eta, min=-1.0, max=+1.0, vary=vary_eta)

    return params
