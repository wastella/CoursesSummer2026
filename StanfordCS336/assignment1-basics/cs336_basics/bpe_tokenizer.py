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
        vocab.update({bytes([i]): i})

    input_text = "low low low low low lower lower widest widest widest newest newest newest newest newest newest"
    #with open(input_path) as f:
        #input_text += f.read()

    # Pre-tokenization
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

    pretok_freq_table = {}
    for pre_tok in re.finditer(PAT, input_text):
        token = tuple(pre_tok.group())
        if token in pretok_freq_table:
            pretok_freq_table[token] += 1
        else:
            pretok_freq_table[token] = 1

    #for itttter in range(1):
        # Compute BPE merges
    freq = {}
    for word in pretok_freq_table:
        length = len(word)
        if length > 1:
            for i in range(0, length - 1):
                # Get pair i and i+1
                curr = word[i]
                next = word[i + 1]
                pair = (curr, next)
                if pair in freq:
                    freq[pair] += pretok_freq_table[word]
                else:
                    freq[pair] = pretok_freq_table[word]

    winner = sorted(freq.keys(), key=lambda k: freq[k], reverse=True)[0]

    print(winner[0])
    print(winner[1])
    for key in list(pretok_freq_table.keys()):
        new_key = []
        i = 0
        while i < len(key):
            if i < len(key)-1 and key[i] == winner[0] and key[i + 1] == winner[1]:
                new_key.append(str(winner[0] + winner[1]))
                i += 2
            else:
                new_key.append(key[i])
                i += 1

        pretok_freq_table[tuple(new_key)] = pretok_freq_table.pop(key)
        vocab[len(vocab)] = str(winner[0] + winner[1])

    print(pretok_freq_table)
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
