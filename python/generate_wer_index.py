import argparse


parser=argparse.ArgumentParser()
parser.add_argument('wavscp')
parser.add_argument('text')
parser.add_argument('edits')
parser.add_argument('nsplits',type=int)
parser.add_argument('index')


args=parser.parse_args()


file_list=[]
with open(args.wavscp,'r') as f:
	for l in f:
		file_list.append(l.split(' ')[0])

text_len={}
with open(args.text,'r') as f:
	for l in f:
		tok=l.strip().split(' ')
		text_len[tok[0]]=len(tok)-1

edits={}
with open(args.edits,'r') as f:
	for l in f:
		tok=l.strip().split(' ')
		edits[tok[0]]=int(tok[1])

wer={}
for f in file_list:
	wer[f]=edits[f]/text_len[f]

edits_index={}
edits_list=sorted(file_list,key=lambda x: edits[x],reverse=True)
for i,f in enumerate(edits_list):
	edits_index[f]=i


wer_index={}
wer_list=sorted(file_list,key=lambda x: wer[x],reverse=True)
for i,f in enumerate(wer_list):
	wer_index[f]=i

split_lists=[]
for i in range(args.nsplits):
	split_lists.append([])

curr_split=0
for f in wer_list:
	split_lists[curr_split].append(f)
	curr_split+=1
	if curr_split>=args.nsplits:
		curr_split=0
split_indices=[]
for s in split_lists:
	index={}
	for i,f in enumerate(s):
		index[f]=i
	split_indices.append(index)

with open(args.index,'w') as fo:
	fo.write('edits wer')
	for s in range(args.nsplits):
		fo.write(' split{} '.format(s))
	fo.write('\n')
	for f in file_list:
		fo.write('{} {} {}'.format(f,edits_index[f],wer_index[f]))
		for s in split_indices:
			if f in s:
				fo.write(' {}'.format(s[f]))
			else:
				fo.write(' -1')
		fo.write('\n')
		
