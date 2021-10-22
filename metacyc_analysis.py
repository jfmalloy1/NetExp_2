import pickle
import json
import assemblycalculator as ac
import time
import multiprocessing as mp


def find_expansion_cpds(fp):
    """ Finds all unique comopunds in metacyc expansion

    Args:
        fp (string): filepath to expansion writeout

    Returns:
        list: all unqiue comopunds generated
    """
    #Load metacyc expansion
    df = pickle.load(file=open(fp, "rb"))

    #Return all unique compounds
    return [cpd for gen in list(df["compounds_new"]) for cpd in gen]


def get_cpd_dict(fp):
    """ Loads the metacyc compound dictionary

    Dictionary organization: {cpd_id: {inchi: "", smiles:"}}

    Args:
        fp (string): filepath to metacyc compound information

    Returns:
        dictionary: metacyc cpd information
    """
    with open(fp) as json_f:
        cpd_dict = json.load(json_f)

    return cpd_dict


def find_cpd_inchis(unique_cpds, cpd_dict):
    """ Find all inchi representations of unique metacyc compounds

    Args:
        unique_cpds (list): unique compounds generated from metacyc expansion
        cpd_dict (dict): links metacyc compounds with inchi and smiles

    Returns:
        dict: links unique compounds with inchi representations
    """
    cpd_inchi_dict = {}

    #Find inchi associated with each compound
    non_inchi_count = 0
    for cpd in unique_cpds:
        #If the compound does not have a inchi, count it & leave blank
        if not cpd_dict[cpd]["inchi"].startswith("InChI="):
            non_inchi_count += 1
            cpd_inchi_dict[cpd] = ""
        #Otherwise add inchi to dictionary
        else:
            cpd_inchi_dict[cpd] = cpd_dict[cpd]["inchi"]

    # print(round(non_inchi_count / float(len(unique_cpds)), 2),
    #       "% of compounds do not have inchis")

    return cpd_inchi_dict


def calculate_assembly(cpd, inchi):
    """ Uses the assembly calculator package to find the assembly index of a compound

    Args:
        cpd (string): metacyc compound ID
        inchi (string): comopund inchi descriptor

    Returns:
        set: (compound, assembly index)
    """
    return (cpd, ac.calculate_ma(inchi, 500, "exact"))


def find_assembly_values(cpd_inchi_dict):
    """ Calculate assembly values for each compound with an inchi string

    Args:
        cpd_inchi_dict (dict): Links each unique compound to inchi

    Returns:
        dict: relation from each compound to its assembly index
    """
    #Set up parallelization
    pool = mp.Pool(16)

    cpd_assembly_results = []
    cpd_assembly_results = [
        pool.apply(calculate_assembly, args=(cpd, inchi))
        for cpd, inchi in cpd_inchi_dict.items()
    ]

    pool.close()

    # for cpd, inchi in cpd_inchi_dict.items():
    #     cpd_assembly_results.append(calculate_assembly(cpd, inchi))

    #Turn sets into dictionary
    cpd_assembly_dict = {}
    for result in cpd_assembly_results:
        cpd_assembly_dict[result[0]] = result[1]

    return cpd_assembly_dict


def main():
    start = time.time()

    #Find unique compounds in expansion
    unique_cpds = find_expansion_cpds("Data/Output/CSE_0.p")

    #Get dictionary of all compounds (with inchi and smiles) in metacyc
    cpd_dict = get_cpd_dict("Data/metacyc_cpds.json")

    #Link unique compounds with inchis
    cpd_inchi_dict = find_cpd_inchis(unique_cpds, cpd_dict)

    #Calculate assembly values over all unique compounds
    cpd_assembly_dict = find_assembly_values(cpd_inchi_dict)

    #Write final assembly numbers to a json file
    with open("Data/assembly_values_parallel_largeTimeout.json", "w") as f:
        json.dump(cpd_assembly_dict, f, indent=2)

    print("Time:", time.time() - start)


if __name__ == "__main__":
    main()
