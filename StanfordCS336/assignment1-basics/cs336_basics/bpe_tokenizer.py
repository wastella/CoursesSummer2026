import regex as re


def BPETokenizer(input_path, vocab_size):
    # TODO
    # [*] Initial vocab
    # [*] Pre-tokenization
    # [*] compute merges
    # [] handle special tokens
    # byte object --> 1-256 ID#
    vocab = {}

    # Initialize vocab with first 256 unicode chars
    for i in range(256):
        vocab.update({i: bytes([i])})

    """ Open file and get text
    input_text = ""
    with open(input_path) as f:
        input_text += f.read()
    """
    input_text = """low low low low low
    lower lower widest widest widest
    newest newest newest newest newest newest"""

    # Pre-tokenization
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

    pretok_freq_table = {}
    for pre_tok in re.finditer(PAT, input_text):
        if pre_tok in pretok_freq_table:
            pretok_freq_table[tuple(pre_tok.group())] += 1
        else:
            pretok_freq_table[tuple(pre_tok.group())] = 1

    # Get all pair
    print("Before:")
    for k, v in pretok_freq_table.items():
        print(k, end="")
        print(" : " + str(v) + "\n")
    print(len(pretok_freq_table))
    # Compute BPE merges
    freq = {}
    for pretok in pretok_freq_table:
        pretok_freq = pretok_freq_table[pretok]
        for i in range(0, len(pretok) - 1):
            # Get pair i and i+1
            curr = pretok[i]
            next = pretok[i + 1]
            pair = (curr, next)
            if pair in freq:
                freq[pair] += pretok_freq
            else:
                freq[pair] = pretok_freq

    sorted_freq = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)
    most_freq = sorted_freq[0]
    print(most_freq)
    for key in list(pretok_freq_table.keys()):
        new_key = []
        for i in range(0, len(key)):
            print(key[i])
            if key[i] == most_freq[0] and key[i + 1] == most_freq[1]:
                new_key.append(str(most_freq[0] + most_freq[1]))
                i += 2
            else:
                new_key.append(key[i])

        pretok_freq_table[tuple(new_key)] = pretok_freq_table.pop(key)
        vocab[str(most_freq[0] + most_freq[1])] = len(vocab)

    print("After running: ")
    for k, v in pretok_freq_table.items():
        print(k, end="")
        print(" : " + str(v) + "\n")
    return vocab


dict = BPETokenizer("test.txt", 500)
"""
for k, v in dict.items():
    print(k, end="")
    print(" : " + str(v) + "\n")
"""
"""
for k, v in pretok_freq_table.items():
    print(k, end="")
    print(" : " + str(v) + "\n")
"""
