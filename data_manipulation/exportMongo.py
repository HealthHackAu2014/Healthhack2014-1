from Ontologies import Ontologies
import json
import pprint


pp = pprint.PrettyPrinter(indent=2)

setting_file = 'onto_setting'

ontos = Ontologies()
res = ontos.onto


for db, entries in res.iteritems():
    fh_out = open('onto_json/%s' % db, 'w+')
    for key, value in entries.iteritems():
        out = { key : value }
        json_out =json.dumps(out)
        fh_out.write("%s\n" % json_out)
    fh_out.close()
# if invalid search happend, the return result will be an empty dict
# so you can get value from res in this way
##name = res['name'] if 'name' in res else ''
##def = res['def'] if 'def' in res else ''
