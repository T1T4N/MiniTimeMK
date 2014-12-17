import collections
import heapq
import math
import re


def millis():
    """
    :return: A millisecond approximation of the current time
    """
    import time
    return int(round(time.time() * 1000))


def get_all_posts():
    """
    Get all posts from the database.

    :return: List containing every post as a string
    """
    rows = []
    for row in db((db.posts.source == db.rssfeeds.source) & (db.posts.category == db.rssfeeds.category)).select(db.posts.ALL):
        text = row.text
        text = re.sub('\n', ' ', text)
        text = re.sub('\s+', ' ', text)
        rows.append(text)
    return rows


def heap_remove_at_index(heap, idx):
    """
    Removes the element at index idx in heap with O(logN) complexity.

    :param heap: The heap from which the element should be removed
    :param idx: The index at which the element should be removed
    :return: The value of the removed element
    """
    if idx == len(heap)-1:
        return heap.pop()

    result = heap[idx]
    heap[idx] = heap.pop()
    heapq._siftup(heap, idx)
    return result


def heap_remove_element(heap, element):
    """
    Removes the given element from the heap while preserving the structure. Done in O(logN) time.

    :param heap: A list which represents a heap
    :param element: The element to be removed
    :return: Nothing
    """
    index = heap.index(element * (-1))
    heap_remove_at_index(heap, index)


def term_frequency(term, post):
    """
    Calculates the term frequency in a document.

    :param term: The term whose frequency should be calculated
    :param post: The document in which to count
    :return: The frequency of the term
    """
    total = post.count(term)
    return 1.0 * total / len(post)


def inverse_document_frequency(term, documents):
    """
    Calculates inverse document frequency for the term in all the documents.

    :param term: The term whose inverse document frequency should be calculated
    :param documents: The set of documents in which to search. The "in" operator is O(1) in set, and O(n) in list
    :return: The inverse document frequency of the term
    """
    total = 1
    for document in documents:
        if term in document:
            total += 1
    return math.log(1.0 * len(documents) / total)


def tf_idf(document, docs_splitted):
    """
    Calculates the top 12 tf-idf keywords of a document.

    :param document: The document whose tf-idf should be calculated, represented as a string list
    :param docs_splitted: A list of the documents' words represented as string lists
    :return:
    """

    tokens = {}
    words_sets = []

    for doc_words in docs_splitted:
        words_sets.append(set(doc_words))

    for term in document:
        weight = term_frequency(term, document) * inverse_document_frequency(term, words_sets)
        tokens[term] = weight

    sorted_tokens = sorted(tokens.items(), key=lambda item: item[1], reverse=True)

    ret = collections.defaultdict(lambda: 0)
    if len(sorted_tokens) > 13:
        for j in range(12):
            term = sorted_tokens[j][0]
            weight = sorted_tokens[j][1]
            # print term, ' <-> ', weight
            ret[term] = weight
        return ret
    return {}


def cosine_similarity(d1, d2):
    """
    Calculates cosine similarity between two tf-idf vectors.

    :param d1: Vector 1
    :param d2: Vector 2
    :return: The cosine similarity between vectors d1 and d2
    """

    upper_sum = 0
    for n in d1:
        if n in d2:
            upper_sum = upper_sum + d1[n]*d2[n]

    if upper_sum == 0:  # If upper_sum = 0, no need to calculate the lower sums
        return 0

    normalization_sum1 = 0.0
    normalization_sum2 = 0.0

    for br in d1.values():
        normalization_sum1 += br*br

    for br in d2.values():
        normalization_sum2 += br*br

    normalization_sum1 = math.sqrt(normalization_sum1)
    normalization_sum2 = math.sqrt(normalization_sum2)

    # upper_sum / (normalization_sum1 * normalization_sum2)
    return 1.0 * upper_sum / (normalization_sum1 * normalization_sum2)


def merge_texts(doc1, doc2, docs_splitted):
    """
    Merges the string contents of two documents, and calculates the top 12 keywords.

    :param doc1: A list containing the words of the first document
    :param doc2: A list containing the words of the second document
    :param docs_splitted: A list containg the words of all documents
    :return: The top 12 tf-idf keywords of the merged document
    """
    result = doc1 + doc2
    docs_splitted.append(result)
    res = tf_idf(result, docs_splitted)
    return res


def init_fill_heap(vectors, score_pair, reverse_score_pair, heap):
    """
    Initial calculation of similarity for each pair of tf-idf vectors.

    :param vectors: A list of the tf-idf vectors for the documents
    :param score_pair: An empty dictionary to be filled with score : pair key-value pairs
    :param reverse_score_pair: A reverse dictionary of score_pair (simVec) to be filled with pair : score key-value pairs
    :param heap: An empty list to be used as a heap
    :return: Fills score_pair (simVec), reverse_score_pair (vecSim) and heap with the corresponding data
    """

    n = len(vectors)
    for i in range(n):
        for j in range(i + 1, n):
            d1 = vectors[i]
            d2 = vectors[j]
            score = cosine_similarity(d1, d2)
            # score = trunc(score, 12)

            if score > 1.0:
                score = 1.0

            if score > 0.6:
                print score, " : ", i, " ", j

                # TODO: Refactor reverse_score_pair (vecSim) to use (i, j) tuples as keys
                score_pair[score] = score_pair.get(score, [])+[[i, j]]
                reverse_score_pair[i] = reverse_score_pair.get(i, []) + [score]
                reverse_score_pair[j] = reverse_score_pair.get(j, []) + [score]
                heapq.heappush(heap, score*(-1))


def get_most_similar(score_pair, reverse_score_pair, heap):
    """
    Return the largest value for similarity between two vectors.

    :param score_pair: A dictionary containing score : pair key-value pairs
    :param reverse_score_pair: A reverse dictionary of score_pair (simVec) containing pair : score key-value pairs
    :param heap: The heap of similarity scores
    :return:
    """
    max_score = heapq.heappop(heap) * (-1)
    result_pair = score_pair[max_score].pop()
    reverse_score_pair[result_pair[0]].remove(max_score)
    reverse_score_pair[result_pair[1]].remove(max_score)

    # Performs dictionary cleaning of every non-optimal pair:score occurrence

    # while vecSim[result_pair[0]] != []:
    while reverse_score_pair[result_pair[0]]:
        score = reverse_score_pair[result_pair[0]].pop()
        heap_remove_element(heap, score)
        removed_pairs = []

        for pair in score_pair[score]:
            if result_pair[0] in pair:  # Remove pair if it contains either i or j
                score_pair[score].remove(pair)
                removed_pairs = removed_pairs + pair
        for pair in removed_pairs:
            if pair != result_pair[0]:
                reverse_score_pair[pair].remove(score)

    while reverse_score_pair[result_pair[1]]:
        score = reverse_score_pair[result_pair[1]].pop()
        heap_remove_element(heap, score)
        removed_pairs = []

        for pair in score_pair[score]:
            if result_pair[1] in pair:
                score_pair[score].remove(pair)
                removed_pairs = removed_pairs + pair
        for pair in removed_pairs:
            if pair != result_pair[1]:
                reverse_score_pair[pair].remove(score)

    return result_pair


def hac(heap, vectors, score_pair, reverse_score_pair, docs_splitted):
    """
    Performs Hierarchical Agglomerative Clustering on the given posts.

    :param heap: A heap containing cosine similarities between the posts
    :param vectors: A list containing the 12 tf-idf keywords of the posts
    :param score_pair: A dictionary containing score : pair key-value pairs
    :param reverse_score_pair: A reverse dictionary of score_pair (simVec) containing pair : score key-value pairs
    :param docs_splitted:
    :return: A dictionary containing cluster_id : posts_id key-value pairs
    """
    hash_merged = {}
    k = len(vectors)
    deleted = []

    while heap:
        result_pair = get_most_similar(score_pair, reverse_score_pair, heap)
        deleted = deleted + result_pair
        merged_vector = merge_texts(docs_splitted[result_pair[0]], docs_splitted[result_pair[1]], docs_splitted)
        vectors.append(merged_vector)

        for i in range(len(vectors)-1):     # ovoa e smeneto
            if i not in deleted:
                d1 = vectors[i]
                score = cosine_similarity(d1, merged_vector)
                # score = trunc(score, 12)

                if score > 1.0:
                    print 'Score bigger than 1: %f' % score
                    score = 1.0
                if score > 0.6:
                    # print score, " : ", i, " ", K
                    score_pair[score] = score_pair.get(score, [])+[[i, k]]
                    reverse_score_pair[i] = reverse_score_pair.get(i, []) + [score]
                    reverse_score_pair[k] = reverse_score_pair.get(k, []) + [score]
                    heapq.heappush(heap, score*(-1))

        hash_merged[k] = result_pair
        k += 1
    return hash_merged


def clustering():
    """
    Main clustering function.

    :return: A map with cluster_id : list_of_posts_ids key-value pairs
    """

    docs = get_all_posts()
    docs_splitted = []
    vectors = []
    score_pair = {}
    reverse_score_pair = {}
    heap = []

    print 'Posts splitting started'
    t1 = millis()
    for i, post in enumerate(docs[:500]):
        post_words = post.split(' ')
        docs_splitted.append(post_words)
        print i, " : ", " ".join(post_words)
    t2 = millis()
    print 'Posts splitted in %d ms' % (t2 - t1)

    print 'tf-idf started'
    t1 = millis()
    for i in range(len(docs_splitted)):
        vectors.append(tf_idf(docs_splitted[i], docs_splitted))
    t2 = millis()
    print 'tf-idf finished in %d ms' % (t2 - t1)

    print 'Initial heap filling started'
    t1 = millis()
    init_fill_heap(vectors, score_pair, reverse_score_pair, heap)
    t2 = millis()
    print 'Heap initially filled in %d ms' % (t2 - t1)

    print 'HAC started'
    t1 = millis()
    result = hac(heap, vectors, score_pair, reverse_score_pair, docs_splitted)
    t2 = millis()
    print 'HAC finished in %d ms' % (t2 - t1)

    eliminated = set([])
    final_dict = {}
    for key in sorted(result, reverse=True):
        post_ids = []
        eliminated.add(key)
        for c_id in result[key]:
            if c_id not in eliminated:
                post_ids += get_children_clusters(result, c_id, eliminated)
        if post_ids:    # Skip empty arrays
            final_dict[key] = post_ids
        print key, ' ', result[key]

    print 'DONE 1'

    for key in sorted(final_dict, reverse=True):
        print key, ' ', final_dict[key]


def get_children_clusters(result_dict, key, eliminated):
    ret = []
    eliminated.add(key)
    if result_dict.get(key, None) is None:
        ret.append(key)
    else:
        for c_id in result_dict[key]:
            if c_id not in eliminated:
                # eliminated.add(c_id)
                ret += get_children_clusters(result_dict, c_id, eliminated)
    return ret