'''
Comparing differnt methods
1. Explicit Factor Model
2. Non-negative Matrix Factorization
3. 
'''
def loadEFM():
	recs = {}
	with open('/home/haile/Yelp Challenge/final_work/final/last/efm/efm_result') as f:
		for line in f:
			cols = line.replace(']\n','').replace('[','').replace('\'','').split(':')
			user_id = cols[0]
			business_id = cols[1]
			menus = cols[2].split(', ')
			recs[user_id] = {}
			recs[user_id][business_id] = menus
	return recs

def loadNMF():
	recs = {}
	with open('/home/haile/Yelp Challenge/final_work/final/last/NMF/nmf_result') as f:
		for line in f:
			cols = line.replace(']\n','').replace('[','').replace('\'','').split(':')
			user_id = cols[0]
			business_id = cols[1]
			menus = cols[2].split(', ')
			recs[user_id] = {}
			recs[user_id][business_id] = menus
	return recs

def loadTestData():
	data = {}
	with open('/home/haile/Yelp Challenge/final_work/final/last/test_data') as f:
		for line in f:
			line = line.replace('\n','')
			cols = line.split(',')
			user_id = cols[0]
			business_id = cols[1]
			
			foods = line.split(':')[1:]
			for f in foods:
				fs = f.lower().replace('(','').replace(')','').split(',')
				if user_id not in data:
					data[user_id] = [fs[0]]
				else:
					rec_data = data[user_id]
					if fs[0] not in rec_data:
						data[user_id].append(fs[0])

	return data

def loadRecsPro(filename):
	recs = {}
	with open(filename) as f:
		for line in f:
			cols = line.replace('\n','').split(' : ')
			user_id = cols[0]
			business_id = cols[2]
			food = cols[1]
			rating = int(cols[4])

			if user_id not in recs:
				recs[user_id] = {}
				business_rec = {}
				food_rec = {}

				food_rec[food] = rating
				business_rec[business_id] = food_rec
				recs[user_id] = business_rec
			else:
				rec_business = recs[user_id]
				if business_id not in rec_business:
					rec_business[business_id] = {}
					rec_food = {}
					rec_food[food] = rating
					rec_business[business_id] = rec_food
					recs[user_id] = rec_business
				else:
					rec_food = rec_business[business_id]
					if food not in rec_food:
						rec_food[food] = rating
						rec_business[business_id] = rec_food
						recs[user_id] = rec_business
	return recs	
		
def computePrecisionAndMRR(rec):
	data = loadTestData()
	data_precision = {}
	data_mrr = {}
	num_retrieved = 0
	num_relevant = 0
	rank = 0
	mrr = 0
	found = 0
	for user in rec:
		data_precision[user] = 0
		for business in rec[user]:
			r_food = rec[user][business]
			num_retrieved += len(r_food)
			rank += 1
			for r in r_food:
				#print r
				for d in data:
					all_food = data[d]
					for a in all_food:
						if r in a or a in r:
							if user == d:
								num_relevant += 1 
								if found == 0:
									mrr = 1/float(rank)
									found = 1
		data_precision[user] = num_relevant/float(num_retrieved) 
		data_mrr[user] = mrr
		rank = 0
		mrr = 0
		num_retrieved = 0
		num_relevant = 0
		found = 0
		
	sum_mrr = 0
	for m in data_mrr:
		sum_mrr += data_mrr[m]
	print sum_mrr/float(len(data_mrr))	

	sum_precision = 0
	for d in data_precision:
		#print d, data_precision[d]
		sum_precision += data_precision[d]
	return sum_precision/float(len(data_precision))

def computePrecisionAndMRR2(rec):
	data = loadTestData()
	data_precision = {}
	data_mrr = {}
	num_retrieved = 0
	num_relevant = 0
	mrr = 0
	rank = 0
	found = 0
	for user in rec:
		data_precision[user] = 0
		for business in rec[user]:
			r_food = rec[user][business]
			num_retrieved += len(r_food)
			for r in r_food:
				rank += 1
				num_retrieved += 1
				for d in data:
					all_food = data[d]
					for a in all_food:
						if r in a or a in r:
							if user == d:
								num_relevant += 1
								if found == 0:
									mrr = 1/float(rank)
									found = 1
		data_precision[user] = num_relevant/float(num_retrieved) 
		data_mrr[user] = mrr
		num_relevant = 0
		num_retrieved = 0
		rank = 0
		mrr = 0
		found = 0
	
	sum_mrr = 0
	for m in data_mrr:
		sum_mrr += data_mrr[m]
	print sum_mrr/float(len(data_mrr))
	
	sum_precision = 0
	for d in data_precision:
		#print d, data_precision[d]
		sum_precision += data_precision[d]
	return  sum_precision/float(len(data_precision))

if __name__ == '__main__':
	loadTestData()
	filepath = '/home/haile/Yelp Challenge/final_work/final/last/'
	recBEFM = loadRecsPro(filepath + 'recommended_based_on_efm')
	recBRBA = loadRecsPro(filepath + 'recommended_based_on_rating_as_aspect_business')
	recBRUA = loadRecsPro(filepath + 'recommended_based_on_rating_as_aspect_user')
	recBFreq = loadRecsPro(filepath + 'recommended_based_on_freq')
	recEFM = loadEFM()
	recNMF = loadNMF()
	print "EFM - Precision : " + str(computePrecisionAndMRR(recEFM))
	print "NMF - Precision : " + str(computePrecisionAndMRR(recNMF))
	
	print "Rec Based on Frequency - Precision : " + str(computePrecisionAndMRR2(recBFreq))
	print "Rec Based on EFM - Precision : " + str(computePrecisionAndMRR2(recBEFM))
	print "Rec Based on Rating as Aspect for User - Precision : " + str(computePrecisionAndMRR2(recBRUA))
	print "Rec Based on Rating as Aspect for Business - Precision : " + str(computePrecisionAndMRR2(recBRBA))
