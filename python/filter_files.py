import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()    
    parser.add_argument('list')
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--operation',default='DEL',help='Can be CROP or DEL (default: DEL)')
    
    args=parser.parse_args()
    
    fl=set()
    with open(args.list) as f:
        for l in f:
            fl.add(l.strip())
    
    keep=(args.operation == 'CROP')
    
    with open(args.input) as fi:
        with open(args.output,'w') as fo:
            for l in fi:
                if l and l.split(' ')[0] in fl:
                    if keep:
                        fo.write(l)
                else:
                    if not keep:
                        fo.write(l)
                        