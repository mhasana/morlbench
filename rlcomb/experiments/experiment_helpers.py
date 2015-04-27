'''
Created on Apr 23, 2015

@author: Dominik Meyer <meyerd@mytum.de>
'''

import numpy as np
import logging as log


def interact_multiple(agent, problem, interactions):
    '''
    Interact multiple times with the problem and then
    return arrays of actions chosen and payouts received
    in each stage.
    '''
    payouts = []
    actions = []
    log.info('Playing %i interactions ... ' % (interactions))
    for t in xrange(interactions):
        action = agent.decide(t)
        payout = problem.play(action)
        agent.learn(t, action, payout)
        log.debug(' step %05i: action: %i, payout: %f' %
                  (t, action, payout))
        payouts.append(payout)
        actions.append(action)
    payouts = np.array(payouts)
    actions = np.array(actions)
    return actions, payouts


def interact_multiple_twoplayer(agent1, agent2, problem, interactions):
    '''
    Interact multiple times with the problem and then
    return arrays of actions chosen and payouts received
    in each stage.
    '''
    #TODO: Make this more flexible instead of tedious code duplication.
    payouts1 = []
    actions1 = []
    payouts2 = []
    actions2 = []
    log.info('Playing %i interactions ... ' % (interactions))
    for t in xrange(interactions):
        action1 = agent1.decide(t)
        action2 = agent2.decide(t)
        payout1, payout2 = problem.play(action1, action2)
        agent1.learn(t, action1, payout1)
        agent2.learn(t, action2, payout2)
        log.debug(' step %05i: action1: %i, payout1: %i, action2: %i, payout2: \
%i' % (t, action1, payout1, action2, payout2))
        payouts1.append(payout1)
        actions1.append(action1)
        payouts2.append(payout2)
        actions2.append(action2)
    payouts1 = np.array(payouts1)
    actions1 = np.array(actions1)
    payouts2 = np.array(payouts2)
    actions2 = np.array(actions2)
    return (actions1, payouts1), (actions2, payouts2)