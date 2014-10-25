import json

'''
    usage:
      from Ontologies import Ontologies
      ontos = Ontologies
      res = ontos.search('dbname','id')
      # if invalid search happend, the return result will be an empty dict
      # so you can get value from res in this way
      name = res['name'] if 'name' in res else ''
      def = res['def'] if 'def' in res else ''
'''

#setting file is in json format
setting_file = 'onto_setting'

class Ontologies(object):
    def __init__(self):
    	# initialisation
        self.onto = {}
        with open(setting_file, 'r') as f:
            self.onto_json = json.loads(f.read())
        self.load_onto()

    def load_onto(self):
    	# load multiple dbs
        for one_onto in self.onto_json["ontos"]:
            self.onto[one_onto["name"]] = {}
            with open(one_onto['file'], 'r') as f:
                content = f.read()
                content = unicode(content, 'utf-8')
                blocks = content.split(self.onto_json['block_delimiter'])
                for i in range(1, len(blocks)):
                    lines =  blocks[i].split('\n')
                    key = ''
                    tmp_map = {}
                    for line in lines:
                        try:
                            parts = line.split(':', 1)
                        except:
                            continue
                        if len(parts) != 2:
                            continue
                        if parts[0].strip() == self.onto_json['key']:
                            key = parts[1].strip()
                        if parts[0].strip() == self.onto_json['name']:
                            tmp_map[self.onto_json['name']] = parts[1].strip()
                        if parts[0].strip() == self.onto_json['def']:
                            tmp_map[self.onto_json['def']] = parts[1].strip()
                        if parts[0].strip() == self.onto_json['parent']:
                            parent_parts = parts[1].split('!')
                            if len(parent_parts) != 2:
                                continue
                            parent_id = parent_parts[0].strip()
                            parent_name = parent_parts[1].strip()
                            if self.onto_json['parent'] not in tmp_map:
                                tmp_map[self.onto_json['parent']] = []
                            tmp_parent = {}
                            tmp_parent['id'] = parent_id
                            tmp_parent['name'] = parent_name
                            tmp_map[self.onto_json['parent']].append(tmp_parent)

                    if key != '':
                        self.onto[one_onto["name"]][key] = tmp_map

    def search(self, db, key):
    	# search from db with key words
    	if db in self.onto:
    		print 'yes'
    		if key in self.onto[db]:
    			return self.onto[db][key]
    	return {}

def main():
	# main part is for ad hoc test purpose only
    ontos = Ontologies()
    print ontos.search('go', 'GO:0000022')

if __name__ == '__main__':
    main()