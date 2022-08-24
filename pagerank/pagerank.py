import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Create a dictionary with pages in the corpus as keys and 0 as initial probability value
    page_probabilities = dict()
    for key in corpus:
        page_probabilities[key] = 0

    # If there are no links from the current page, all pages in corpus have the same probability
    # of being chosen
    if len(corpus[page]) == 0:
        probability_no_links = 1 / len(corpus)
        for page in page_probabilities:
            page_probabilities[page] += probability_no_links

        return page_probabilities

    # Calculate probabilities for pages linked from the current page
    probability_per_link = damping_factor / len(corpus[page])

    # Calculate probability that any page from corpus is chosen at random
    probability_for_all = (1 - damping_factor) / len(corpus)

    # Combine the probabilities
    for link in page_probabilities:
        if link in corpus[page]:
            page_probabilities[link] += probability_per_link

        page_probabilities[link] += probability_for_all

    return page_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary that will store the number of times a page was chosen as a sample
    pages_samples = dict()

    # Copy page names from corpus to the new dictionary
    for key in corpus:
        pages_samples[key] = 0

    # Initialize current page, at first, pick a random key from the corpus
    current_page = random.choice(list(corpus))
    pages_samples[current_page] += 1

    # Keep track of the number of samples
    number_of_samples = 1

    # Create samples until n is reached
    while number_of_samples < n:

        # Calculate the probabilities for the next page using the transition model function
        next_page_probabilities = transition_model(corpus, current_page, damping_factor)

        # Pick the next page (the new current page) based on the probabilities
        # The parameters to the choices function are 1) list of pages to choose from,
        # 2) the weights or probabilities when making the choice, 2) the number of values to choose (1)
        current_page = random.choices(list(next_page_probabilities),
                                      weights=list(next_page_probabilities.values()), k=1)[0]

        # Update the pages_samples dictionary by increasing the times a page was chosen by 1
        for page in pages_samples:
            if page == current_page:
                pages_samples[page] += 1

        # Update the number of samples
        number_of_samples += 1

    # Initialize a dictionary that will store the pages of the corpus with their PageRank values
    page_rank_values = dict()

    # Calculate PageRanks
    for key in corpus:
        page_rank_values[key] = pages_samples[key] / n

    return page_rank_values


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize a dictionary that will store the pages of the corpus with their PageRank values
    page_rank_values = dict()

    # At first, set each page rank to 1 / nr of pages in total
    for key in corpus:
        page_rank_values[key] = 1 / len(corpus)

    # Initialize variable to keep track of how much the pange ranks change
    max_change = 1

    # Calculate new page ranks until no page rank change is higher than 0.001
    while max_change > 0.001:

        max_change = 0

        for p in page_rank_values:
            initial_value = page_rank_values[p]

            random_from_all = ((1 - damping_factor) / len(corpus))
            links_prob = 0

            for i in page_rank_values:
                # If i has no links, it will have one link for every page in the corpus (including itself)
                if len(corpus[i]) == 0:
                    links_prob += page_rank_values[i] * (1 / len(corpus))

                # Else if i has a link to p, it randomly picks from all links on i:
                elif p in corpus[i]:
                    links_prob += page_rank_values[i] / len(corpus[i])

            page_rank_values[p] = random_from_all + (damping_factor * links_prob)

            # See if the change is higher than 0.001
            change = abs(page_rank_values[p] - initial_value)
            if change > max_change:
                max_change = change

    # Normalize the page ranks
    sum = 0
    for value in page_rank_values.values():
        sum += value

    for page, value in page_rank_values.items():
        page_rank_values[page] = value / sum

    return page_rank_values


if __name__ == "__main__":
    main()
