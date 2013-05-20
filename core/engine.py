#import core lib
#from core.downloader import Downloader

from include.api import api
import os
import pprint
import sys, traceback


class Engine(object):
	def __init__( self):
		pass


	
	def start(self):
		print "engine start"
		

		try:
			#read file into people_array
			print "opening data_source/reviewer_data.txt"
			ins = open( "./data_source/reviewer_data.txt", "r" )
			people_array = []
			i = 1
			for line in ins:
				line = line[:len(line)-1]
				if(i % 2 ==0 ):
					people_array.append( line )
				i = i+1
			ins.close()
			print("/data_downloaded/people_info.txt")
			wp = open( "./data_downloaded/people_info.txt", "w" )
			
			sikp = True
			num = 0
			for people in people_array:

				#if( people == "cameron marlow" or people == "chen chen" or people == "hui xiong"):
				#	sikp = False
				#else:
				#	sikp = True
				#if( sikp == True):
				#	continue
				print "[**{0}**]".format(people)
				num += 1
				"""
				if( people == "ying li"):
					value = True
				if( value == False):
					continue
				"""
				params = {}
				params['ResultObjects'] = "Author"
				params['AuthorQuery'] = people
				params['StartIdx'] = "1"
				params['EndIdx'] = "1"
				params['YearStart'] = "2005"
				#params['OrderBy'] = "Rank"
				#pprint.pprint (params)
				result=  api.request(params)
				#print ("----")
				#pprint.pprint (result)
				if(result == None or result['Result'] == None):
					continue;
				res = result['Result'][0];
				
				temp=""
				for p in res['ResearchInterestDomain']:
					temp += p['Name']+", "
				temp = temp[:len(temp)-3]	
				if( res['Affiliation'] == None):
					continue;
				Affiliation = res['Affiliation']['Name'].encode('utf-8').strip()
				
				
				
				#resquest for publitions
				#print "---------------------------------"
				start = 1
				total = 2 #res['PublicationCount'];
				once_count = 100;
				os.makedirs("paper")
				print "opening ./paper/{0}_paper.txt".format(people)
				wy = open( "./paper/{0}_paper.txt".format(people),"w")
				print "start to fetch paper, write to ./paper/{0}_paper.txt".format(people)
				while(start < total ):
					print "------------------------------------------------------------------------"
					print "reqest publication: from {0} to {1} , request :{2} ".format(start, total,once_count)
					params = {}
					params['ResultObjects'] = "Publication"
					params['PublicationContent'] = "Title,Author,Abstract,FullVersionURL"
					params['AuthorID'] = "{0}".format(res['ID'])
					params['StartIdx'] = start
					params['EndIdx'] = start+once_count
					params['YearStart'] = "2005"
					params['OrderBy'] = "Year"

					#pprint.pprint (params)

					result= api.request(params)
					#print line
					#pprint.pprint (result)
					
					#pprint.pprint(result['Result'])
					if( len(result['Result']) == 0):
						print "********* no publication result ********\n\n"
						break
					i = start
					for one in result['Result']:

						string = "[{0}]\n".format(i)+"Title: "+one['Title'].encode('ascii', 'ignore')+"\n"
						string += "Year: {0}".format(one['Year'])+"\n"
						if( one['FullVersionURL'] != None):
							for j in one['FullVersionURL']:
								string += "FullVersionURL: "+ j.encode('ascii', 'ignore')+"\n"
								break;
						else:
							string += "FullVersionURL: None\n"
						string += "Abstract: "+one['Abstract'].encode('ascii', 'ignore')+"\n"

						string+="\n"

						
						wy.write(string)
						i += 1

					total = result['TotalItem']

					start += once_count
					
				wy.close()

				res['PublicationCount'] = total
				line = "pid={0}; name={1}; affiliation={2}; g-index={3}; h-index={4}; research_domain={5}; paper_count={6}\n"\
				.format(num, people,Affiliation ,res['GIndex'], res['HIndex'],temp,res['PublicationCount'] )
				
				wp.write(line)
				#pprint.pprint (result)
				print line
				#break
			wp.close()
			print "finish"

		except (Exception) as e:
			#Log().debug("download_page failed")
			print e
			pprint.pprint (result)
			#print res['Affiliation']['Name'].decode('utf8')
			#print res['GIndex']
			#print res['HIndex']
			#print res['PublicationCount']
			traceback.print_exc(file=sys.stdout)
			#continue
			#return
		
	def stop(self):
		print "engine stop"