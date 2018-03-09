import argparse


parser=argparse.ArgumentParser()
parser.add_argument('wavscp')
parser.add_argument('nsplits',type=int)
parser.add_argument('index')


args=parser.parse_args()


file_list=[]
with open(args.wavscp,'r') as f:
	for l in f:
		file_list.append(l.split(' ')[0])

with open(args.index,'w') as f:
	ns=args.nsplits
	for s in range(ns):
		f.write('split{} '.format(s+1))
	f.write('\n')
	
	curr_pos=0
	curr_split=0
	for fn in file_list:
		f.write(fn+' ')
		for s in range(ns):
			if s==curr_split:
				f.write('{} '.format(curr_pos))
			else:
				f.write('-1 ')
		f.write('\n')
		curr_split+=1
		if curr_split>=ns:
			curr_split=0
			curr_pos+=1
	
