import json

def calculate_and_insert_human_averages(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metrics = [
        'readability_score',
        'understandability_score',
        'maintainability_score'
    ]

    for key, entry in data.items():
        if not isinstance(entry, dict) or 'metadata' not in entry:
            continue
        
        human_keys = [h for h in ['Human1', 'Human2', 'Human3'] if h in entry]
        if not human_keys:
            continue
        
        averages = {}
        for metric in metrics:
            scores = [entry[h][metric] for h in human_keys if metric in entry[h]]
            if scores:
                averages[metric] = round(sum(scores) / len(scores))
            else:
                averages[metric] = 0

        old_metadata = entry['metadata']
        new_metadata = {}
        
        inserted = False
        for m_key, m_val in old_metadata.items():
            if m_key in metrics:
                continue
            
            new_metadata[m_key] = m_val
            
            if m_key == 'external_reference_url':
                for metric in metrics:
                    new_metadata[metric] = averages[metric]
                inserted = True

        if not inserted:
            for metric in metrics:
                new_metadata[metric] = averages[metric]

        entry['metadata'] = new_metadata

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"File successfully processed and saved to {output_file}")

if __name__ == '__main__':
    calculate_and_insert_human_averages('Results.json', 'Results_2.json')