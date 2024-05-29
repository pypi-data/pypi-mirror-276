"""# 
Doc::

    #### install
        pip install datasketch narrow-down


    #### Infos Duplicate Text:

        https://github.com/topics/hypothesis-testing?l=python&o=desc&s=stars

        https://pypi.org/project/pysie/#description

       https://pypi.org/project/narrow-down/
       https://pypi.org/project/pyhyperminhash/
       https://github.com/bradhackinen/vminhash 

      

     ### Minhas algo

        MinHash is an approximation of the Jaccard similarity between two sets. If you assume the output space of a hash function is uniformly distributed, and you hash each element of a set and take the minimum (or maximum, doesn't matter) hash value, that can be thought of as a uniform random variable. In other words, it's the same as randomly drawing one element from the set.

        This by itself isn't that useful, until you realize that hash functions are deterministic. Each random draw will be the same for each seed if given the same input. Even just with one, this is already clearly an approximation of the jaccard index, just with a very low sample size.

        MinHash takes this a step further by computing many hashes with different seeds for each input variable. If you, say, hash each element 150 times and taken the minimum for each, the law of large numbers says that the average of these 150 minimums will be very close to the true jaccard index. So you can use this set of 150 minimums as a signature for each document, and compare the signatures to find similar documents.

        The problem comes with large scale, as each similarity search is O(N), requiring you to search across every other already sampled document. And that is just for a single document. If you have millions of sets to compare, this becomes very slow.

        This is where Locality Sensitive Hashing comes in. MinHash LSH can be done in a few ways, and I currently implemented the more simple mechanism. The idea is that if you have a signature of 200 hashes, you go over it and re hash the concatenated hashes of, say, 10 hashes at a time. This leaves you with a smaller (but fuzzier) signature of 20 hashes. For each of these 20 hashes we have buckets (in this case, a simple list of 20 dictionaries) that we store bighash: [docID1, docID2, ...]. If two items are duplicates, they will likely have at least on hash in common. So we now just look through all the buckets and find the hashes with more than one document in them. We then check the documents in each bucket to see if they are actually similar (either with minhash or the original jaccard index). This is much faster than checking every document against every other document, and the tradeoff is that we will have some false positives, and it's not as good for things that aren't as similar.

        This is a special version of LSH in general, with the more generalized one consisting of generating a bunch of random hyperplanes (random normal / norm(random_normal)) in a high dimensional space (with d being the dimensionality of the input data, in this case how many minhash permutations). Then, when querying, you simply take the dot product of your query vectors against these projections and then bucket them based on the sign of the result. This effectively creates buckets in a very efficient way, and lowers the search space dramatically. I have only implemented up to here, but iirc then within the buckets you can directly compare them similar to before, often using things like the hamming distance (bitwise method) to make it especially fast. As far as I can understand, this is much better for more continuous variables you want to intersect, like normal vector embeddings. For hashes of documents the hashes themselves don't mean all that much, and the minhash method is more than sufficient (and likely faster/so close it doesn't matter). Take everything I said in second half of paragraph with grain of salt.


"""
import os,sys,  pandas as pd, numpy as np
from typing import List
from utilmy import log

import asyncio
import narrow_down as nd
from narrow_down.storage import StorageLevel
from typing import Iterable

from datasketch import MinHash, MinHashLSH
import numpy as np


from datasketch import MinHash, MinHashLSH
from concurrent.futures import ThreadPoolExecutor


########################################################################
def test2():
    """function test

        
    """
    from difflib import SequenceMatcher
    from pandas._testing import assert_series_equal

    list1 = ['dog', 'cat']
    list2 = ['doggy', 'cat']

    cols = ['name','pet_name']
    sample_df = pd.DataFrame(zip(list1, list2), columns=cols)
    original_value = pd_text_similarity(sample_df, cols)['score']

    check_similarity = lambda *x: SequenceMatcher(None, *x[0]).ratio()
    
    output_value = pd.Series(sample_df.apply(lambda x: check_similarity(x[[*cols]]), axis=1), name="score")

    assert_series_equal(original_value, output_value, check_names=False)

    log(pd_text_getcluster )
    test_lsh()
      





#############################################################################
def test3():

  column_name = "question1"
  threshold = 0.7
  num_perm = 10
  num_items = 100000

  url = "https://raw.githubusercontent.com/AlexAdvent/utilmy-data/main/text_question.csv"
  df = pd.read_csv(url)
  print(df.head())

  df1 = pd_text_getcluster(
        df.head(num_items), column_name, threshold, num_perm)
  log(df1.head())

  df2 = pd_text_similarity(df, cols=['question1','question2'])
  matched = df.loc[df['score'] >= 0.8]
  print("match using SequenceMatcher is",matched.shape[0])
  print(matched.head())

  df2 = pd_text_similarity(df, cols=['question1','question2'],algo="rapidfuzz")
  matched = df.loc[df['score'] >= 80]
  print("match using rapidfuzz is",matched.shape[0])

  df2 = pd_text_similarity(df, cols=['question1','question2'],algo="editdistance")
  matched = df.loc[df['score'] >= 80]
  print("match using editdistance is",matched.shape[0])


def test_lsh():
    """function test_lsh
    Args:
    Returns:
        
    """

    ll = ['aa bb cc', 'a b c', 'cc bb cc']
    column_name = "sentence"
    threshold = 0.7
    num_perm = 10
    num_items = 100000

    df = pd.DataFrame(ll, columns=[column_name])
    df1 = pd_text_getcluster(
        df.head(num_items), column_name, threshold, num_perm)
    print(df1)


def test(algo="default"):
    text_list1 = nlp_generate_random_sentences(10000)
    text_list2 = nlp_generate_random_sentences(5000)
    text_list2 = text_list2 + text_list1[:5000]

    func = np_find_duplicate_text
    if algo == "fast":
        func = np_find_duplicate_text_fast
        print("running datasketch fast")
    elif algo == "narrow":
        func = np_find_duplicate_text_narrow
        print("running narrow-down")
    else:
        print("running datasketch default")

    result = func(text_list1, text_list2, threshold=0.7)
    count = 0
    for _, v in result.items():
        if len(v) > 0:
            count += 1

    assert count == 5000

    text_list1 = nlp_generate_random_sentences(10000)
    text_list2 = nlp_generate_random_sentences(10000)
    text_list1[1000] = "What is the wildest thing you have ever done in your life?"
    text_list2[1001] = "What is the wildest thing you have ever done in life?"

    text_list1[2000] = "How much Pepto Bismol should I give my dogs?"
    text_list2[3000] = "How much Pepto Bismol should I give my dog?"

    result = func(text_list1, text_list2, threshold=0.7)
    assert result[1000][0][0] == 1001
    assert result[2000][0][0] == 3000


def test_single(algo="default"):
    text_list = nlp_generate_random_sentences(5000)
    text_list += text_list
    func = np_find_duplicate_single
    if algo == "narrow":
        func = np_find_duplicate_text_narrow_single
    def execute():
        result = func(text_list, threshold=0.7)

        count = 0
        for _, v in result.items():
            if len(v) > 0:
                count += 1

        assert count == 5000

    import timeit
    t = timeit.Timer(execute)
    count = 5
    print('time taken for duplicate check is ', t.timeit(count)/count)

    text_list = nlp_generate_random_sentences(5000)
    text_list[1000] = "What is the wildest thing you have ever done in your life?"
    text_list[1001] = "What is the wildest thing you have ever done in life?"

    text_list[2000] = "How much Pepto Bismol should I give my dogs?"
    text_list[3000] = "How much Pepto Bismol should I give my dog?"

    result = func(text_list, threshold=0.7)
    assert result[1000][0] == 1001
    assert result[2000][0] == 3000





#############################################################################
##### data-sketchv     ##################################
def np_find_duplicate_text(text_list1: list, text_list2: list, threshold=0.7):
    """function np_find_duplicate_text
    Args:
        text_list1: list
        text_list2: list
        threshold: float

    Returns: Dict

         {  
            text_id1 : list of (text2_id, score) where scorre> threshold [(0, 0.9), (1, 0.8), ....  ]
                         text2_id : index in text_list2

             0 :   [(0, 0.9), (1, 0.8), ....  ]    
         }

    ### Example usage
      text_list1 = ["hello world", "foo bar", "lorem ipsum"]
      text_list2 = ["hello world", "foo baz", "lorem ipsum dolor"]

      result = np_find_duplicate_text(text_list1, text_list2, threshold=0.7)
      print(result)

    """
    init_min = MinHash() # create a minhash for reusing the permutations (saves init time)
    def get_minhash(text):
        m = MinHash(permutations=init_min.permutations)
        for word in text.split():
            m.update(word.encode('utf8'))
        return m

    # Create MinHash objects for each text in both lists
    minhashes1 = [get_minhash(text) for text in text_list1]


    # minhashes2 = [get_minhash(text) for text in text_list2]
    # Create LSH index
    #lsh = MinHashLSH(threshold=threshold)
    #for i, m in enumerate(minhashes2):
    #    lsh.insert(f"text2_{i}", m)


    # Create LSH index
    lsh = MinHashLSH(threshold=threshold)
    minhashes2 = []
    for i, text in enumerate(text_list2):
       mhash2 = get_minhash(text)
       lsh.insert(f"text2_{i}", mhash2)
       minhashes2.append(mhash2)


    # Find duplicates
    ddict = {}
    for text1_id, m1 in enumerate(minhashes1):
        ddict[text1_id] = []
        for j in lsh.query(m1):
            text2_id = int(j.split('_')[1])
            score    = m1.jaccard(minhashes2[text2_id])
            if score > threshold:
                ddict[text1_id].append((text2_id, score))

    return ddict

def np_find_duplicate_single(text_list: list, threshold=0.7):
    """Find duplicate texts in a list of texts using MinHash and Locality-Sensitive Hashing (LSH).

    Args:
        text_list (list): A list of texts to search for duplicates.
        threshold (float, optional): The similarity threshold for considering two texts as duplicates. Defaults to 0.7.

    Returns:
        dict: A dictionary mapping each unique text to a list of duplicate texts.

    Algorithm:
        1. Initialize a MinHash object for reusing permutations (saves initialization time).
        2. Define a helper function `get_minhash` to compute the MinHash of a given text.
        3. Create a MinHashLSH object with the given threshold.
        4. Iterate over the text list and compute the MinHash of each text using the `get_minhash` function.
        5. Insert each MinHash into the LSH index.
        7. If any similar MinHashes are found, add the bucket of indices to the set of duplicates.
        8. Convert the set of duplicates to a dictionary, where each unique text is mapped to a list of duplicate texts.
        9. Return the resulting dictionary.

    Note:
        - The MinHash algorithm approximates the Jaccard similarity between two sets.
    """    
    init_min = MinHash() # create a minhash for reusing the permutations (saves init time)
    def get_minhash(text):
        mh = MinHash(permutations=init_min.permutations)
        for word in text.split():
            mh.update(word.encode('utf8'))
        return mh

    lsh = MinHashLSH(threshold=threshold)
    minhashes = []
    for i, text in enumerate(text_list):
        mhash = get_minhash(text)
        lsh.insert(i, mhash)
        minhashes.append(mhash)

    ###Iterate over the MinHashes and query the LSH index for similar MinHashes.
    duplicates = set()
    for i, mh in enumerate(minhashes):
        bucket = lsh.query(mh)
        matches = [bi for bi in bucket if bi != i and mh.jaccard(minhashes[bi]) > threshold]
        if len(matches) > 0:
            duplicates.add(tuple(bucket))

    ddict = {}
    for d in duplicates:
        ddict[d[0]] = d[1:]

    return ddict

def np_find_duplicate_text_fast(text_list1: list, text_list2: list, threshold=0.7):
    """function np_find_duplicate_text
    Args:
        text_list1: list
        text_list2: list
        threshold: float
    Returns: Dict

    # Example usage
    text_list1 = ["hello world", "foo bar", "lorem ipsum"]
    text_list2 = ["hello world", "foo baz", "lorem ipsum dolor"]

    result = np_find_duplicate_text_fast(text_list1, text_list2, threshold=0.7)
    print(result)


    """
    init_min = MinHash() # create a minhash for reusing the permutations (saves init time)
    def get_minhash(text):
        m = MinHash(permutations = init_min.permutations)
        for word in text.split():
            m.update(word.encode('utf8'))
        return m

    # Create MinHash objects for each text in both lists using parallel processing
    with ThreadPoolExecutor() as executor:
        minhashes1 = list(executor.map(get_minhash, text_list1))
        minhashes2 = list(executor.map(get_minhash, text_list2))

    # Create LSH index
    lsh = MinHashLSH(threshold=threshold)
    for i, m in enumerate(minhashes2):
        lsh.insert(i, m)

    # Find duplicates using parallel processing
    def find_duplicates(i, m):
        matches = []
        for j in lsh.query(m):
            score = m.jaccard(minhashes2[j])
            if score > threshold:
                matches.append((j, score))
        return (i, matches)

    result = {}
    with ThreadPoolExecutor() as executor:
        for i, matches in executor.map(lambda x: find_duplicates(*x), enumerate(minhashes1)):
            result[i] = matches

    return result



##### narrow-down algo  ################################
def np_find_duplicate_text_narrow(text_list1, text_list2, threshold=0.7):
    """Finds duplicate texts in two lists of texts using the narrow approach.

    Args:
        text_list1 (List[str]): The first list of texts.
        text_list2 (List[str]): The second list of texts.
        threshold (float, optional): The similarity threshold for finding duplicates. Defaults to 0.7.

    Returns:
        Dict[int, List[Tuple[int, float]]]: A dictionary mapping each text ID in text_list1 to a list of tuples containing the text ID and Jaccard similarity score of the duplicate texts.

    Example Usage:
        text_list1 = ["hello world", "foo bar", "lorem ipsum"]
        text_list2 = ["hello world", "foo baz", "lorem ipsum dolor"]

        result = np_find_duplicate_text_narrow(text_list1, text_list2, threshold=0.7)
        print(result)

    """
    async def find_duplicates():
        # Create and configure the SimilarityStore
        similarity_store = await nd.similarity_store.SimilarityStore.create(
            storage_level=StorageLevel.Document,
            similarity_threshold=threshold,
            tokenize="char_ngrams(3)"
        )

        # Index documents from text_list2
        for i, text in enumerate(text_list2):
            await similarity_store.insert(text, document_id=i)

        # Find duplicates
        ddict = {}
        for text1_id, text in enumerate(text_list1):
            result = await similarity_store.query(text, validate=True)
            ddict[text1_id] = [(doc.id_,
                                jaccard_similarity(doc.document.split(), text.split())) for doc in result]

        return ddict

    return asyncio.run(find_duplicates())


def np_find_duplicate_text_narrow_single(text_list, threshold=0.7):
    """
    Finds duplicate texts in a single list of texts using the narrow approach.

    Args:
        text_list (List[str]): The list of texts.
        threshold (float, optional): The similarity threshold for finding duplicates. Defaults to 0.7.

    Returns:
        Dict[int, List[int]]: A dictionary mapping each text ID in text_list to a list of text IDs of its duplicate texts.

    Example Usage:
        text_list = ["hello world", "foo bar", "lorem ipsum", "hello world", "foo baz"]

        result = np_find_duplicate_text_narrow_single(text_list, threshold=0.7)
        print(result)

    """
    async def find_duplicates():
        # Create and configure the SimilarityStore
        similarity_store = await nd.similarity_store.SimilarityStore.create(
            storage_level=StorageLevel.Document,
            similarity_threshold=threshold,
            tokenize="char_ngrams(3)"
        )

        # Index documents from text_list
        for i, text in enumerate(text_list):
            await similarity_store.insert(text, document_id=i)

        # Find duplicates
        duplicates = set()
        for text in text_list:
            result = await similarity_store.query(text, validate=True)
            if len(result) > 1:
                duplicates.add(tuple(sorted([doc.id_ for doc in result])))

        ddict = {}
        for d in duplicates:
            ddict[d[0]] = d[1:]

        return ddict

    return asyncio.run(find_duplicates())





##############################################################################
def pd_text_hash_create_lsh(df, col, sep=" ", threshold=0.7, num_perm=10, npool=1, chunk = 20000):
    '''
    For each of the entry create a hash function
    '''
    from datasketch import MinHash, MinHashLSH
    lsh = None

    if npool > 1 and len(df) > 20000 :
        from utilmy.parallel import multithread_run
        nchunk  = 1 + len(df) // chunk
        df_list = [  df.iloc[i*chunk:(i+1)*chunk, :] for i in range(0, nchunk ) ]

        # Create LSH
        lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)   #### Global lsh

        res = multithread_run(pd_text_hash_create_lsh, df_list, npool=1)

        hash_lines = []
        for xi in res :
            hash_lines.extend(xi[0])

        return hash_lines, lsh

    if len(df) < 1 :
        return [],[]

    if lsh is None :
       lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

    # Intialize list
    hash_lines = []
    ll         = df[col].values
    for index, sentence in enumerate(ll):

        # Get tokens of individual elements
        tokens = sentence.split(sep)

        # Create local hash funtion
        v = MinHash(num_perm=num_perm)

        for j in set(tokens):
            v.update(j.encode('utf8'))

        hash_lines.append(v)
        lsh.insert(str(index), v)
    return hash_lines, lsh


def pd_text_getcluster(df:pd.DataFrame, col:str='col', threshold=0.5, num_perm:int=5, npool=1, chunk = 100000):
    '''
    For each of the hash function find a cluster and assign unique id to the dataframe cluster_id
    '''
    # MAster cluster ids
    all_cluster_ids = []
    if len(df)< 1 : return df

    if npool > 1 and len(df) > 200000 :
        from utilmy.parallel import multithread_run
        nchunk  = 1 + len(df) // chunk
        df_list = [  df.iloc[i*chunk:(i+1)*chunk, :] for i in range(0, nchunk ) ]
        res     = multithread_run(pd_text_getcluster, df_list, npool=1)
        df      = pd.concat(res)
        return df

    # REturn from hash list
    hash_lines, lsh = pd_text_hash_create_lsh(
        df, col=col, threshold=threshold, num_perm=num_perm)

    # For each local hash find the cluster ids and assign to the dataframe and return dataframe
    cluster_count = 1
    for ind, i in enumerate(hash_lines):
        if ind in all_cluster_ids:
            continue

        x_duplicate     = lsh.query(i)
        x_duplicate_int = list(map(int, x_duplicate))
        # print(x_duplicate_int)
        df.at[x_duplicate_int, 'cluster_id'] = cluster_count
        cluster_count   += 1
        all_cluster_ids += x_duplicate_int

    return df


def pd_text_similarity(df: pd.DataFrame, cols=[], algo='') -> pd.DataFrame:
    '''
        Return similarities between two columns with 
        python's SequenceMatcher algorithm

        Args:
            df (pd.DataFrame): Pandas Dataframe.
            algo (String)    : rapidfuzz | editdistance 
            cols (list[str]) : List of of columns name (2 columns)

        Returns:
            pd.DataFrame

    '''
    if len(cols) != 2:
        raise Exception("Add two columns")
    for col in cols:
        if col not in df:
            raise Exception(f"Columns not found {col}")
            break

    from difflib import SequenceMatcher
    from rapidfuzz import fuzz
    import editdistance

    def find_similarity(col1, col2):
        if algo == "rapidfuzz":
            similarity_score = fuzz.ratio(col1, col2)
        elif algo == "editdistance":
            similarity_score = editdistance.eval(col1, col2)
        else:
            is_junk = None
            similarity_score = SequenceMatcher(is_junk, col1, col2).ratio()
        return similarity_score

    df['score'] = df.apply(lambda x: find_similarity( x[cols[0]], x[cols[1]]), axis=1)
    return df



#############################################################################
def jaccard_similarity(s1: Iterable, s2: Iterable):
    s1 = set(s1)
    s2 = set(s2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def nlp_generate_random_sentences(n_sentences=1, n_word_max=20):
    from faker import Faker
    fake  = Faker()
    import numpy as np
    return [fake.sentence(nb_words=np.random.randint(5, n_word_max)) for _ in range(n_sentences)]





###################################################################################################
if __name__ == "__main__":
    import fire ;
    fire.Fire()
