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
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    joint = 1

    
    for person in people:
        if (people[person]["mother"] == None) and (people[person]["father"] == None):

            if (person in one_gene):
                prob = PROBS["gene"][1] * PROBS["trait"][1][(person in have_trait)]

            elif (person in two_genes):
                prob = PROBS["gene"][2] * PROBS["trait"][2][(person in have_trait)]

            else:
                prob = PROBS["gene"][0] * PROBS["trait"][0][(person in have_trait)]
            

            
        else:

            # For the mother

            if (people[person]["mother"] not in one_gene) and (people[person]["mother"] not in two_genes):
                probGetFromMother = PROBS["mutation"]
                probNotGetFromMother = 1 - PROBS["mutation"]

            elif (people[person]["mother"] in one_gene):
                probGetFromMother = 0.5
                probNotGetFromMother = 0.5

            elif (people[person]["mother"] in two_genes):
                probGetFromMother = 1 - PROBS["mutation"]
                probNotGetFromMother = PROBS["mutation"]
            

            # For the father

            if (people[person]["father"] not in one_gene) and (people[person]["father"] not in two_genes):
                probGetFromFather = PROBS["mutation"]
                probNotGetFromFather = 1 - PROBS["mutation"]

            elif (people[person]["father"] in one_gene):
                probGetFromFather = 0.5
                probNotGetFromFather = 0.5

            elif (people[person]["father"] in two_genes):
                probGetFromFather = 1 - PROBS["mutation"]
                probNotGetFromFather = PROBS["mutation"]


            """
            if the child only gets one gene, we must presume that either he gets the gene from his mother 
            and not his father, or he gets the gene from his father and not his mother
            """
            if (person in one_gene):
                """
                if the child only gets one gene, we must presume that either he gets the gene from his mother 
                and not his father, or he gets the gene from his father and not his mother
                """
                gene = 1
                prob = (probGetFromFather*probNotGetFromMother + probGetFromMother*probNotGetFromFather)*PROBS["trait"][gene][(person in have_trait)]
            elif (person in two_genes):
                """
                if the child gets two genes, we must presume that he gets gene both
                from his mother and his father
                """
                gene = 2
                prob = (probGetFromFather*probGetFromMother)*PROBS["trait"][gene][(person in have_trait)]
            else:
                """
                if the child gets no genes, we must presume that he gets neither from 
                his mother nor his father
                """
                gene = 2
                prob = (probNotGetFromFather*probNotGetFromMother)*PROBS["trait"][gene][(person in have_trait)]
            

        joint *= prob
    
    
    return joint



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if (person in one_gene):
            probabilities[person]["gene"][1] += p
        elif (person in two_genes):
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        

        if (person in have_trait):
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p
        

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = 0
        for gene in probabilities[person]["gene"]:
            total += probabilities[person]["gene"][gene]

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= total 


        total = 0
        for trait in probabilities[person]["trait"]:
            total += probabilities[person]["trait"][trait]

        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= total



if __name__ == "__main__":
    main()
