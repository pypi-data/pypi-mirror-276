#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PyMieSim.experiment.setup import Setup

import numpy
from pydantic.dataclasses import dataclass
from dataclasses import field

from PyMieSim.physics import power_to_amplitude
from PyMieSim import polarization
from PyMieSim.binary.Sets import CppSourceSet
from DataVisual import units

from typing import List, Union, NoReturn


@dataclass
class BaseSource:
    """
    Base class for light sources in PyMieSim experiments.

    Attributes:
        wavelength (List): The wavelength(s) of the light source.
        polarization_value (List): The polarization values of the light source, in degrees.
        name (str): The name of the source set, defaults to 'PlaneWave'.
    """
    wavelength: Union[List[float], float]
    polarization_value: Union[List[float], float]
    name: str = field(default='PlaneWave', init=False)

    def __post_init__(self):
        self.mapping = {
            'wavelength': None,
            'polarization': None
        }

        self.format_inputs()
        # self.generate_polarization_attribute()
        self.generate_amplitude()
        self.generate_binding()

    def format_inputs(self):
        """Formats input wavelengths and polarization values into numpy arrays."""
        self.polarization_value = numpy.atleast_1d(self.polarization_value).astype(float)
        self.wavelength = numpy.atleast_1d(self.wavelength).astype(float)

    def get_datavisual_table(self) -> NoReturn:
        """
        Appends the scatterer's properties to a given table for visualization purposes. This enables the
        representation of scatterer properties in graphical formats.

        Parameters:
            table (list): The table to which the scatterer's properties will be appended.

        Returns:
            list: The updated table with the scatterer's properties included.
        """
        self.mapping['wavelength'] = units.Length(
            long_label='Wavelength',
            short_label=r'$\lambda$',
            base_values=self.wavelength,
            string_format='.2f'
        )

        self.mapping['polarization'] = units.Degree(
            long_label='Polarization',
            short_label=r'Pol',
            base_values=self.polarization_value,
            string_format='.2f'
        )

        return [v for k, v in self.mapping.items() if v is not None]

    def bind_to_experiment(self, experiment: Setup):
        """
        Binds the source set to an experiment.

        Parameters:
            experiment (Setup): The experiment setup to bind the source to.
        """
        experiment.binding.set_source(self.binding)


@dataclass
class Gaussian(BaseSource):
    """
    Represents a Gaussian light source with a specified numerical aperture and optical power.

    Inherits from BaseSource and adds specific attributes for Gaussian sources.

    Attributes:
        NA (List): The numerical aperture(s) of the Gaussian source.
        optical_power (float): The optical power of the source, in Watts.
        polarization_type (str): The type of polarization, defaults to 'linear'.
    """
    NA: Union[List[float], float]
    optical_power: float
    polarization_type: str = 'linear'

    def generate_binding(self) -> NoReturn:
        """
        Prepares the keyword arguments for the C++ binding based on the scatterer's properties. This
        involves evaluating material indices and organizing them into a dictionary for the C++ interface.

        Returns:
            None
        """
        linear_polarization = polarization.Linear(*self.polarization_value)

        self.binding_kwargs = dict(
            wavelength=numpy.atleast_1d(self.wavelength).astype(float),
            jones_vector=numpy.atleast_2d(linear_polarization.jones_vector).astype(complex).T,
            amplitude=numpy.atleast_1d(self.amplitude).astype(float),
        )

        self.binding = CppSourceSet(**self.binding_kwargs)

    def generate_amplitude(self):
        """Generates the amplitude of the Gaussian source based on its optical power and numerical aperture."""
        self.amplitude = power_to_amplitude(
            wavelength=self.wavelength,
            optical_power=self.optical_power,
            NA=self.NA
        )


@dataclass
class PlaneWave(BaseSource):
    """
    Represents a Plane Wave light source with a specified amplitude.

    Inherits from BaseSource and specifies amplitude directly.

    Attributes:
        amplitude (float): The amplitude of the plane wave, in Watts.
        polarization_type (str): The type of polarization, defaults to 'linear'.
    """
    amplitude: Union[List[float], float]
    polarization_type: str = 'linear'

    def generate_binding(self) -> NoReturn:
        """
        Prepares the keyword arguments for the C++ binding based on the scatterer's properties. This
        involves evaluating material indices and organizing them into a dictionary for the C++ interface.

        Returns:
            None
        """
        self.binding_kwargs = dict(
            wavelength=self.wavelength,
            jones_vector=self.jones_vector,
            amplitude=self.amplitude
        )

        self.binding = CppSourceSet(**self.binding_kwargs)

    def generate_amplitude(self):
        """Sets the amplitude of the plane wave as a numpy array."""
        self.amplitude = numpy.atleast_1d(self.amplitude)
