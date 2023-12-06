import os

if '__main__' == __name__:
    xdict = os.environ
    xkeys = sorted(xdict.keys())
    for k in xkeys:
        print(f'|{k}|=|{xdict[k]}|')
