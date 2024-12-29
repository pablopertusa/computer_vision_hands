from pathlib import Path
import numpy as np
import json

partition = {'training': [], 'validation' : []}
labels = {}

data = Path('/home/pablo/Desktop/tercero/mdp/trabajo/HANDS/')
names = [str(name) for name in data.iterdir()]
np.random.shuffle(names)

split = 0.2
training_split = int(len(names)*(1-split))

def obtener_label(s: str) -> str:
    img = s.split('/')[-1].split('.')[0]
    label = img[-2:]
    return label

for name in names[:training_split]:
    label = obtener_label(name)
    partition['training'].append(name)
    labels[name] = label

for name in names[training_split:]:
    label = obtener_label(name)
    partition['validation'].append(name)
    labels[name] = label

with open('partition.json', 'w') as partition_file:
    json.dump(partition, partition_file)

with open('labels.json', 'w') as labels_file:
    json.dump(labels, labels_file)

