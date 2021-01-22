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
    joint_prob = 1

    for person in people.values():
        # convert the number of copy of the gene that the person has into a number
        gene_num = convert_gene_to_num(one_gene, two_genes, person['name'])

        # convert the have_trait variable to boolean
        trait = convert_trait_to_bool(have_trait, person['name'])

        # if person has known father and mother, calculate it like this
        if person['mother'] and person['father']:
            # calculate probability of getting a gene from mother, as well as from father (seperately)
            get_from_father = chance_to_pass_gene(
                one_gene, two_genes, person['father'])
            get_from_mother = chance_to_pass_gene(
                one_gene, two_genes, person['mother'])
            not_from_father = 1 - get_from_father
            not_from_mother = 1 - get_from_mother

            if gene_num == 0:
                # probability of not getting it from either
                prob_gene = not_from_father * not_from_mother
            elif gene_num == 1:
                # probability of getting one from either and none from the other
                prob_gene = get_from_father * not_from_mother + not_from_father * get_from_mother
            else:
                # probability of getting one from each parent
                prob_gene = get_from_father * get_from_mother

        # if person has no known father and mother, calculater it like this
        else:
            prob_gene = PROBS['gene'][gene_num]

        prob_trait = prob_gene * PROBS['trait'][gene_num][trait]

        joint_prob *= prob_trait

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # convert the number of copy of the gene that the person has into a number
        gene_num = convert_gene_to_num(one_gene, two_genes, person)

        # convert the have_trait variable to boolean
        trait = convert_trait_to_bool(have_trait, person)

        probabilities[person]['gene'][gene_num] += p
        probabilities[person]['trait'][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_prob_sum = sum(probabilities[person]['gene'].values())
        trait_prob_sum = sum(probabilities[person]['trait'].values())
        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] /= gene_prob_sum
        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] /= gene_prob_sum


def convert_gene_to_num(one_gene, two_genes, person):
    # convert the number of copy of the gene that the person has into a number
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0


def convert_trait_to_bool(have_trait, person):
    # convert the have_trait variable to boolean
    if person in have_trait:
        return True
    else:
        return False


def chance_to_pass_gene(one_gene, two_genes, person):
    # convert the number of copy of the gene that the person has into a number
    if person in one_gene:
        # this is calculated bu summing the chance of the 1 gene being passed on and not mutating, together with the chance of the none-gene mutating and being passed on
        # the mutating chance cancells out therefor its just 0.5
        # since we are not worrying about efficiency in the program, for clarity, just leave the canceling out part to the computer
        return 0.5 - PROBS['mutation'] + PROBS['mutation']
    elif person in two_genes:
        return 1 - PROBS['mutation']
    else:
        return PROBS['mutation']


if __name__ == "__main__":
    main()
