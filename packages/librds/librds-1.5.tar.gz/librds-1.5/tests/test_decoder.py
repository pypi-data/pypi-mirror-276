import librds

def test_ps():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    ps = librds.GroupGenerator.ps(basic, "radio95 ", 3,ta=True)
    ps_d = dec.decode(ps)
    assert ps_d.pty == 10
    assert ps_d.tp == True
    assert ps_d.group == 0
    assert ps_d.raw_group.is_version_b == False
    
    assert ps_d.details.segment == 3
    assert ps_d.details.di == 1
    assert ps_d.details.ms == True
    assert ps_d.details.ta == True
    assert ps_d.details.text == "5 "

def test_psb():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    psb = librds.GroupGenerator.ps_b(basic, "radio95 ", 3,ta=True)
    psb_d = dec.decode(psb)
    assert psb_d.pty == 10
    assert psb_d.tp == True
    assert psb_d.group == 0
    assert psb_d.raw_group.is_version_b == True
    assert psb_d.raw_group.c == psb_d.raw_group.a
    
    assert psb_d.details.segment == 3
    assert psb_d.details.di == 1
    assert psb_d.details.ms == True
    assert psb_d.details.ta == True
    assert psb_d.details.text == "5 "

def test_rt():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    rt = librds.GroupGenerator.rt(basic,"Test\r   ",0)
    rt_d = dec.decode(rt)
    assert rt_d.pty == 10
    assert rt_d.tp == True
    assert rt_d.group == 2
    assert rt_d.raw_group.is_version_b == False
    assert rt_d.raw_group.c != rt_d.raw_group.a
    
    assert rt_d.details.segment == 0
    assert rt_d.details.ab == False
    assert rt_d.details.text == "Test"

def test_rt2():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    rt = librds.GroupGenerator.rt(basic,"Test\r   ",0,ab=True)
    rt_d = dec.decode(rt)
    assert rt_d.pty == 10
    assert rt_d.tp == True
    assert rt_d.group == 2
    assert rt_d.raw_group.is_version_b == False
    assert rt_d.raw_group.c != rt_d.raw_group.a
    
    assert rt_d.details.segment == 0
    assert rt_d.details.ab == True
    assert rt_d.details.text == "Test"

def test_rtb():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000)
    rt = librds.GroupGenerator.rt_b(basic,"Test\r   ",0)
    rt_d = dec.decode(rt)
    assert rt_d.group == 2
    assert rt_d.raw_group.is_version_b == True
    assert rt_d.raw_group.c == rt_d.raw_group.a
    
    assert rt_d.details.segment == 0
    assert rt_d.details.ab == False
    assert rt_d.details.text == "Te"

def test_rtb2():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000)
    rt = librds.GroupGenerator.rt_b(basic,"Test\r   ",0,ab=True)
    rt_d = dec.decode(rt)
    assert rt_d.group == 2
    assert rt_d.raw_group.is_version_b == True
    assert rt_d.raw_group.c == rt_d.raw_group.a
    
    assert rt_d.details.segment == 0
    assert rt_d.details.ab == True
    assert rt_d.details.text == "Te"

def test_ecc():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000)
    eccs = []
    for i in range(0xa0, 0xf3):
        eccs.append({i: librds.GroupGenerator.ecc(basic,i)})
    for ecc in eccs:
        ecc_d = dec.decode(list(ecc.values())[0])
        assert ecc_d.group == 1
        assert ecc_d.details.data == list(ecc.keys())[0]
        assert ecc_d.details.is_lic == False

def test_lic():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000)
    lics = []
    for i in range(0x0, 0x46):
        lics.append({i: librds.GroupGenerator.lic(basic,i)})
    for lic in lics:
        lic_d = dec.decode(list(lic.values())[0])
        assert lic_d.group == 1
        assert lic_d.details.data == list(lic.keys())[0]
        assert lic_d.details.is_lic == True
        
def test_ptyn():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    ptyn = librds.GroupGenerator.ptyn(basic,"Test".ljust(8),0)
    ptyn_d = dec.decode(ptyn)
    assert ptyn_d.pty == 10
    assert ptyn_d.tp == True
    assert ptyn_d.group == 10
    assert ptyn_d.raw_group.is_version_b == False
    assert ptyn_d.raw_group.c != ptyn_d.raw_group.a
    
    assert ptyn_d.details.segment == 0
    assert ptyn_d.details.ab == False
    assert ptyn_d.details.text == "Test"
def test_ptyn2():
    dec = librds.GroupDecoder()
    basic = librds.GroupGenerator.basic(0x3000, tp=True, pty=10)
    ptyn = librds.GroupGenerator.ptyn(basic,"Test".ljust(8),0,ab=True)
    ptyn_d = dec.decode(ptyn)
    assert ptyn_d.pty == 10
    assert ptyn_d.tp == True
    assert ptyn_d.group == 10
    assert ptyn_d.raw_group.is_version_b == False
    assert ptyn_d.raw_group.c != ptyn_d.raw_group.a
    
    assert ptyn_d.details.segment == 0
    assert ptyn_d.details.ab == True
    assert ptyn_d.details.text == "Test"