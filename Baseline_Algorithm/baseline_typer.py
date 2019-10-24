import os
import re


def evaluate_context(phrase, var_name, variables):
    other_var_match = r'^[a-z, A-Z, \-, \_]+'
    type_matches = {
        '$number$': r'^\(*[0-9]+\)*;?',
        '$string$': r'''^(["'])((?:\\\1|(?:(?!\1)).)*)(\1);?''', # works with single or double quotes
        '$bool$': r'^(true)|(false);?',
        '$list$': r'^\['
    }
    pred = 'O'
    for var_type, regex in type_matches.items():
        if re.search(other_var_match, phrase) and not re.search(type_matches['$bool$'], phrase):
            if phrase in variables:
                pred = variables[phrase]
            else:
                if not variables.get(var_name):
                    pred = '$any$'
        elif re.search(regex, phrase):
            pred = var_type
            break
        elif not variables.get(var_name):
            pred = '$any$'
    return pred


def typer(tokens):
    # Read in tokens
    variables = {}
    types = []
    for i in range(len(tokens)):
        if tokens[i] != '=' or i <= 0 or i >= len(tokens)-1:
            if variables.get(tokens[i]):
                types.append(variables[tokens[i]])
            else:
                types.append('O')
            continue
        var_name, phrase = tokens[i-1], tokens[i+1]

        type_pred = evaluate_context(phrase, var_name, variables)
        if type_pred == "$list$" and i+2 < len(tokens):
            type_pred = evaluate_context(tokens[i+2], var_name, variables)[:-1] + "[]$"
        variables[var_name] = type_pred
        types[-1] = variables[var_name]
        types.append('O')
    return types


if __name__ == "__main__":
    dir = os.getcwd()

    with open("500tech__angular-tree-component.json") as f:
        tokens_and_types = [line.split('\t') for line in f.readlines()]
        data = [{"tokens": tokens.split(' '), "types": types.split(' ')} for tokens, types in tokens_and_types]

    accuracies = []
    for i, file in enumerate(data):
        tokens = file['tokens']
        types  = file['types']
        types_pred = typer(tokens)
        correct = [pred for target, pred in zip(types, types_pred) if target == pred and target != 'O']
        accuracies.append(len(correct) / len([t for t in types if t != "O"]))
        print(f'{len(correct)}/{len([t for t in types if t != "O"])} types correctly annotated, excluding non-types')
    print(f"Average accuracy: {sum(accuracies)/len(accuracies)}")
