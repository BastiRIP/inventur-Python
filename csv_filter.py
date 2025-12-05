import re

def filter_csv_blocks(csv_text):
    lines = csv_text.splitlines()
    results = []
    i = 0
    while i < len(lines) - 1:
        current_line = lines[i]
        next_line = lines[i + 1]
        if '0400' in current_line and '0001' in next_line:
            k_nummer_match = re.search(r'0400\s+([KZM]\d+\.\d+|\d{8})', current_line)
            k_nummer = k_nummer_match.group(1) if k_nummer_match else ''
            artikel_match = re.search(r'0001\s+(.+)', next_line)
            artikel = artikel_match.group(1).strip() if artikel_match else ''
            results.append({'kNummer': k_nummer, 'artikel': artikel})
            i += 2
        else:
            i += 1
    return results
