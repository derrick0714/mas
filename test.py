from api import api

import pprint

def main():

	
	params = {}
	params['ResultObjects'] = "Author"
	params['AuthorQuery'] = "nasir memon"
	params['StartIdx'] = "1"
	params['EndIdx'] = "1"

	result=  api.request(params)
	
	pprint.pprint(result)
	#print result

		
if __name__ == "__main__":
	main()