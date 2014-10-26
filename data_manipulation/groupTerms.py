import json
from collections import defaultdict

'''
    usage:
        from groupTerms import groupTerms
        json_str = groupTerms("sample_data/up.json", "sample_data/down.json")
'''

class groupTerms(object):
	def __init__(self, g1, g2):
		self.confidenct = 0.9
		self.db_list = ["Wiki", "Disease", "GO-CC", "GO-BP", "GO-MF"]
		self.g1_json = {}
		self.g2_json = {}
		with open(g1, 'r') as f:
			self.g1_json = json.load(f)
		with open(g2, 'r') as f:
			self.g2_json = json.load(f)
		self.cal_group()

	def cal_group(self):
		final_output = {}
		final_output["group1"] = {}
		final_output["group2"] = {}
		final_output["common"] = {}
		for db in self.db_list:
			stat = {}
			for term in self.g1_json[db]:
				if term not in stat:
					stat[term] = {}
					stat[term]['1'] = 0
					stat[term]['2'] = 0
				stat[term]['1'] = self.g1_json[db][term]
			for term in self.g2_json[db]:
				if term not in stat:
					stat[term] = {}
					stat[term]['1'] = 0
					stat[term]['2'] = 0
				stat[term]['2'] = self.g2_json[db][term]

			group1 = {}
			group2 = {}
			common = {}
			for term in stat:
				if stat[term]['1'] * 1.0 / (stat[term]['1'] + stat[term]['2']) >= self.confidenct:
					group1[term] = stat[term]['1']
				elif stat[term]['2'] * 1.0 / (stat[term]['1'] + stat[term]['2']) >= self.confidenct:
					group2[term] = stat[term]['2']
				else:
					common[term] = (stat[term]['1'] + stat[term]['2']) / 2

			final_output["group1"][db] = group1
			final_output["group2"][db] = group2
			final_output["common"][db] = common

			# print "\n\n", db
			# print len(group1), len(group2), len(common)
			# print "group1:\n", group1
			# print "\ngroup2:\n", group2
			# print "\ncommon:\n", common
		# for key in final_output:
		# 	print key, len(final_output[key])
		# with open('try.txt', 'w') as f:
		# 	f.write(json.dumps(final_output))
		return json.dumps(final_output)

	

def main():
	groupTerms("sample_data/up.json", "sample_data/down.json")

if __name__ == '__main__':
	main()