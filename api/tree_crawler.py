def crawl(tree, target):
    '''Generator to recursively crawl through tree and pick up IDs (for
    question/treatments as a target. Set target='q' or target='t'''

    if target != 'q' and target != 't':
        raise ValueError('target must be q (question) or t (treatment)')

    if tree['next'] == target:
        yield tree['id']

    if 'act' in tree.keys():
        for branch in tree['act']:
            # this would be 'yield from' in python3.3. i long for python3.3
            for x in crawl(branch, target):
                yield x
