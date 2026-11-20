import os

folder_path = r".\\dataset"
locs = []

for root, _, files in os.walk(folder_path):
    for f in files:
        if f.endswith(('.java', '.cpp', '.py')):
            with open(
                os.path.join(root, f), 'r', encoding='utf-8', errors='ignore'
            ) as file:
                lines = file.readlines()
                locs.append(len(lines))

if locs:
    print(f'Total files: {len(locs)}')
    print(f'Min LOC: {min(locs)}')
    print(f'Max LOC: {max(locs)}')
    print(f'Average LOC: {sum(locs)/len(locs):.1f}')