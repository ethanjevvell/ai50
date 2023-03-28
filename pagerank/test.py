
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


corpus = {"1.html": {"2.html", "3.html"},
          "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damping_factor = 0.85

print(iterate_pagerank(corpus, damping_factor))
