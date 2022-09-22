import random
from collections import defaultdict
from Bio import SeqIO
from io import StringIO
from pathlib import Path
from django.conf import settings
from dna_features_viewer import GraphicFeature, GraphicRecord


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
                    ch = 3

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
            if self.out[current_state] == 0:
                continue
            for j in range(len(self.words)):
                if (self.out[current_state] & (1 << j)) > 0:
                    word = self.words[j]
                    result[word].append(i - len(word) + 1)

        return result


def CAS_to_PAM(cas):
    N = ["A", "T", "G", "C"]
    R = ["A", "G"]
    Y = ["C", "T"]
    W = ["A", "T"]
    V = ["G", "C", "A"]
    D = ["A", "T", "G"]
    PAM = ["ATGC"]

    if cas == "SpCas9":
        PAM = [n+"GG" for n in N]

    elif cas == "SaCas9":
        PAM = [n1+"G"+r1+r2+n2 for n1 in N for r1 in R for r2 in R for n2 in N]

    elif cas == "NmeCas9":
        PAM = [n1+n2+n3+n4+"GATT" for n1 in N for n2 in N for n3 in N for n4 in N]

    elif cas == "CjCas9":
        PAM = [n1+n2+n3+n4+r+y+"AC" for n1 in N for n2 in N for n3 in N for n4 in N for r in R for y in Y]

    elif cas == "StCas9":
        PAM = [n1+n2+"AGAA"+w for n1 in N for n2 in N for w in W]

    elif cas == "LbCpf1" or cas == "AsCpf1":
        PAM = ["TTT"+v for v in V]

    elif cas == "AaCas12b":
        PAM = ["TT"+n for n in N]

    elif cas == "BhCas12bv4":
        PAM = [d+"TTN" for d in D]

    elif cas == "Cas14":
        PAM = ["TTTA"]

    PAM = list(set(PAM))

    return PAM


def search(filename, CAS):

    fasta_sequences = SeqIO.parse(StringIO(filename.read().decode()), "fasta")

    for fasta in fasta_sequences:
        name, seq = fasta.id, str(fasta.seq)

    aho_corasick = AhoCorasick(CAS_to_PAM(CAS))
    result = aho_corasick.search_words(seq)

    result_text = str()
    indexes = []
    for PAM in result.keys():
        for i in result[PAM]:
            result_text += f"PAM {PAM} appears from {i} to {i + len(PAM) - 1} with "
            result_text += f"Guide RNA: {seq[i + len(PAM): i + len(PAM) + 20]} \n, "
            indexes.append([i, i + len(PAM) + 20, PAM])

    print(result)
    features = []
    for i, j, pam in indexes:
        pam_no = sum([ord(c) for c in pam])
        random.seed(pam_no)
        color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        features.append(GraphicFeature(start=i, end=j, strand=+1, color=color, label=pam))

    print(features)

    record = GraphicRecord(sequence=seq, features=features)

    record.plot_on_multiple_pages(
        settings.MEDIA_ROOT + "/Images/multipage_plot.pdf",
        nucl_per_line=140,
        lines_per_page=7,
        plot_sequence=True
    )

    return result_text
