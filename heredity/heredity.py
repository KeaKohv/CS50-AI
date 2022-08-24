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

    # Initialize the return value to 1
    joint_probability = 1

    # Iterate over all members of the family:
    for person in people:

        # Check if the person has 0, 1 or 2 of the mutated versions of the gene
        person_genes = (2 if person in two_genes
                        else 1 if person in one_gene
                        else 0)

        # Check if person has a mother and father in the dataset
        mother = people[person]['mother'] or None
        father = people[person]['father'] or None

        # Initialize the probabilty calculated for this person to 0
        person_probability = 0

        # If dataset has no info about parents, unconditional probability is used
        # to calculate the probability that the person has 0, 1 or two mutated genes
        if not mother and not father:
            person_probability = PROBS['gene'][person_genes]

        # If parents are known, their data is used to calculated the probability of
        # the number of mutated genes the person has:
        else:
            # Calculate the probability that the person gets a mutated gene from their mother
            if mother in two_genes:
                mother_probability = 1 - PROBS['mutation']
            elif mother in one_gene:
                mother_probability = 0.5
            else:
                mother_probability = PROBS['mutation']

            # Calculate the probability that the person gets a mutated gene from their father
            if father in two_genes:
                father_probability = 1 - PROBS['mutation']
            elif father in one_gene:
                father_probability = 0.5
            else:
                father_probability = PROBS['mutation']

            # Calculate the probability that the person has 2, 1 or 0 mutated genes
            if person_genes == 2:
                # Prob of getting 2 mutated genes is equal to the probability of getting
                # a mutated gene from the mother AND a mutated gene from the father
                person_probability = mother_probability * father_probability
            elif person_genes == 1:
                # Prob of getting 1 mutated gene is equal to the probability of
                # getting a mutated gene from either the father OR the mother
                person_probability = (1 - mother_probability) * father_probability + (1 - father_probability) * mother_probability
            else:
                # Probability of getting 0 mutated genes is equal to the probability
                # of NOT getting a mutated gene from the mother and NOT getting it from the father
                person_probability = (1 - mother_probability) * (1 - father_probability)

        # The probability of having the trait is multiplied with the person's number of mutated genes:
        person_probability *= PROBS['trait'][person_genes][person in have_trait]

        # Include the person in the joint probability calculation
        joint_probability *= person_probability

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Add the joint probability depending on if person is in one_gene or two_genes
    # and if the person is in have_trait
    for person in probabilities:
        number_of_mut_genes = (2 if person in two_genes
                              ``else 1 if person in one_gene
                              else 0)

        # Update person's probability distributions
        probabilities[person]['gene'][number_of_mut_genes] += p
        probabilities[person]['trait'][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:

        # Sum all values of the gene and trait probability sets
        gene_sum = sum(probabilities[person]['gene'].values())
        trait_sum = sum(probabilities[person]['trait'].values())

        # Normalise both distributions
        for i in range(0, 3):
            probabilities[person]["gene"][i] /= gene_sum

        for i in range(0, 2):
            probabilities[person]["trait"][i] /= trait_sum


if __name__ == "__main__":
    main()
