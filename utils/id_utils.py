import hashids

def hashid(_id, length=6):
    '''
        用户/题目ID哈希算法
    '''
    KEY = 'yuhi.xyz'
    hasher = hashids.Hashids(salt=KEY, min_length=length)
    return hasher.encode(_id) # 返回哈希结果