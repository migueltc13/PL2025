#!/usr/bin/env python3

import sys
import os
import re
import json

DELIMITER = ';'
OUTPUT_FILE = 'out/results.json'

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

results = {
    'compositores': set(),  # Lista de compositores ordenada
    'distr': {},            # Distribuição de obras por período
    'obras': {}             # Obras por período ordenadas
}

with open(input_file, 'r', encoding='utf-8') as f:
    data = f.read()

# Regex to match full rows:
# Any line followed by 0 or more lines indented with 8 spaces
pattern = r'^(.*)(?:\n {8}(.*?))*$'

rows = re.findall(pattern, data, re.MULTILINE)

# Ignore the first row (header)
rows = rows[1:]

for i, row in enumerate(rows):
    full_row = "".join(row)  # Join the captured groups

    pattern = rf'({DELIMITER}")|("{DELIMITER})|({DELIMITER})'
    tokens = re.split(pattern, full_row)

    # Remove null or empty strings from the split result
    tokens = [t for t in tokens if t is not None and t != '']

    # Build the fields list by parsing the tokens
    fields = []
    field = ""
    on = True

    for token in tokens:
        if token == f'{DELIMITER}"':    # OFF
            fields.append(field)
            field = ""
            on = False
        elif token == f'"{DELIMITER}':  # ON
            fields.append(field)
            field = ""
            on = True
        elif token == f'{DELIMITER}':   # If delimiter appears, finalize current field
            if on:
                fields.append(field)
                field = ""
            else:
                field += token
        else:
            field += token  # Accumulate inside quoted field

    # Append the last field if it exists
    if field != "":
        fields.append(field)

    # Ensure enough fields exist
    if len(fields) < 7:
        print(f"Row number {i + 1} has less than 7 fields")
        continue

    nome       = fields[0]
    periodo    = fields[3]
    compositor = fields[4]

    results['compositores'].add(compositor)
    results['distr'][periodo] = results['distr'].get(periodo, 0) + 1
    results['obras'][periodo] = results['obras'].get(periodo, []) + [nome]

# Sort compositores
results['compositores'] = sorted(results['compositores'])

# Sort obras
for periodo in results['obras']:
    results['obras'][periodo] = sorted(results['obras'][periodo])

# Output file

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# Output to stdout
print("Compositores:")
print(json.dumps(results['compositores'], indent=2, ensure_ascii=False))

print("\nDistribuição por período:")
print(json.dumps(results['distr'], indent=2, ensure_ascii=False))

print("\nObras por período:")
print(json.dumps(results['obras'], indent=2, ensure_ascii=False))

print(f"Processed {len(rows)} rows")
