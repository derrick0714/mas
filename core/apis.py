from include.api import api
import pprint

class APIS(object):
	def print_athor_info(self,people):
		params = {}
		params['ResultObjects'] = "Author"
		params['AuthorQuery'] = people
		params['StartIdx'] = "1"
		params['EndIdx'] = "1"
		params['YearStart'] = "2005"

		result=  api.request(params)
		if(result == None or result['Result'] == None):
			print" Microsoft API maybe not working..."
		res = result['Result'][0];

		temp=""
		for p in res['ResearchInterestDomain']:
			temp += p['Name']+", "
		temp = temp[:len(temp)-3]	
		if( res['Affiliation'] == None):
			return
		Affiliation = res['Affiliation']['Name'].encode('utf-8').strip()

		line = "name: {0}; affiliation: {1}; g-index: {2}; h-index: {3}; research_domain: {4}\n"\
				.format(people, Affiliation ,res['GIndex'], res['HIndex'],temp, )

		print line

	def print_publications(self, peoples):
		num = 1
		print "Querying results(after 2005) from Microsoft API ...."
		peoples_new = peoples.split(',')
		co_author_publishtions = []
		for people in peoples_new:
			id = self.getuthor_id(people)
			publishtions = self.get_publitions_by_id(id)
			if( publishtions != None):
				print "[{3}] author: {0} id: {1}, publishtions: {2}".format(people, id, len(publishtions),num)
			num = num +1
			if( len(co_author_publishtions) == 0 ):
				for i in publishtions:
					co_author_publishtions.append(i)
			else:
				temp_list = []
				for i in co_author_publishtions:
					for j in publishtions:
						if( j == i ):
							temp_list.append(i)
							break
				co_author_publishtions = temp_list
		print "{0} : {1} co-authors since 2005".format( peoples, len(co_author_publishtions))



	def getuthor_id(self, people):

		params = {}
		params['ResultObjects'] = "Author"
		params['AuthorQuery'] = people
		params['StartIdx'] = "1"
		params['EndIdx'] = "1"
		params['OrderBy'] = "rank"
		#pprint.pprint(params)
		result=  api.request(params)
		if(result == None or result['Result'] == None):
			print" Microsoft API maybe not working..."
		res = result['Result'][0];
		#pprint.pprint(res)
		return res['ID']

	def get_publitions_by_id(self, id):

		StartIdx = 1
		publishtions = []
		while (True):
			params = {}
			params['ResultObjects'] = "Publication"
			params['AuthorID'] = id
			params['StartIdx'] = StartIdx
			params['EndIdx'] = StartIdx + 50
			params['YearStart'] = "2005"
			params['OrderBy'] = "Year"

			
			result=  api.request(params)
			if(result == None or result['Result'] == None):
				print" Microsoft API maybe not working..."
				return None;

			res = result['Result']
			for one_publishtion in res:
				#print one_publishtion['ID']
				publishtions.append(one_publishtion['ID'])

			if( result['TotalItem'] > StartIdx + 50):
				StartIdx = StartIdx + 50
			else:
				return publishtions
		 
