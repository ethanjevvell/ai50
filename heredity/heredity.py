import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):

    # Establish universal probabilities per person per scenario
    one_gene_dict   = {p: PROBS["gene"][1] for p in one_gene}
    two_gene_dict   = {p: PROBS["gene"][2] for p in two_genes}
    zero_gene_dict  = {p: PROBS["gene"][0] for p in people if p not in one_gene and p not in two_genes}
    has_trait_dict  = {}
    no_trait_dict   = {}

    for p in people:
        has_one_gene    = p in one_gene
        has_two_genes   = p in two_genes
        has_zero_genes  = p not in one_gene and p not in two_genes
        has_trait       = p in have_trait
        no_trait        = p not in have_trait

        if has_one_gene and has_trait:
            has_trait_dict[p]   = PROBS["trait"][1][True]
        if has_two_genes and has_trait:
            has_trait_dict[p]   = PROBS["trait"][2][True]
        if has_zero_genes and has_trait:
            has_trait_dict[p]   = PROBS["trait"][0][True]
        if has_one_gene and no_trait:
            no_trait_dict[p]    = PROBS["trait"][1][False]
        if has_two_genes and no_trait:
            no_trait_dict[p]    = PROBS["trait"][2][False]
        if has_zero_genes and no_trait:
            no_trait_dict[p]    = PROBS["trait"][0][False]

    gene_trait_dicts =  [one_gene_dict, two_gene_dict, zero_gene_dict, has_trait_dict, no_trait_dict]
    final_prob_dict = {p: 1 for p in people}

    # Calculate the joint probability for those without parents (the roots of the network)
    for p in people:
        for dict in gene_trait_dicts:
            if p in dict and not hasParents(people, p):
                final_prob_dict[p] *= dict[p]

    for p in people:
        if hasParents(people, p):
            p_mother = people[p]["mother"]
            p_father = people[p]["father"]
            mother_genes = numOfParentGenes(p_mother, one_gene, two_genes)
            father_genes = numOfParentGenes(p_father, one_gene, two_genes)

            if p in list(one_gene_dict.keys()):
                # P(one gene | child) = P(gene passed from mom, but not dad) + P(gene passed from dad, but not mom); (XOR)
                final_prob_dict[p] *= ((probParentPassesGene(mother_genes) * (1 - probParentPassesGene(father_genes)))
                                        + (probParentPassesGene(father_genes) * (1 - probParentPassesGene(mother_genes))))

            if p in list(two_gene_dict.keys()):
                # P(two genes | child) = P(gene passed from mom) * P(gene passed from dad)
                final_prob_dict[p] *= (probParentPassesGene(mother_genes) * probParentPassesGene(father_genes))

            if p in list(zero_gene_dict.keys()):
                # P(no genes | child) = P(gene NOT passed from mom) * P(gene NOT passed from dad)
                final_prob_dict[p] *= ((1 - probParentPassesGene(mother_genes)) * (1 - probParentPassesGene(father_genes)))

        for dict in [has_trait_dict, no_trait_dict]:
            if p in dict:
                final_prob_dict[p] *= dict[p]

    joint_prob = 1
    for p in final_prob_dict:
        joint_prob *= final_prob_dict[p]

    return joint_prob

def hasParents(people, p):
    return people[p]["mother"] and people[p]["father"]

def probParentPassesGene(num_of_genes):
    if num_of_genes == 0:
        return PROBS["mutation"]
    if num_of_genes == 1:
        return 0.5 * (1 - PROBS["mutation"]) + (0.5 * PROBS["mutation"])
    if num_of_genes == 2:
        return 1 - PROBS["mutation"]

def numOfParentGenes(parent, one_gene, two_genes):
    if parent in one_gene:
        return 1
    if parent in two_genes:
        return 2
    return 0

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1]        += p
        if person in two_genes:
            probabilities[person]["gene"][2]        += p
        if person not in one_gene and person not in two_genes:
            probabilities[person]["gene"][0]        += p
        if person in have_trait:
            probabilities[person]["trait"][True]    += p
        if person not in have_trait:
            probabilities[person]["trait"][False]   += p


def normalize(probabilities):
    """
    Normalize the probability distributions for each person in `probabilities`.
    """
    for person in probabilities:
        # Normalize gene distribution
        gene_sum = sum(probabilities[person]["gene"].values())
        for gene_copy in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_copy] /= gene_sum

        # Normalize trait distribution
        trait_sum = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_sum



if __name__ == "__main__":
    main()
