.. _sec-data-molecular_absorption:

Atmosphere: Molecular absorption
================================

Molecular absorption datasets tabulate the volume absorption coefficient of a
gas mixture against the spectral coordinates, the volume fraction of the mixture
components, air pressure and air temperature.
Eradiate's built-in molecular absorption datasets are managed by the data store
(see :ref:`sec-data-intro` for details).

Specifications
--------------

Monochromatic
~~~~~~~~~~~~~

Monochromatic absorption coefficient datasets include one data variable:

* volume absorption coefficient (``sigma_a``),

and at least four :term:`dimension coordinates <dimension coordinate>`:

* radiation wavelength or radiation wavenumber (``w``),
* gas mixture mole fractions (``x_M`` where ``M`` is the molecule formula,
  e.g. ``x_H2O``),
* air pressure (``p``),
* and air temperature (``t``).

CKD
~~~

CKD absorption coefficient datasets include at least two data variables:

* ``sigma_a [x_M, p, t, w, g]`` : volume absorption coefficient
* ``wbounds [wbv, w]`` : band spectral bounds

one optional data variable:

* ``error [w, ng]`` : relative error on atmosphere band-averaged transmittance,

at least five :term:`dimension coordinates <dimension coordinate>`:

* ``w`` : radiation wavelength or radiation wavenumber of the band center
* ``wbv`` : band wavelength bounds
* ``g`` : quadrature :math:`g`-point / absorption coefficient cumulative probability
* ``x_M`` (where ``M`` is the molecule formula, e.g. ``x_H2O``, ``x_CO2``): gas
  mixture mole fractions (1 to :math:`N_M` coordinates where :math:`N_M` is the
  number of molecules in the mixture),
* ``p`` : air pressure,
* ``t`` : and air temperature,

and, if the data variable ``error`` is present:

* ``ng`` : number of quadrature :math:`g`-point.

.. warning::
   Although we try to handle out-of range interpolation errors as gracefully as
   possible, it is strongly recommend to ensure that thermophysical parameter
   values can be used as arguments to interpolate in the molecular absorption
   database when assembling molecular absorption data and / or thermophysical
   parameters.

Available datasets
------------------

Monochromatic datasets
~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Available monochromatic datasets
   :widths: 25 25 25 25
   :header-rows: 1

   * - Codename
     - Spectral range
     - Sampling resolution
     - Online data store path
   * - ``gecko``
     - [250, 3125] nm
     - 0.01 :math:`\rm{cm}^{-1}` in [250, 300] :math:`\cup` [600, 3125] nm,
       0.1 :math:`\rm{cm}^{-1}` in [300, 600] nm
     - ``spectra/absorption/mono/gecko/``
   * - ``komodo``
     - [250, 3125] nm
     - 1 :math:`\rm{cm}^{-1}`
     - ``spectra/absorption/mono/komodo/``

CKD datasets
~~~~~~~~~~~~

.. list-table:: Available CKD datasets
   :widths: 25 25 25 25
   :header-rows: 1

   * - Codename
     - Spectral range
     - Band widths
     - Online data store path
   * - ``monotropa``
     - [250, 3125] nm
     - 100 :math:`\rm{cm}^{-1}`
     - ``spectra/absorption/ckd/monotropa/``
   * - ``panellus``
     - [250, 3125] nm
     - 1 nm
     - ``spectra/absorption/ckd/panellus/``
   * - ``mycena``
     - [250, 3120] nm
     - 10 nm
     - ``spectra/absorption/ckd/mycena/``
