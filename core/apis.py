from include.api import api

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
		params = {}
		params['ResultObjects'] = "Publication"
		params['PublicationContent'] = "Title,Author,Abstract,FullVersionURL"
		params['AuthorQuery'] = peoples
		params['StartIdx'] = 1
		params['EndIdx'] = 5
		params['YearStart'] = "2005"
		params['OrderBy'] = "Year"

		result= api.request(params)
		if(result == None):
			print" Microsoft API maybe not working..."
		print peoples +" have {0} publications since 2005".format(result['TotalItem'])