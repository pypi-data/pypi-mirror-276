import librds

def test_sequencer():
    input = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    seq = librds.GroupSequencer(input)
    a = []
    for _ in range(len(input)*2):
        a.append(seq.get_next())
    # We circled it 2 times so 2 have input+input
    assert a == (input+input)