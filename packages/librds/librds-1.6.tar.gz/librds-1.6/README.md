# LibRDS
[![pipeline status](https://flerken.zapto.org:1115/kuba/librds/badges/main/pipeline.svg)](https://flerken.zapto.org:1115/kuba/librds/-/commits/main)


LibRDS is a simple library that you can use to generate the RDS groups, just the groups, so something like `3000 2000 7575 7575` the origins of development of this started on 12 May, later creating the [rdPy](https://github.com/KubaPro010/rdPy) repository, here it is mostly similiar code but improved and packaged as a library

Example code:
```python
import librds

basic = librds.GroupGenerator.basic(0x3000)
print(basic)

print(librds.GroupGenerator.ps(basic,"hi",0))
```

Output:
```
    Group(a=12288, b=0, c=0, d=0, is_version_b=None)
    Group(a=12288, b=8, c=57549, d=26729, is_version_b=False)
```

**Note** that LibRDS required Python 3.10+ to run due to its use of `match` in the character set which is required for PS, RT, PTYN and also match is used in AF

# Decoder
LibRDS also includes a RDS Group decoder, so you can encode with librds and then also decode it, currently librds's decoder decodes all of the groups it can encode (such as CT, IH, TDC, etc...)