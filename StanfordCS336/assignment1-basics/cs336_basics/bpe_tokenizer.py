import regex as re


def BPETokenizer(input_path, vocab_size, special_tokens):
    # TODO
    # [*] Initial vocab
    # [*] Pre-tokenization
    # [*] compute merges
    # [] handle special tokens
    # byte object --> 1-256 ID#
    vocab = {}
    merges = []

    # Initialize vocab with first 256 unicode chars
    for i in range(256):
        vocab.update({bytes([i]): i})

    input_text = ""
    with open(input_path) as f:
        input_text += f.read()

    # AI helped me with regex shit
    special_pattern = "|".join(re.escape(tok) for tok in special_tokens)
    text_chunks = re.split(special_pattern, input_text)

    # Pre-tokenization
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

    pretok_freq_table = {}
    for chunk in text_chunks:
        for pre_tok in re.finditer(PAT, chunk):
            # Used AI to help me with the byte splitting stuff
            b = pre_tok.group().encode("utf-8")
            token = tuple(b[i:i+1] for i in range(len(b)))
            if token in pretok_freq_table:
                pretok_freq_table[token] += 1
            else:
                pretok_freq_table[token] = 1


    for iterr in range(vocab_size - 256):
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

        winner = max(freq.keys(), key=lambda k: (freq[k], k))

        new_key = []
        for key in list(pretok_freq_table.keys()):
            new_key = []
            i = 0
            while i < len(key):
                if i < len(key)-1 and key[i] == winner[0] and key[i + 1] == winner[1]:
                    new_key.append(winner[0] + winner[1])
                    i += 2
                else:
                    new_key.append(key[i])
                    i += 1

            pretok_freq_table[tuple(new_key)] = pretok_freq_table.pop(key)

        vocab[winner[0] + winner[1]] = len(vocab)
        merges.append(tuple([winner[0], winner[1]]))

        #print(pretok_freq_table)
        #print(vocab)
    return vocab, merges


dict, merges = BPETokenizer("test.txt", 500, ["<|endoftext|>"])
print(dict)
print(merges)
