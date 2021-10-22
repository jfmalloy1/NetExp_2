# NetExp_2

Python version of Network Expansion (Handorf, 2005). 
Takes in seed compounds and a defined network of reactions & compounds, and calculates the possible scope of compounds generated from the seeds.
This algorithm as is ignores thermodynamics and concentrations - if a compound is present in the scope, it is considered universally available. 
Also, if all products OR all reactants are present of a reaction, the reaction is considered functional and the other side (either products or 
reactants) will be added to the scope.

## Runtime Instructions
1. Seeds: Upload .txt file with seeds to the `Seeds` directory and specify the file location as an input to the `load_seeds()` method. 
All seeds should be entered on one line with a single space between each, e.g. `C1 C2 C3`.
Multiple seed sets (for multiple expansions) can be entered by utilizing multiple lines.
2. Reaction List: a .json file of reactions should be uploaded to the `Data` directory, and the file location should be specified in the `fp` variable in `main()`.
3. Using Python 3, run the netexp.py file.

## Output
Output will be generated as pickle files to the `Data\Output\` directory. If multiple seed sets are entered, the output will be numbered with "_0, _1, ...".
