# -*- coding: utf-8 -*-
"""
ENV variables

   export torch_device='cpu'



### How to run
    sudo docker run -d -p 6333:6333     -v ~/.watchtower/qdrant_storage:/qdrant/storage:z     qdrant/qdrant


### How to run qdrant from binary file

    # download latest tar.gz package file from here, Linux: 
        wget -c https://github.com/qdrant/qdrant/releases/download/v1.9.0/qdrant-x86_64-unknown-linux-gnu.tar.gz

    # extract tar.gz package
        tar -xvf qdrant-x86_64-unknown-linux-gnu.tar.gz

    # run qdrant on separate shell.
        cd download_folder
        ./qdrant --config-path /absolute/path/to/config.yaml &

        # Config Where to store all  data
           storage_path: ./ztmp/qdrant/storage

        ---> In same docker : easy


### Benchmarks:
    alias py2="python engine.py "

    py2 bench_v1_create_indexes --dirdata_root ztmp/bench/
    py2 bench_v1_run  --dirout ztmp/bench/   --topk 5


    ### Bench
       tantivy : v1  6ms
       Sparse :      23ms
       Dense:        30 ms




### Benchmark accuracy:
   Sames 1000 query for all 3.
     --> Accuracy.
     --> Compare  errors.

     join  dataframe on id


     ### csv metrics
       df1 = df1.merge(df2, on='id', how='left', suffixes=('', '_2'))

       df[ df.is_topk == 0 ] --> Find errors.


### Binary mode for qdrant
https://github.com/qdrant/qdrant/releases


"""
import os, time, glob

from box import Box  ## use dot notation as pseudo class

import pandas as pd, numpy as np

from qdrant_client import QdrantClient

# from fastembed import TextEmbedding

from utilmy import pd_read_file, pd_to_file, date_now, glob_glob, json_save
from utilmy import log
from utils import pd_append

from rag.engine import (EmbeddingModel, qdrant_dense_create_index,
                        qdrant_dense_search,
                        dataset_hf_to_parquet, dataset_agnews_schema_v1,
                        qdrant_sparse_create_index, qdrant_sparse_search, qdrant_dense_create_collection,
                        qdrant_sparse_create_collection, qdrant_collection_exists,
                        tantivy_index_documents, EmbeddingModelSparse, tantivy_search
                        )


##########################################################################################
def create_error_report(dirin="ztmp/bench", dataset="ag_news", dirquery=None):
    """Merging  query dataframe with  results from each benchmark.

    python bench.py create_error_report --dirin "ztmp/bench/"

    Args:
        dirin (str, optional):  path path where  benchmark results are stored. Defaults to "ztmp/bench".

    """
    dirmetric = f"{dirin}/{dataset}/metrics"


    log("###### pick latest file from each benchmark directory")
    search_types = ("sparse", "dense", "tantivy")
    bench_dirs = [f"{dirin}/{dataset}/{dirk}" for dirk in search_types]
    flist = [glob_glob_last_modified(f"{bench_dir}/*/*.csv") for bench_dir in bench_dirs]
    flist = [filepath for filepath in flist if filepath is not None]


    log("###### Merge query df with results from each benchmark")
    dirquery = f"{dirin}/{dataset}/query/df_search_test.parquet" if dirquery is None else dirquery
    dfall = pd_read_file(dirquery)
    dfall = dfall[["id", "query"]]

    for i, filepath in enumerate(flist):
        df2 = pd_read_file(filepath)
        dfall = dfall.merge(df2, on="id", how="left", suffixes=("", f"_{search_types[i]}"))
    dfall.rename(columns={"istop_k": "istop_k_sparse"}, inplace=True)

    pd_to_file(dfall, f"{dirmetric}/df_err_all.csv", show=1)

    log("##### Select mismatch rows between engine")
    dfdiff = dfall[(dfall.istop_k_sparse != 1) | (dfall.istop_k_dense != 1) | (dfall.istop_k_tantivy != 1)]
    dfdiff = dfdiff[["id", "query", "istop_k_sparse", "istop_k_dense", "istop_k_tantivy"]]
    pd_to_file(dfdiff, f"{dirmetric}/df_err_mismatch.csv", show=1)

    log("##### Calc metrics")
    n = len(dfall)
    dmetrics = {"acc_dense": dfall["istop_k_dense"].sum() / n,  ## 91%
                "acc_sparse": dfall["istop_k_sparse"].sum() / n,  ## 99.9%
                "acc_tantivy": dfall["istop_k_tantivy"].sum() / n,
                }
    log(dmetrics)
    json_save(dmetrics, f"{dirmetric}/metrics.json")


##########################################################################################
####### data converter ###################################################################
def bench_v1_data_convert(dirin=None, dirdata_root=None, dataset=None, dirout=None):

    dirdata_norm = f"{dirdata_root}/norm/{dataset}"

    norm_files = glob_glob(f"{dirdata_norm}/*/*.parquet")
    if len(norm_files) > 0: 
        return None 

    if dirin is None:
        dataset_hf_to_parquet(dataset, dirout=dirdata_root, splits=["train", "test"])

    if dataset == "agnews":
        # normalize
        dataset_agnews_schema_v1(dirin=f"{dirdata_root}/{dataset}/*.parquet", dirout=dirdata_norm)


def query_load_or_create(dirin=None, dirdata=None, nfile=1, nquery=1000):
    """Load or create a query dataset based on  input directories and parameters.
    args :
        dirin (str):  input path to load or create  query dataset.
        dirdata (str):  data path used to create  query dataset.
        nfile (int): Number of files to read when creating  dataset. Default is 1.
        nquery (int): Number of queries to sample from  dataset. Default is 1000.

    Returns:
        DataFrame:  loaded or created query dataset.
    """

    if not os.path.exists(dirin):
        df = pd_read_file(f"{dirdata}/*/df*.parquet", nfile=nfile)  ##  Real Dataset

        # pick thousand random rows
        df_query = df.sample(nquery)
        df_query["query"] = df_query["body"].apply(lambda x: np_random_subset(x, 20))
        pd_to_file(df_query, f"{dirin}")

    else:
        df_query = pd_read_file(dirin)

    return df_query


##########################################################################################
####### Dense Vector  ####################################################################
def bench_v1_dense_run(cfg=None, dirout="ztmp/bench/", topk=5, dataset="ag_news", dirdata="ztmp/bench/norm/",
                       dirquery:str=None):
    """Measure performance in Real and bigger dataset.

    python engine.py bench_v1_run  --dirout ztmp/bench/   --topk 5


    """
    cc = Box({})
    cc.name = "bench_v1_dense_run"

    cc.server_url      = "http://localhost:6333"
    cc.collection_name = f"hf-{dataset}-dense"
    cc.model_type = "stransformers"
    cc.model_id   = "sentence-transformers/all-MiniLM-L6-v2"  ### 384,  50 Mb
    cc.topk       = topk

    cc.dataset  = dataset
    cc.dirquery = f"{dirout}/{dataset}/query/df_search_test.parquet" if dirquery is None else dirquery
    cc.dirdata2 = f"{dirdata}/{dataset}/"

    df_query = query_load_or_create(dirin=cc.dirquery, dirdata=cc.dirdata2)
    model    = EmbeddingModel(cc.model_id, cc.model_type)
    client   = QdrantClient(cc.server_url)

    dfmetrics = pd.DataFrame(columns=["id", "istop_k", "dt"])
    for i, row in df_query.iterrows():
        id1 = row["id"]
        query = row["query"]
        t0 = time.time()
        results = qdrant_dense_search(query, collection_name=cc.collection_name,
                                      model=model, topk=topk, client=client)
        dt = time.time() - t0
        topk_ids = [scored_point.id for scored_point in results[:topk]]

        ####  Add metrics
        istop_k = 1 if id1 in topk_ids else 0
        dfmetrics= pd_append(dfmetrics, [id1, istop_k, dt])

    metrics_export(dfmetrics, dataset, dirout,cc, engine="dense")


def bench_v1_create_dense_indexes(dirdata_root="ztmp/bench", dataset = "ag_news"):
    """Create indexes for benchmarking
    python engine.py bench_v1_create_indexes --dirout ztmp/bench/
    """
    # download dataset from Hugging Face in dirout
    # save normalized dataset in dirout/norm
    model_type = "stransformers"
    model_id = "sentence-transformers/all-MiniLM-L6-v2"  ### 384,  50 Mb
    server_url = "http://localhost:6333"

    dirdata_norm = f"{dirdata_root}/norm/{dataset}"
    # print(filelist)
    collection_name = f"hf-{dataset}-dense"
    qclient = QdrantClient(server_url)
    if qdrant_collection_exists(qclient, collection_name):
        log(f"collection {collection_name} already exists")
        return

    # if dirdata_norm not empty skip
    bench_v1_data_convert(dirdata_root=dirdata_root, dataset=dataset)


    model = EmbeddingModel(model_id, model_type)
    qdrant_dense_create_collection(qclient, collection_name=collection_name,
                                   size=model.model_size)
    qdrant_dense_create_index(
        dirin=f"{dirdata_norm}/*/*.parquet",
        collection_name=collection_name,
        coltext="body",
        colscat=["title", "body", "cat1"],
        model_id="sentence-transformers/all-MiniLM-L6-v2",
        model_type="stransformers",
        batch_size=100,
        client=qclient
    )



##########################################################################################
####### Tantivy Index  ###################################################################
def bench_v1_create_tantivy_indexes(dirdata_root="ztmp/bench",     dataset = "ag_news"):
    """Create indexes for benchmarking
    python engine.py bench_v1_create_tantivy_indexes --dirout ztmp/bench/
    """
    # download dataset from Hugging Face in dirout
    # save normalized dataset in dirout/norm

    dirdata_norm = f"{dirdata_root}/norm/{dataset}"
    # print(filelist)
    index_path = f"{dirdata_root}/tantivy_index/hf-{dataset}"
    if os.path.exists(index_path):
        return

    # if dirdata_norm not empty skip
    bench_v1_data_convert(dirdata_root=dirdata_root, dataset=dataset)    

    colsused = ["title", "body", "cat1"]
    tantivy_index_documents(
        dirin=f"{dirdata_norm}/*/*.parquet", datapath=index_path, colsused=colsused
    )


def bench_v1_tantivy_run(cfg=None, dirout="ztmp/bench", topk=5, dataset="ag_news", dirdata="ztmp/bench/norm/",
                         dirquery=None):
    """Measure performance in Real and bigger dataset.

    python engine.py bench_v1_tantivy_run  --dirout ztmp/bench/   --topk 5

    """
    cc = Box({})
    cc.name = "bench_v1_tantivy_run"
    cc.dirquery = f"{dirout}/{dataset}/query/df_search_test.parquet" if dirquery is None else dirquery

    cc.dirdata2 = f"{dirdata}/{dataset}/"
    cc.datapath = f"{dirout}/tantivy_index/hf-{dataset}"
    df_query = query_load_or_create(dirin=cc.dirquery, dirdata=cc.dirdata2)

    dfmetrics = pd.DataFrame(columns=["id", "istop_k", "dt"])
    # log(df_query.title)
    for i, row in df_query.iterrows():
        # print(row)
        id1 = row["id"]
        title = row["title"]
        query = row["query"]

        # clean query to avoid query language errors
        # replace non alphanumeric characters with space
        query = str_to_alphanum_only(query)
        t0 = time.time()
        results = tantivy_search(datapath=cc.datapath, query=query, topk=topk)
        dt = time.time() - t0

        # tantivy returning id as float, hence using title instead
        topk_titles = [doc["title"][0] for score, doc in results]
        # log(topk_titles)
        #### Accuracy.abs
        istop_k = 1 if title in topk_titles else 0
        dfmetrics= pd_append(dfmetrics, [id1, istop_k, dt])

    metrics_export(dfmetrics, dataset, dirout,cc, engine="tantivy")





##########################################################################################
####### Sparse Index  ####################################################################
def bench_v1_create_sparse_indexes(dirdata_root="ztmp/bench", dataset = "ag_news"):
    
    model_id = "naver/efficient-splade-VI-BT-large-doc"  # 268 MB
    dirdata_norm = f"{dirdata_root}/norm/{dataset}"
    server_url = "http://localhost:6333"

    # print(filelist)
    collection_name = f"hf-{dataset}-sparse"
    qclient = QdrantClient(server_url)
    if qdrant_collection_exists(qclient, collection_name):
        log(f"collection {collection_name} already exists")
        return

    # if dirdata_norm not empty skip
    bench_v1_data_convert(dirdata_root=dirdata_root, dataset=dataset)   

    qdrant_sparse_create_collection(qclient=qclient, collection_name=collection_name)
    qdrant_sparse_create_index(
        dirin=f"{dirdata_norm}/*/*.parquet",
        collection_name=collection_name,
        coltext="body",
        colscat=["title", "body", "cat1"],
        model_id=model_id,
        batch_size=10,
        client=qclient
    )


def bench_v1_sparse_run(cfg=None, dirout="ztmp/bench", topk=5, dataset="ag_news",
                        dirdata="ztmp/bench/norm/", dirquery: str =None):
    """Measure performance in Real and bigger dataset.

    python engine.py bench_v1_sparse_run  --dirout ztmp/bench/   --topk 5


    """
    cc = Box({})
    cc.name = "bench_v1_sparse_run"

    cc.server_url = "http://localhost:6333"
    cc.collection_name = f"hf-{dataset}-sparse"
    cc.model_type = "stransformers"
    cc.model_id = "naver/efficient-splade-VI-BT-large-query"  ### 17 Mb
    cc.topk = topk

    cc.dataset = dataset
    cc.dirquery = f"{dirout}/{dataset}/query/df_search_test.parquet" if dirquery is None else dirquery 
    cc.dirdata2 = f"{dirdata}/{dataset}/"

    df_query = query_load_or_create(dirin=cc.dirquery, dirdata=cc.dirdata2)
    model = EmbeddingModelSparse(cc.model_id)
    client = QdrantClient(cc.server_url)
    dfmetrics = pd.DataFrame(columns=["id", "istop_k", "dt"])

    for i, row in df_query.iterrows():
        # print(row)
        id1 = row["id"]
        query = row["query"]

        t0 = time.time()
        results = qdrant_sparse_search(
            query, collection_name=cc.collection_name, model=model, topk=topk, client=client
        )
        dt = time.time() - t0
        topk_ids = [scored_point.id for scored_point in results[:topk]]

        #### Accuracy.abs
        istop_k = 1 if id1 in topk_ids else 0
        dfmetrics= pd_append(dfmetrics, [id1, istop_k, dt])

    metrics_export(dfmetrics, dataset, dirout,cc, engine="sparse")




##########################################################################################
####### Utils   ##########################################################################
# def zzz_pd_append(df:pd.DataFrame, rowlist:list)-> pd.DataFrame:
#   df2 = pd.DataFrame(rowlist, columns= list(df.columns))
#   df  = pd.concat([df, df2], ignore_index=True)
#   return df

def metrics_export(dfmetrics, dataset, dirout,cc, engine="sparse"):
    """Export metrics to a specified directory after processing them and saving to a file.
    Parameters:
        dfmetrics (DataFrame):  metrics data to be exported.
        dataset (str):  dataset name.
        dirout (str):  output directory path.
        cc (object): Additional configuration object.
    """
    tunix = date_now(fmt="%Y%m%d_%H%M_%S", returnval="str")
    cc.dirout2 = f"{dirout}/{dataset}/{engine}/{tunix}/"
    log(cc)
    # dfmetrics = pd.DataFrame(metrics, columns=["id", "istop_k", "dt"])
    pd_to_file(dfmetrics, f"{cc.dirout2}/dfmetrics.csv", show=1)
    log(" Avg time per request", dfmetrics["dt"].mean())
    log(" Percentage accuracy", dfmetrics["istop_k"].mean() * 100)
    json_save(cc, f"{cc.dirout2}/config.json")



def str_to_alphanum_only(txt):
     return "".join([c if c.isalnum() else " " for c in txt])


def np_random_subset(txt: str, w_count=20):
    """Generate a random subset of words from a given text.
    Args:
        txt (str):  input text.
        w_count (int, optional):  number of words to include in  subset. Defaults to 20.

    Returns:
        str: A string containing  randomly selected subset of words.
    """
    words = txt.split()
    start = np.random.randint(0, len(words) - w_count) if len(words) > w_count else 0
    return " ".join(words[start: start + w_count])


def glob_glob_last_modified(dirpath):
    # print(dirpath)
    files = sorted(glob.glob(dirpath), key=os.path.getctime, reverse=True)
    if len(files) > 0:
        return files[0]  # Latest file


###################################################################################################
if __name__ == "__main__":
    import fire

    # pd.options.mode.chained_assignment = None
    fire.Fire()

######################
'''
def zzz_query_clean_list(query: str, sep="@@"):
    """
    hacky way to clean queries. Ideally should be separated by separator only.
    """
    query = query.replace("\n", "")
    query_list = query.split("?")

    # remove sep
    query_list = [q.replace(sep, "") for q in query_list]

    # remove numbered prefix via regex
    query_list = [re.sub(r"^[0-9]*\.", "", q) for q in query_list]
    query_list = [q.strip() for q in query_list]
    query_list = [q for q in query_list if len(q) > 0]
    return query_list
'''
