import os
import random
import re
import collections
import copy
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
    probability = dict()

    for key in sorted(corpus):
        probability[key] = (1 - damping_factor)/len(corpus)

    for key in corpus:

        if (key == page):
            numLinks = len(corpus[page])

            if (numLinks == 0):
                for key in corpus:
                    probability[key] = 1/len(corpus)
            
            else:
                for link in corpus[page]:
                    probability[link] += damping_factor/numLinks

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = dict()

    for key in sorted(corpus):
        pagerank[key] = 0

    chosen = random.sample(list(corpus.keys()), 1)
    samples = list()
    samples.append(chosen[0])


    while(n != 0):

        probability = transition_model(corpus, str(chosen[0]), damping_factor)

        weights = list()
        population = list()
        for key in probability:
            weights.append(probability[key])
            population.append(key)
        

        chosen = random.choices(population, weights)
        samples.append(chosen[0])

        n -= 1

    pagerank = collections.Counter(samples)

    for key in pagerank:
        pagerank[key] = pagerank[key]/10000

    return pagerank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    for key in sorted(corpus):
        pagerank[key] = 1/len(corpus)
    

    sumup = 0
    count = 0

    while True: 
        oldPagerank = copy.deepcopy(pagerank)
        count = 0


        for key in pagerank:
            for key2 in corpus:
                if (key in corpus[key2]):
                    numLinks = len(corpus[key2])
                    pr = pagerank[key2]
                    sumup += pr/numLinks

            pagerank[key] = (1 - damping_factor)/len(corpus) + damping_factor*(sumup)
            sumup = 0

            if (oldPagerank[key] - pagerank[key] < 0.001):
                count += 1
            
        if (count == len(corpus)):
            break
        
    
    return pagerank



if __name__ == "__main__":
    main()
