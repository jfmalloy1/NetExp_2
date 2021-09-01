import os

def main():
    with open("C:/users/group/Desktop/25.1/data/reactions.dat") as f:
        rxn_data = f.read()
        rxns = rxn_data.split("//\n") #Split data on "//" character




if __name__ == "__main__":
    main()