#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:08:12 2024

@author: lorenzo piu
"""

from src.aPrioriDNS.DNS import Field3D

my_field = Field3D('data/Lifted_H2_subdomain')

# my_field.compute_reaction_rates()
filtered_field = Field3D(my_field.filter_favre(filter_size=12))
filtered_field.compute_reaction_rates()
filtered_field.compute_strain_rate(save_tensor=False)
filtered_field.compute_residual_kinetic_energy()
filtered_field.compute_residual_dissipation_rate()
filtered_field.compute_chemical_timescale()
filtered_field.compute_mixing_timescale()
filtered_field.compute_reaction_rates_batch()

