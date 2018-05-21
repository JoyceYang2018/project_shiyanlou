import string

text=open('mess.txt').read()

def my_solution(text):
    s=filter(lambda x:x in string.letters,text)
    print s

if __name__ == '__main__':
    my_solution(text)


s=''.join([line.rstrip() for line in open('mess.txt')])
occ={}

for c in s:
    occ[c]=occ.get(c,0)+1
    avgoc = len(s)//len(occ)

print(''.join([c for c in s if occ[c]<avgoc]))