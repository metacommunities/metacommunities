# code to simplifiy and compact everything in redis
# %load_ext autoreload
# %autoreload 2


import redis
import bitarray as ba
import numpy as np 


#hash buckets by size
bucket_size = 1000

def construct_id_repo_hashset(repo_id):
    # construct ids-repo sets for all github repos
    # make buckets of 1000 ids to speed retrieval
    
    bucket_count = len(repo_id)/bucket_size
    for current_bucket in range(0, bucket_count):
        start_index = current_bucket*bucket_size
        repo_id_dict = {id:repo for id, repo in zip(range(start_index,start_index+bucket_size), repo_id[start_index:start_index+bucket_size])}
        key = 'id:repo:{}'.format(current_bucket)
        pipe.hmset(key, repo_id_dict).execute()
        print 'adding bucket {} with name {}'.format(current_bucket, key)

def get_repo_by_id(id):
    """ retrieve repo name for id"""
    bucket_number = id/bucket_size
    item_number = id % bucket_size
    key = 'id:repo:{}'.format(bucket_number)
    # print key, id
    return red.hget(key, id)

def get_repos_by_ids(ids):
    """ retrieve list of repos names for ids """
    return [get_repo_by_id(i) for i in ids]

def test_id_repo_hashset(start, end, repo_id):
    """ simple test to see if hashbuckets work ok"""
    ids = [get_repo_by_id(i) for i in range(start, end)]
    ids_ac  = repo_id[start:end]
    if ids == ids_ac:
        print 'hash results are the same as repo list'
    return {'hash_result': ids, 'repo_ids': ids_ac}


def construct_repo_id_set():
    """ Constructs  a sorted set in redis of all repo names with ids as the score
    This should only be done once. """    
    #load set of all repo names
    repos = list(red.smembers('repos:list'))
    #construct simple ids based on index
    ids =range(0, len(repos)) 
    bucket_size = 100000
    bucket_count = len(id)/bucket_size
    # add repo names and ids as scores to  a sorted set by buckets
    for b in range(0, len(ids), bucket_size):
    	repo_id = {r:i for i,r in zip(ids[b:b+bucket_size], repos[b:b+bucket_size])}
    	print 'adding bucket {}'.format(b)
    	print repo_id.popitem(), b
    	pipe.zadd('repo:id', **repo_id)
    	pipe.execute()

## to get a long list of ids for given a set of repo names
# too slow on redis itslef
#a list based version takes ages; better to load all the repos into a dictionary with ids and then 
# e.g. large_names = map(lambda x: red.zrank('repo:id', x), repos[:400000])	


#do lookups against this dictionary
# images = red.smembers('images')
# image_ids = [repo_id[n] for n in images if repo_id.has_key(n)]
# tests = red.smembers('tests')
# tests_ids = [repo_id[n] for n in tests if repo_id.has_key(n)]

def convert_set_to_bits(set_to_convert, repo_id_dict, delete_existing = False):
    """ Converts an existing redis set to a bits"""
    if red.exists(set_to_convert) is False:
        return 'Repo collection \'{}\' does not exist'.format(set_to_convert)
    print 'converting {} ... '.format(set_to_convert)
    current_set = red.smembers(set_to_convert)
    current_ids = [repo_id_dict[n] for n in current_set if repo_id_dict.has_key(n)]
    new_name = store_repos(set_to_convert, current_ids)
    if delete_existing:
        red.delete(set_to_convert)
    return new_name

def  store_repos(repo_collection, ids):
    """store a set of bits as a named repo collection""" 
    bits = np.zeros(repo_count)
    bits[ids]=1
    new_name = 'repos:' + repo_collection
    red.set(new_name, ba.bitarray(bits.tolist()).tobytes())
    return new_name

def  load_repo_collection(name):
    ## retrieve a collection of repos as a bitarray
    b2 = ba.bitarray()
    b2.frombytes(red.get(name))
    return b2

def bits_to_reponames(bits):
    # convert bitarray to repo names
    bits_array = np.array(bits.tolist(), 'bool')
    indexes = list(np.nonzero(bits_array)[0])
    repos = [id_repo[id] for id in indexes]
    return repos

#load the dictionaries of repos and ids
def load_repo_id():
    repo_count = red.zcard('repo:id')
    repo_id = {r:i for r,i in zip(red.zrangebyscore('repo:id', 0, repo_count), xrange(0, repo_count))}
    id_repo = {v:k for k,v in repo_id.items()}
    return {'repo_id':repo_id, 'id_repo':id_repo}

testing = False
if testing:
    # for testing purposes, use different database
    red = redis.Redis(db='3')
else:
    red = redis.Redis(db='1')
pipe = red.pipeline()

# load repo lists
print 'loading repo lists  -- this might take a while'
rs = load_repo_id()
repo_id = rs['repo_id']
id_repo = rs['id_repo']
 