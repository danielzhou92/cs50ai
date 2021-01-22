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
    all_pages = list(corpus)
    page_links = corpus[page]
    prob_dict = dict()

    if len(page_links) == 0:
        prob_per_page = 1/len(all_pages)
        for page in all_pages:
            prob_dict[page] = prob_per_page
    else:
        prob_none_page_link = (1 - damping_factor) / len(all_pages)
        prob_page_link = (damping_factor)/len(page_links)+prob_none_page_link
        for page in all_pages:
            if page in page_links:
                prob_dict[page] = prob_page_link
            else:
                prob_dict[page] = prob_none_page_link

    return prob_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus)
    page_rank = dict()
    # initialize all probibility to 0 to start
    for page in all_pages:
        page_rank[page] = 0

    # sample and update pagerank value each sample
    random.seed()
    for i in range(n):
        if i == 0:
            page = random.choice(all_pages)
        else:
            page = random.choices(list(sample.keys()), weights=list(sample.values()))[0]

        sample = transition_model(corpus, page, damping_factor)
        for key in list(sample.keys()):
            page_rank[key] += (sample[key] / n)

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus)
    curr_page_rank = dict()
    new_page_rank = dict()
    n = len(all_pages)
    links_on_page = dict()

    # initialize all probibility to 1/n to start
    for page in all_pages:
        curr_page_rank[page] = 1 / n
        links_on_page[page] = len(corpus[page])

    # iterate page rank until no page rank value changes by more than 0.001
    # calculate page rank value page by page, based on links on other pages
    while True:
        largest_pr_change = 0
        for page_p in all_pages:
            new_page_rank[page_p] = (1 - damping_factor) / n
            for page_i in all_pages:
                if page_p in corpus[page_i]:
                    new_page_rank[page_p] += damping_factor * curr_page_rank[page_i] / links_on_page[page_i]
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                elif links_on_page[page_i] == 0:
                    new_page_rank[page_p] += damping_factor * curr_page_rank[page_i] / n
            page_pr_change = abs(new_page_rank[page_p] - curr_page_rank[page_p])
            if page_pr_change > largest_pr_change:
                largest_pr_change = page_pr_change
        if largest_pr_change <= 0.001:
            break
        curr_page_rank = new_page_rank.copy()
    return new_page_rank


if __name__ == "__main__":
    main()
