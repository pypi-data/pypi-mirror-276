from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit import RDLogger
import argparse

# ignore RDKit warnings
RDLogger.DisableLog('rdApp.*') 

def formula_atom_economy(reactants, products):
    """
    Calculate the atom economy of a reaction.

    Args:
        reactants (list): List of RDKit molecule objects for reactants.
        products (list): List of RDKit molecule objects for products.

    Returns:
        atom_economy (float): The atom economy as a percentage.
    """
    reactant_mass = sum([Descriptors.MolWt(mol) for mol in reactants])
    product_mass = sum([Descriptors.MolWt(mol) for mol in products])
    atom_economy = (product_mass / reactant_mass) * 100
    return atom_economy

def print_molecule_info(molecules, title):
    """
    Print information about molecules.

    Args:
        molecules (list): List of RDKit molecule objects.
        title (str): The title for the molecule group (e.g., "Reactants", "Products").
    """
    border = '=' * 50
    print(border)
    print(f"{title.upper():^50}")
    for smiles in molecules:
        mol = Chem.MolFromSmiles(smiles)
        mol_weight = f"{Descriptors.MolWt(mol):.2f} g/mol"
        mol_formula = Chem.rdMolDescriptors.CalcMolFormula(mol, False)  # False for not using Hill notation
        
        print(f"{'-' * 50}")
        print(f"{' SMILES:':<20} {smiles}")
        print(f"{' Molecular Weight:':<20} {mol_weight}")
        print(f"{' Molecular Formula:':<20} {mol_formula}")
    print(border)

def calculate_atom_economy(reactions_smiles):
    """
    Calculate overall atom economy from a list of reaction SMILES.

    Args:
        reactions_smiles (str): Reaction SMILES for multiple reactions separated by newlines.

    Returns:
        None
    """
    reactions = reactions_smiles.split('\n')  # Split reactions by newline character

    overall_reactants = []
    overall_products = []

    for reaction_smiles in reactions:
        reaction_parts = reaction_smiles.split('>')

        if len(reaction_parts) != 3:
            print("Error: Each reaction SMILES must be in the form 'reactants>agents>products'")
            continue

        reactants_smiles, agents_smiles, products_smiles = reaction_parts

        try:
            reactant_smiles_list = reactants_smiles.split('.')
            product_smiles_list = products_smiles.split('.')

            # Filter reactants on a SMILES basis
            filtered_reactants = [reactant for reactant in reactant_smiles_list if reactant not in overall_products]

            # Accumulate reactants
            overall_reactants.extend(filtered_reactants)

            # Collect products for each reaction
            overall_products.extend(product_smiles_list)
        except ValueError as e:
            print(e)
            continue

    # Convert SMILES to RDKit molecule objects
    overall_reactants_mols = [Chem.MolFromSmiles(smiles) for smiles in overall_reactants]
    overall_products_mols = [Chem.MolFromSmiles(smiles) for smiles in overall_products]

    # Use only the products from the last reaction for atom economy calculation
    last_reaction_products_mols = [Chem.MolFromSmiles(smiles) for smiles in product_smiles_list]

    atom_economy = formula_atom_economy(overall_reactants_mols, last_reaction_products_mols)

    print("\n Overall Atom Economy Calculation:")
    print(" Calculation Method: Molecular Weights \n")
    print("Used Reactants:")
    print_molecule_info(overall_reactants, " Reactants")
    print("\nUsed Products (from the last reaction):")
    print_molecule_info(product_smiles_list, " Products")
    atom_economy_str = f"{atom_economy:.2f}%"
    print(f"{' Overall Atom Economy:':<20} {atom_economy_str:<30} \n")

def main():
    """
    Main function to parse arguments and calculate overall atom economy.
    """
    parser = argparse.ArgumentParser(description='Calculate Atom Economy for reactions using Reaction SMILES.')
    parser.add_argument('reactions', type=str, help='Reaction SMILES for multiple reactions separated by newlines')
    args = parser.parse_args()

    calculate_atom_economy(args.reactions)

if __name__ == '__main__':
    main()
