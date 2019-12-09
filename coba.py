jalur = [[8001, 4.810006239055881], [8002, 78.99854068022951], [8003, 266.1533504662417]]
port = 8001

tetangga2 = "null"
tetangga1 = "null"

for x in jalur:
	print "masuk for"
	print len(jalur)
	if x[0] == port:
		print "masuk port"
		if jalur.index(x) != 0:
			print "masuk if"
			tetangga1 = jalur.index(x)-1
		if jalur.index(x) < len(jalur)-1:
			print "masuk if2"
			tetangga2 = jalur.index(x)+1
print tetangga1, tetangga2