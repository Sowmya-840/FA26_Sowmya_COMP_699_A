"""Validate the two-channel, format-212 MIT-BIH inputs without WFDB."""
import argparse
import csv
from pathlib import Path


def annotation_counts(data, samples):
    i = pos = n = v = 0
    while i + 2 <= len(data):
        a, b = data[i:i+2]; i += 2
        code, delta = b >> 2, a + ((b & 3) << 8)
        if code == 0 and delta == 0:
            if i != len(data): raise ValueError('Trailing annotation bytes')
            return n, v
        if code == 59:
            if i+4 > len(data): raise ValueError('Truncated SKIP')
            x = data[i:i+4]; i += 4
            pos += int.from_bytes(x[2:4]+x[:2], 'little', signed=True)
        elif code == 63:
            i += delta + (delta % 2)
            if i > len(data): raise ValueError('Truncated AUX')
        elif code not in (60,61,62):
            pos += delta
            if not 0 <= pos < samples: raise ValueError('Annotation outside signal')
            n += code == 1; v += code == 5
    raise ValueError('Missing annotation terminator')


def validate_record(root, rid):
    lines = (root / (rid+'.hea')).read_text().splitlines()
    record, channels, hz, samples = lines[0].split()[:4]
    samples = int(samples)
    fields = [line.split() for line in lines[1:3]]
    if (record, channels, hz) != (rid,'2','360') or samples <= 0:
        raise ValueError('Unexpected header')
    if any(f[0] != rid+'.dat' or f[1] != '212' for f in fields) or fields[0][-1] != 'MLII':
        raise ValueError('Unexpected signal format or lead')
    data = (root / (rid+'.dat')).read_bytes()
    if len(data) != samples*3: raise ValueError('Signal length mismatch')
    sums = [0,0]
    for i in range(0,len(data),3):
        a,b,c = data[i:i+3]
        values = [a+((b&15)<<8), c+((b&240)<<4)]
        for j,x in enumerate(values):
            x = x-4096 if x>=2048 else x
            if i==0 and x != int(fields[j][5]): raise ValueError('Initial sample mismatch')
            sums[j] += x
    if any(s%65536 != int(f[6])%65536 for s,f in zip(sums,fields)):
        raise ValueError('Checksum mismatch')
    n,v = annotation_counts((root/(rid+'.atr')).read_bytes(),samples)
    if not n or not v: raise ValueError('Missing target class')
    return dict(record_id=rid,n_annotations=n,v_annotations=v,signal_checksum='pass')

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('root',type=Path); p.add_argument('records',nargs='+'); args=p.parse_args()
    rows=[validate_record(args.root,r) for r in args.records]
    import sys
    w=csv.DictWriter(sys.stdout,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
