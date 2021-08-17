import json


def load_reaction_data(fp):
    """ Loads pre-defined reaction information

    Assumes reaction data is in a json file, with the products and substrates
    separated.

    Args:
        fp (string): filepath to pre-defined reaction json

    Returns:
        dict, dict: dictionaries containing products and substrates data.
    """
    with open(fp) as json_file:
        data = json.load(json_file)

    return data["products"], data["substrates"]

def load_seeds(fp):
    """ Read in seed sets

    Assumes seed sets are in a txt file with one seed set per line

    Args:
        fp (string): filepath to seed text file

    Returns:
        2D list: list of all seed sets (each their own individual lists)
    """
    with open(fp) as f:
        seed_list = []
        for line in f:
            seed_list.append(line.split())

    return seed_list

def turn_on_reactions(cum_cpds, cum_rxns, products, substrates):
    new_rxns = []

    #Add new compounds from product -> substrate
    for rxn in products.keys():
        cpds = products[rxn]
        if set(cpds).issubset(cum_cpds):
            new_rxns.append(rxn)

    #Add new compounds from substrate -> product
    for rxn in substrates.keys():
        cpds = substrates[rxn]
        if set(cpds).issubset(cum_cpds):
            new_rxns.append(rxn)

    return list(set(new_rxns) - set(cum_rxns))

def add_cpds(rxns, cum_cpds, substrates, products):
    new_cpds = []
    for rxn in rxns:
        new_cpds.extend(products[rxn])
        new_cpds.extend(substrates[rxn])

    #Return new compounds, excluding those already in the cumulative set
    return list(set(new_cpds) - set(cum_cpds))

def run_network_expansion(seeds, products, substrates):
    cum_rxns = []
    cum_cpds = seeds
    flag = 1
    count = 0
    while flag:
        #Step 1: add newly found cps associated with reactions to cumulative cpds
        new_cpds = add_cpds(cum_rxns, cum_cpds, products, substrates)

        # TODO: add new cpds to dataframe
        cum_cpds.extend(new_cpds)
        #TODO: add cumulative cpds to dataframe

        #Step 2: turn on new reactions
        new_rxns = turn_on_reactions(cum_cpds, cum_rxns, products, substrates)
        # TODO: add new rxns to dataframe

         #Stop expansion if no new reactions are added
        if len(new_rxns) == 0:
            flag = 0

        #Step 3: add reactions to cumulative rxns
        cum_rxns.extend(new_rxns)
        # TODO: add cumulative reactions to dataframe

        count += 1

    #Print final stats # TODO: make this a specific function?
    print("New cpd size:", len(new_cpds))
    print("Cumulative cpd size:", len(cum_cpds))
    print("New reaction size:", len(new_rxns))
    print("Cumulative reaction size", len(cum_rxns))
    print("Generations:", count)

def main():
    fp = "Data/reaction_edges.json"
    products, substrates = load_reaction_data(fp)

    seed_list = load_seeds("Seeds/primordial.txt")

    #Run network expansion over each seed set
    for seeds in seed_list:
        run_network_expansion(seeds, products, substrates)


    #TODO: identify reactions of seed compounds


    #TODO: propogate network expansion


if __name__ == "__main__":
    main()
