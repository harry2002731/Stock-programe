import re
import config

collection = config.Stock_list.keys()

def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)  # Converts 'djm' to 'd.*?j.*?m'
    regex = re.compile(pattern)  # Compiles a regex.
    for item in collection:
        match = regex.search(item)  # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    if suggestions == []:
        False
    else:
        return [x for _, _, x in sorted(suggestions)]

# print(fuzzyfinder("000002.SZ", collection))
