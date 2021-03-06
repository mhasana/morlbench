#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jun 07, 2016

@author: Dominik Meyer <meyerd@mytum.de>
@author: Johannes Feldmaier <johannes.feldmaier@tum.de>
@author: Simon Woelzmueller   <ga35voz@mytum.de>

    Copyright (C) 2016  Dominik Meyer, Johannes Feldmaier, Simon Woelzmueller

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from morlbench.morl_problems import MORLResourceGatheringProblem, MountainCarTime, MORLGridworld, MORLBuridansAss1DProblem, \
        Deepsea, MOPuddleworldProblem
from morlbench.morl_agents import MORLScalarizingAgent, MORLHVBAgent
from morlbench.experiment_helpers import morl_interact_multiple_episodic
from morlbench.morl_policies import PolicyFromAgent
from morlbench.plot_heatmap import policy_heat_plot
from morlbench.plotting_stuff import plot_hypervolume

import numpy as np
import random
import matplotlib.pyplot as plt
import logging as log

if __name__ == '__main__':

    epsilon_experiment = False
    gamma_experiment = False
    alpha_experiment = False
    tau_experiment = True
    ref_point_experiment = True
    # create Problem
    problem = MORLGridworld()
    # create an initialize randomly a weight vector
    scalarization_weights = [1.0, 0.0, 0.0]
    # tau is for chebyshev agent
    tau = 4.0
    # ref point is used for Hypervolume calculation
    ref = [-1.0, ]*problem.reward_dimension
    # learning rate
    alfacheb = 0.11
    eps = 0.9
    # Propability of epsilon greedy selection
    epsilons = np.arange(0, 1, 0.1)
    gammas = np.arange(0, 1, 0.1)
    alphas = np.arange(0, 1, 0.1)
    taus = np.arange(0.0, 10.0, 1.0)
    ref_points = [[-1.0, -1.0, -25.0], [-1.0, -25.0, -1.0], [-25.0, -1.0, -1.0]]
    # agents:
    agents = []
    interactions = 600
    if epsilon_experiment:
        log.info('Started epsilon experiment')
        for eps in xrange(len(epsilons)):
            agents.append(MORLScalarizingAgent(problem, epsilon=epsilons[eps], alpha=alfacheb,
                                               scalarization_weights=scalarization_weights,
                                               ref_point=ref, tau=tau, function='chebishev'))
            morl_interact_multiple_episodic(agents[eps], problem, interactions)

        plot_hypervolume(agents, problem, name='epsilon')

    if gamma_experiment:
        log.info('Started gamma experiment')
        for gam in xrange(len(gammas)):
            agents.append(MORLScalarizingAgent(problem, epsilon=0.1, alpha=alfacheb,
                                               scalarization_weights=scalarization_weights,
                                               ref_point=ref, tau=tau, function='chebishev', gamma=gammas[gam]))
            morl_interact_multiple_episodic(agents[gam], problem, interactions)

        plot_hypervolume(agents, problem, name='gamma')

    if alpha_experiment:
        log.info('Started alpha experiment')
        for alf in xrange(len(alphas)):
            agents.append(MORLScalarizingAgent(problem, epsilon=0.1, alpha=alphas[alf],
                                               scalarization_weights=scalarization_weights,
                                               ref_point=ref, tau=tau, function='chebishev'))
            morl_interact_multiple_episodic(agents[alf], problem, interactions)

        plot_hypervolume(agents, problem, name='alpha')

    if tau_experiment:
        log.info('Started tau experiment')
        for tau in xrange(len(taus)):
            agents.append(MORLScalarizingAgent(problem, epsilon=0.1, alpha=alfacheb,
                                               scalarization_weights=scalarization_weights,
                                               ref_point=ref, tau=taus[tau], function='chebishev'))
            morl_interact_multiple_episodic(agents[tau], problem, interactions)

        plot_hypervolume(agents, problem, name='tau')

    if ref_point_experiment:
        log.info('Started reference point experiment')
        for ref_p in xrange(len(ref_points)):
            agents.append(MORLHVBAgent(problem, alfacheb, eps, ref_points[ref_p], scalarization_weights))
            morl_interact_multiple_episodic(agents[ref_p], problem, interactions)
        plot_hypervolume(agents, problem, name='reference point')

