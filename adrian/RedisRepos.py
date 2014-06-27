# %load_ext autoreload
# %autoreload 2

import redis
import bitarray as ba
import numpy as np 

class Repos(object):
   
    """ The Repos class provides methods for working with
    large collections of github repository names in Redis. In storing 
    10M or so names, it uses bitarrays to deal with intersections,
    unions, etc. The methods in the class translate between repo names
    and the bitarrays."""

    #hash buckets size
    bucket_size = 1000
    # dictionary of repo names and ids
    repo_id = None
    # dictionary of ids and repo names
    id_repo = None
    # connection to redis
    red = None
    # the redis pipe for batch operations
    pipe = None

    def __init__(self, testing = False, load_repos = False):
        if testing:
            # for testing purposes, use different database
            self.red = redis.Redis(db='3')
        else:
            self.red = redis.Redis(db='1')
        self.pipe = self.red.pipeline()
        # load repo lists
        if load_repos:
            print 'loading repo lists  -- this might take a while'
            rs = self.load_repo_id()
            self.repo_id = rs['repo_id']
            self.id_repo = rs['id_repo']

    def load_repo_id_dictionaries(self):
        """load the dictionaries of repos and ids
        from Redis; this is slow because there are 10 million or so
        @return: a dictionary with id_repo and repo_id dictionaries in item_number"""
        repo_count = self.red.zcard('repo:id')
        repo_id = {r:i for r,i in zip(red.zrangebyscore('repo:id', 0, repo_count), xrange(0, repo_count))}
        id_repo = {v:k for k,v in repo_id.items()}
        return {'repo_id':repo_id, 'id_repo':id_repo}

    def construct_id_repo_hashset(self, repo_id):
        # construct ids-repo sets for all github repos
        # make buckets of 1000 ids in hashsets to speed retrieval
        
        bucket_count = len(self.repo_id)/self.bucket_size
        for current_bucket in range(0, bucket_count):
            start_index = current_bucket*bucket_size
            repo_id_dict = {id:repo for id, repo in zip(range(start_index,start_index+bucket_size), repo_id[start_index:start_index+bucket_size])}
            key = 'id:repo:{}'.format(current_bucket)
            self.pipe.hmset(key, repo_id_dict).execute()
            print 'adding bucket {} with name {}'.format(current_bucket, key)

    def get_repo_by_id(self, id):
        """ retrieve repo name for id"""
        # # find which bucket it is in
        # bucket_number = id/self.bucket_size
        # # find where in the bucket it is
        # item_number = id % self.bucket_size
        # # construct key name for hashset
        # key = 'id:repo:{}'.format(bucket_number)
        # # print key, id
        # return self.red.hget(key, id)
        return self.red.zrange('repo:id', id, id)[0]

    def get_repos_by_ids(self, ids):
        """ retrieve list of repos names for ids """
        return [self.get_repo_by_id(i) for i in ids]

    def test_id_repo_hashset(self, start, end, repo_id_list):
        """ simple test to see if hashbuckets work ok"""
        ids = [self.get_repo_by_id(i) for i in range(start, end)]
        ids_ac  = repo_id_list[start:end]
        if ids == ids_ac:
            print 'hash results are the same as repo list'
        return {'hash_result': ids, 'repo_ids': ids_ac}

    def construct_repo_id_set(self):
        """ Constructs  a sorted set in redis of all repo names with ids as the score
        This should only be done once. """    
        #load set of all repo names
        repos = list(self.red.smembers('repos:list'))
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

    def convert_set_to_bits(self,  set_to_convert, repo_id_dict, delete_existing = False):
        """ Converts an existing redis set to a bits
        This is only needed for migration from string based sets 
        to bitarray-based sets"""
        if self.red.exists(set_to_convert) is False:
            return 'Repo collection \'{}\' does not exist'.format(set_to_convert)
        print 'converting {} ... '.format(set_to_convert)
        current_set = self.red.smembers(set_to_convert)
        current_ids = [repo_id_dict[n] for n in current_set if repo_id_dict.has_key(n)]
        new_name = store_repos(set_to_convert, current_ids)
        if delete_existing:
            self.red.delete(set_to_convert)
        return new_name

    def  store_repos(self, repo_collection, ids):
        """store a set of bits as a named repo collection""" 
        repo_count = self.red.zcard('repo:id')
        bits = np.zeros(repo_count)
        bits[ids]=1
        new_name = 'repos:' + repo_collection
        self.red.set(new_name, ba.bitarray(bits.tolist()).tobytes())
        return new_name

    def  load_repo_collection_bits(self, name):
        ## retrieve a collection of repos as a bitarray
        b2 = ba.bitarray()
        b2.frombytes(self.red.get(name))
        return b2

    def bits_to_reponames(self, bits):
        # convert bitarray to repo names
        bits_array = np.array(bits.tolist(), 'bool')
        indexes = list(np.nonzero(bits_array)[0])
        if self.id_repo is None:
            # load the repo names from Redis
            print 'using redis to get repo names'
            repos = self.get_repos_by_ids(indexes)
        else:
            repos = [self.id_repo[id] for id in indexes]
        return repos

    def load_repo_collection(self, name):
        """ load named collection of repos as  a list of strings"""
        bits = self.load_repo_collection_bits(name)
        return self.bits_to_reponames(bits)
    
     