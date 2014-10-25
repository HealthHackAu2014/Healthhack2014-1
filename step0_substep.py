__author__ = 'quek'



vaUp = 'vaUp.tsv'
vaDown ='vaDown.tsv'

from collections import defaultdict

def selectThree(filename):
    return_dict = defaultdict(list)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            fields = line.split('\t')
            if len(return_dict[fields[0]]) > 1:
                pass
            else:
                print "%s\t%s" % (fields[0], fields[1])
                return_dict[fields[0]].append(fields[1])


selectThree(vaUp)











