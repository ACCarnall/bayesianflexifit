import numpy as np

import os
import h5py

from .fit import fit


class posterior(object):
    """ Provides access to the outputs from fitting models to data and
    calculating posterior predictions for derived parameters (e.g. for
    star-formation histories, rest-frane magnitudes etc).

    Parameters
    ----------
    run : string - optional
        The subfolder into which outputs will be saved, useful e.g. for
        fitting more than one model configuration to the same data.

    n_samples : float - optional
        The number of posterior samples to generate for each quantity.
    """

    def __init__(self, ID, run=".", n_samples=500):

        self.ID = ID
        self.run = run
        self.n_samples = n_samples

        fname = "bff/" + self.run + "/" + self.ID + ".h5"

        # Check to see whether the object has been fitted.
        if not os.path.exists(fname):
            raise IOError("Fit results not found for " + self.ID + ".")

        # Reconstruct the fitted model.
        with h5py.File(fname, "r") as file:
            fit_info_str = file.attrs["fit_instructions"]
            # Evaluate with numpy names (array, float64, ...) available
            self.fit_instructions = eval(fit_info_str,
                                         {**vars(np), "np": np})

            # 2D array of samples for the fitted parameters only.
            self.samples2d = np.array(file["samples2d"])

        # Recover the fitted parameter names (in the same order as the
        # columns of samples2d) using the same logic as the fit class.
        fit._process_fit_instructions(self)

        # If fewer than n_samples exist in posterior, reduce n_samples
        if self.samples2d.shape[0] < self.n_samples:
            self.n_samples = self.samples2d.shape[0]

        # Randomly choose points to generate posterior quantities
        self.indices = np.random.choice(self.samples2d.shape[0],
                                        size=self.n_samples, replace=False)

        self.samples = {}  # Store all posterior samples

        # Add 1D posteriors for fitted params to the samples dictionary
        for i in range(self.ndim):
            param_name = self.params[i]

            self.samples[param_name] = self.samples2d[self.indices, i]
