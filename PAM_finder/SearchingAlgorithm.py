from collections import defaultdict
from Bio import SeqIO
from pathlib import Path


class AhoCorasick:
    def __init__(self, words):

        self.max_states = sum([len(word) for word in words])
        self.max_characters = 4
        self.out = [0] * (self.max_states + 1)
        self.fail = [-1] * (self.max_states + 1)
        self.goto = [[-1] * self.max_characters for _ in range(self.max_states + 1)]
        self.words = words
        self.states_count = self.__build_matching_machine()

    def __build_matching_machine(self):

        k = len(self.words)
        states = 1
        for i in range(k):
            word = self.words[i]
            current_state = 0

            for character in word:
                if character == 'A':
                    ch = 0
                elif character == 'T':
                    ch = 1
                elif character == 'G':
                    ch = 2
                else:
                    character = 'C'

                if self.goto[current_state][ch] == -1:
                    self.goto[current_state][ch] = states
                    states += 1
                current_state = self.goto[current_state][ch]

            self.out[current_state] |= (1 << i)

        for ch in range(self.max_characters):
            if self.goto[0][ch] == -1:
                self.goto[0][ch] = 0

        queue = []
        for ch in range(self.max_characters):
            if self.goto[0][ch] != 0:
                self.fail[self.goto[0][ch]] = 0
                queue.append(self.goto[0][ch])

        while queue:
            state = queue.pop(0)
            for ch in range(self.max_characters):
                if self.goto[state][ch] != -1:
                    failure = self.fail[state]
                    while self.goto[failure][ch] == -1:
                        failure = self.fail[failure]

                    failure = self.goto[failure][ch]
                    self.fail[self.goto[state][ch]] = failure
                    self.out[self.goto[state][ch]] |= self.out[failure]
                    queue.append(self.goto[state][ch])

        return states

    def __find_next_state(self, current_state, next_input):
        answer = current_state

        if next_input == 'A':
            ch = 0
        elif next_input == 'T':
            ch = 1
        elif next_input == 'G':
            ch = 2
        else:
            ch = 3

        while self.goto[answer][ch] == -1:
            answer = self.fail[answer]

        return self.goto[answer][ch]

    def search_words(self, text):

        current_state = 0
        result = defaultdict(list)

        for i in range(len(text)):
            current_state = self.__find_next_state(current_state, text[i])
            if self.out[current_state] == 0: continue
            for j in range(len(self.words)):
                if (self.out[current_state] & (1 << j)) > 0:
                    word = self.words[j]
                    result[word].append(i - len(word) + 1)

        return result


def search(filename, PAMs):

    seq = str()
    fasta_sequences = SeqIO.parse(open(Path('/home/roshan/PycharmProjects/djangoProject/PAM_finder/media') / filename), 'fasta')
    for fasta in fasta_sequences:
        name, seq = fasta.id, str(fasta.seq)

    aho_corasick = AhoCorasick(PAMs)
    result = aho_corasick.search_words(seq)

    result_text = str()
    for PAM in result.keys():
        for i in result[PAM]:
            result_text += f"PAM {PAM} appears from {i} to {i + len(PAM) - 1} with "
            result_text += f"Guide RNA: {seq[i + len(PAM): i + len(PAM) + 20]} \n, "

    return result_text
