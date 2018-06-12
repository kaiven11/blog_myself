
#coding=utf-8

# comment_list=[{'artical_id': 1, 'parent_id': None, 'id': 1, 'user_id': 1, 'content': 'sdfadfadsf',},
#               {'artical_id': 1, 'parent_id': 1, 'id': 2, 'user_id': 1, 'content': '<p>你说谁呢</p>',},
#               {'artical_id': 1, 'parent_id': 2, 'id': 3, 'user_id': 1, 'content': '<p>说你呢</p>', },
#               {'artical_id': 1, 'parent_id': None, 'id': 4, 'user_id': 1, 'content': '<p>我就是来开玩笑的！！</p>'},
#               {'artical_id': 1, 'parent_id': None, 'id': 5, 'user_id': 1, 'content': '<p>发蒂法蒂法蒂法蒂法蒂法蒂法蒂法</p>'}]

def gender_comment(comm_list):
    '''
    gender the comment list like below,you can use to show on the front page.
    [{'user_id': 1, 'content': 'sdfadfadsf', 'artical_id': 1, 'id': 1, 'parent_id': None, 'include': {'user_id': 1, 'content': '<p>你说谁呢</p>', 'artical_id': 1, 'id': 2, 'parent_id': 1, 'include': {'user_id': 1, 'content': '<p>说你呢</p>', 'artical_id': 1, 'id': 3, 'parent_id': 2, 'include': []}}}]
    :param comm_list:
    :return: {commentid:comment}
    '''
    #gender root comment
    gen_comment=[]
    for i in comm_list:
        if not i.get('parent_id'):
            gen_comment.append(i)

    # add the "include" for parent comment
    new_dict={}
    for i in comm_list:
        i.update({'include':[]})
        new_dict.update({i.get('id'):i})
    #gender the end result
    for k,v in new_dict.items():
        parent_id=v.get('parent_id')
        if parent_id:
            new_dict[parent_id]['include'].append(v)
    print(gen_comment,__file__)

    return gen_comment

if __name__ == '__main__':
    result=gender_comment(comm_list=[])
    print(result)


