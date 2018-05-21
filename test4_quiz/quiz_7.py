import re,zipfile

findnothing = re.compile(r'Next nothing is (\d+)').match
seed = '90052'
comment=[]
z=zipfile.ZipFile('channel.zip','r')

while True:
    fname = seed+'.txt'
    comment.append(z.getinfo(fname).comment)
    guts = z.read(fname)
    m = findnothing(guts)
    if m:
        seed = m.group(1)
    else:
        break
print("".join(comment))