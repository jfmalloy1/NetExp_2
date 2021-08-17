import json

def load_reaction_data(fp):
    #TODO: function comments
    with open(fp) as json_file:
        data = json.load(json_file)

        print(data["products"])

    #TODO: what data is necessary to return?

def main():
    fp = "Data/reaction_edges_curated.json"
    load_reaction_data(fp)

    #TODO: load seed compounds

    #TODO: identify reactions of seed compounds

    #TODO: propogate network expansion

if __name__ == "__main__":
    main()