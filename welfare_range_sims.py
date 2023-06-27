## Simulate welfare range data
import os
import pickle
import random
import argparse
import csv

import numpy as np
import pandas as pd
import squigglepy as sq
from squigglepy.numbers import K, M, B
import scipy.stats as stats

parser = argparse.ArgumentParser(description='Generate welfare ranges')
parser.add_argument('--animal', type=str, help="What species do you want to simulate the welfare range of?")
parser.add_argument('--unknown_prob', type=float, help="What probability do you assign Unknown judgements for this species?", default=0)
parser.add_argument('--weight_no', type=str, help="Do you want to give non-zero probability to lean no and likely no?")
parser.add_argument('--hc_weight', type=float, help="What weight do high-confidence proxies get relative to other proxies?")
parser.add_argument('--scenarios', type=int, help='How many Monte Carlo simulations to run?', default=10000)
parser.add_argument('--csv', type=str, help='Define the relative path to the CSV with the species scores information')
parser.add_argument('--path', type=str, help='Define a custom path for the saved model outputs', default='')
parser.add_argument('--save', type=bool, help='Set to False to not save (overwrite) model outputs', default=True)
parser.add_argument('--update_every', type=int, help='How many steps to run before updating?', default=1000)
parser.add_argument('--verbose', type=bool, help='Set to True to get scenario-specific output', default=False)
args = parser.parse_args()

ANIMAL = args.animal
UNKNOWN_PROB = args.unknown_prob
WEIGHT_NO = args.weight_no
HC_WEIGHT = args.hc_weight
N_SCENARIOS = args.scenarios
VERBOSE = args.verbose
CSV = args.csv
SAVE = args.save
PATH = args.path
update_every = args.update_every

SCENARIO_RANGES = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]

judgments = pd.read_csv(os.path.join('inputs', 'Qualitative Data.csv'))

if WEIGHT_NO == "Yes":
    judgment_prob_map = {'Likely no': {'lower': 0, 'upper': 0.25},
                    'Lean no': {'lower': 0.25, 'upper': 0.50},
                    'Lean yes': {'lower': 0.50, 'upper': 0.75},
                    'Likely yes': {'lower': 0.75, 'upper': 1.00},
                    'Unknown': UNKNOWN_PROB}
else:
    judgment_prob_map = {'Likely no': {'lower': 0, 'upper': 0},
                    'Lean no': {'lower': 0, 'upper': 0},
                    'Lean yes': {'lower': 0.50, 'upper': 0.75},
                    'Likely yes': {'lower': 0.75, 'upper': 1.00},
                    'Unknown': UNKNOWN_PROB}

animal_scores = judgments[['Proxies', ANIMAL]]

simulated_probs = {}
simulated_scores = {}

proxies_list = animal_scores['Proxies'].to_list()

for proxy in proxies_list:
    simulated_probs[proxy] = []
    simulated_scores[proxy] = []

for s in range(N_SCENARIOS):
    if s % update_every == 0:
        if VERBOSE:
            print('-')
            print('### SCENARIO {} ###'.format(s + 1))
        else:
            print('... Completed {}/{}'.format(s + 1, N_SCENARIOS))

    for idx, row in animal_scores.iterrows():
        judgment = row[ANIMAL]
        proxy = row['Proxies']

        if judgment == 'Unknown':
            proxy_prob = judgment_prob_map[judgment]
        else:
            lower_prob = judgment_prob_map[judgment]['lower']
            upper_prob = judgment_prob_map[judgment]['upper']
            proxy_prob = random.uniform(lower_prob, upper_prob)
            
        has_proxy = stats.bernoulli.rvs(proxy_prob)

        simulated_probs[proxy].append(proxy_prob)
        simulated_scores[proxy].append(has_proxy)

if SAVE:
    print('... Saving 1/1')
    pickle.dump(simulated_scores, open('{}simulated_scores.p'.format(PATH), 'wb'))