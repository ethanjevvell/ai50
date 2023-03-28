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

    pages = corpus[page]

    if not pages:
        probability = 1 / len(corpus)
        return {page: probability for page in corpus}

    initProbability = 1 / len(pages)
    probabilities = {p: (initProbability * damping_factor) for p in pages}
    probabilities[page] = 0

    dampProbability = (1 - sum(probabilities.values())) / len(probabilities)

    return {p: probabilities[p] + dampProbability for p in probabilities}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {name: 0 for name in corpus}
    page = random.choice(list(corpus.keys()))

    while n > 0:
        page_rank[page] += 1
        dist = transition_model(corpus, page, damping_factor)
        keys = list(dist.keys())
        values = list(dist.values())
        page = random.choices(keys, weights=values, k=1)[0]
        n -= 1

    page_rank_sum = sum(page_rank.values())
    return {p: page_rank[p] / page_rank_sum for p in page_rank}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    old_page_ranks = {p: 0 for p in corpus}
    new_page_ranks = {p: 1 / len(list(corpus.keys())) for p in corpus}
    threshold = 0.001

    while not within_threshold(new_page_ranks, old_page_ranks, threshold):
        old_page_ranks = new_page_ranks.copy()
        dampen_term = (1 - damping_factor) / len(corpus)

        for page in new_page_ranks:
            iterative_term = 0

            for i in corpus:
                if page in corpus[i]:
                    iterative_term += (old_page_ranks[i] /
                                       num_links(corpus, i))

            rank = dampen_term + (damping_factor * iterative_term)
            new_page_ranks[page] = rank

    return new_page_ranks


def num_links(corpus, i):
    links = len(corpus[i])
    if links:
        return links
    return len(list(corpus.keys()))


# Tests if every value of the new ranks are within the 0.001 threshold of the old ranks
def within_threshold(old_ranks, new_ranks, threshold):
    return all(abs(old_ranks[p] - new_ranks[i]) < threshold for p, i in zip(old_ranks, new_ranks))


if __name__ == "__main__":
    main()
