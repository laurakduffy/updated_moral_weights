import os
import csv
import platform
import pandas as pd
import warnings
import user_inputs
import pickle

warnings.filterwarnings('ignore')

ANIMALS = ['Pigs', 'Chickens', 'Carp', 'Octopuses', 'Shrimp', 'BSF']

default_weight_unknowns = {animal : 0 for animal in ANIMALS}

print("### CHOOSE UNKNOWNS ###")
weight_unknowns = user_inputs.assign_unknowns(ANIMALS, default_weight_unknowns)
weight_nos = user_inputs.choose_nonzero_nos()

PARAMS = {'N_SCENARIOS': 10000, 'UPDATE_EVERY': 100, "WEIGHT_NOS": weight_nos}

def run_cmd(cmd):
    print(cmd)
    os.system(cmd)

def simulate_scores(animal, params):
    print("### SIMULATING SCORES FOR {} ###".format(animal.upper()))
    params['animal'] = animal
    params['path'] = "{}_sims".format(animal)
    params['unknown_prob'] = weight_unknowns[animal]

    run_cmd('python3 welfare_range_sims.py --animal {animal} --unknown_prob {unknown_prob} \
            --weight_no {WEIGHT_NOS} --scenarios {N_SCENARIOS} --csv simulations/{path}.csv \
            --path "simulations/{path}" --update_every {UPDATE_EVERY}'.format(**params)
            )
    
print('...Pull data from Sheets')
if platform.system() == 'Darwin' or platform.system() == 'Linux':
    run_cmd('rm -rf inputs')
    run_cmd('mkdir inputs')
    run_cmd('rm -rf simulations')
    run_cmd('mkdir simulations')
    run_cmd('python3 download_sheets.py')
elif platform.system() == 'Windows':
    run_cmd('rmdir /Q /S inputs')
    run_cmd('mkdir inputs')
    run_cmd('rmdir /Q /S simulations')
    run_cmd('mkdir simulations')
    run_cmd('python download_sheets.py')
else:
    raise ValueError('Platform `{}` not supported'.format(platform.system()))

pickle.dump(weight_unknowns, open(os.path.join('inputs', 'Unknown Probabilities.p'), 'wb'))
pickle.dump(PARAMS, open(os.path.join('inputs', 'Parameters.p'), 'wb'))

for animal in ANIMALS:
    simulate_scores(animal, PARAMS)

print('...Completed simulations')

