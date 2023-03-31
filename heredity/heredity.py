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

    j_prob = 1

    for p in people:

        p_prob = 1
        p_genes = (2 if p in two_genes else 1 if p in one_gene else 0)
        p_trait = p in have_trait

        p_mother = people[p]["mother"]
        p_father = people[p]["father"]

        if not p_father and not p_mother:
            p_prob *= PROBS["gene"][p_genes]

        else:
            mother_prob = probParentPassesGene(p_mother, one_gene, two_genes)
            father_prob = probParentPassesGene(p_father, one_gene, two_genes)

            # P(one gene | child) = P(gene passed from mom, but not dad) + P(gene passed from dad, but not mom); (XOR)
            if p_genes == 1:
                p_prob *= ((mother_prob * (1 - father_prob)) + (father_prob * (1 - mother_prob)))

            # P(two genes | child) = P(gene passed from mom) * P(gene passed from dad)
            elif p_genes == 2:
                p_prob *= mother_prob * father_prob

            # P(no genes | child) = P(gene NOT passed from mom) * P(gene NOT passed from dad)
            else:
                p_prob *= (1 - mother_prob) * (1 - father_prob)

        # Now we need to account for a person p with 0, 1, or 2 genes having or not having the trait
        p_prob *= PROBS["trait"][p_genes][p_trait]
        j_prob *= p_prob

    return j_prob

def probParentPassesGene(parent, one_gene, two_genes):
    if parent in one_gene:
        return 0.5
    if parent in two_genes:
        return 1 - PROBS["mutation"]
    return PROBS["mutation"]

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
        trait_sum = sum(probabilities[person]["trait"].values())
        gene_alpha = 1 / gene_sum
        trait_alpha = 1 / trait_sum

        probabilities[person]["gene"] = {gene: (gene_alpha * gene_prob) for gene, gene_prob in probabilities[person]["gene"].items()}
        probabilities[person]["trait"] = {trait: (trait_alpha * trait_prob) for trait, trait_prob in probabilities[person]["trait"].items()}


if __name__ == "__main__":
    main()
