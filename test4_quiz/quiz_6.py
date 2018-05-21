import pickle

data = pickle.load(open("banner.p","rb"))
for each in data:
    s = ''.join([i[1]*i[0] for i in each])
    print s