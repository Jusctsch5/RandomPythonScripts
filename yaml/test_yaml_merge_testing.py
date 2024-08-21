import yaml

def merge_sequences(seq1, seq2):
    merged = seq1.copy()
    merged['foo'].extend(seq2['foo'])
    return merged

def test_merge_sequences():
    seq1 = yaml.safe_load('''
        foo:
        - a
        - b
        - c
    ''')
    seq2 = yaml.safe_load('''
        foo:
        - d
        - e
        - f
    ''')
    expected_merged_seq = yaml.safe_load('''
        foo:
        - a
        - b
        - c
        - d
        - e
        - f
    ''')

    actual_merged_seq = merge_sequences(seq1, seq2)
    print("_____________________________")
    print(f"seq1_______________:{seq1}")
    print(f"seq2_______________:{seq2}")
    print(f"expected_merged_seq:{expected_merged_seq}")
    print(f"actual_merged_seq__:{actual_merged_seq}")
    print("_____________________________")

    assert actual_merged_seq == expected_merged_seq

def test_merge_sequences_2():
    seq1 = yaml.safe_load('''
        foo:
        - a: b
          fun: wahoo
        - b
        - c
    ''')
    seq2 = yaml.safe_load('''
        foo:
        - d
        - e
        - f
    ''')
    expected_merged_seq = yaml.safe_load('''
        foo:
        - a: b
          fun: wahoo
        - b
        - c
        - d
        - e
        - f
    ''')

    actual_merged_seq = merge_sequences(seq1, seq2)
    print("_____________________________")
    print(f"seq1_______________:{seq1}")
    print(f"seq2_______________:{seq2}")
    print(f"expected_merged_seq:{expected_merged_seq}")
    print(f"actual_merged_seq__:{actual_merged_seq}")
    print("_____________________________")

    assert actual_merged_seq == expected_merged_seq

def test_merge_sequences_3():
    seq1 = yaml.safe_load('''
        foo:
        - a: b
          fun: wahoo
        - b
        - c
    ''')
    seq2 = yaml.safe_load('''
        foo:
        - a: b
          bar: bazhoo
        - e
        - f
    ''')
    expected_merged_seq = yaml.safe_load('''
        foo:
        - a: b
          fun: wahoo
          bar: bazhoo
        - b
        - c
        - d
        - e
        - f
    ''')

    actual_merged_seq = merge_sequences(seq1, seq2)
    print("_____________________________")
    print(f"seq1_______________:{seq1}")
    print(f"seq2_______________:{seq2}")
    print(f"expected_merged_seq:{expected_merged_seq}")
    print(f"actual_merged_seq__:{actual_merged_seq}")
    print("_____________________________")

    assert actual_merged_seq == expected_merged_seq

test_merge_sequences()
test_merge_sequences_2()
test_merge_sequences_3()