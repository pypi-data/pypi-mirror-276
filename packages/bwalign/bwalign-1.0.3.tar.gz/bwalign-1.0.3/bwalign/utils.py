from Bio import SeqIO
from typing import List, Tuple
import sys
import random
import math

def calculate_mapping_quality(score, read_length):  
    max_possible_score = 2 * read_length
    
    if score < 0:
        return 0 

    if max_possible_score > 0:
        probability = score / max_possible_score
    else:
        probability = 0

    if probability > 0:
        mapping_quality = -10 * math.log10(1 - probability)
    else:
        mapping_quality = 0

    return min(int(mapping_quality), 60)

### CIGAR STRING CREATOR

def calculate_cigar(alignment_s, alignment_t):
    cigar = []
    match = 0
    ins = 0
    del_ = 0

    for s, t in zip(alignment_s, alignment_t):
        if s == '-' and t != '-':  #del in quer
            if match > 0:
                cigar.append(f"{match}M") 
                match = 0
            del_ += 1
        elif s != '-' and t == '-':  #insertion
            if match > 0:
                cigar.append(f"{match}M")
                match = 0
            ins += 1
        else:  # Match or mismatch
            if ins > 0:
                cigar.append(f"{ins}I")  
                ins = 0
            if del_ > 0:
                cigar.append(f"{del_}D")
                del_ = 0
            match += 1

    if match > 0:
        cigar.append(f"{match}M")
    if ins > 0:
        cigar.append(f"{ins}I")
    if del_ > 0:
        cigar.append(f"{del_}D")

    return ''.join(cigar)

### CIGAR STRING CREATOR

def calculate_cigar(alignment_s, alignment_t):
    cigar = []
    match = 0
    ins = 0
    del_ = 0

    for s, t in zip(alignment_s, alignment_t):
        if s == '-' and t != '-':  #del in quer
            if match > 0:
                cigar.append(f"{match}M") 
                match = 0
            del_ += 1
        elif s != '-' and t == '-':  #insertion
            if match > 0:
                cigar.append(f"{match}M")
                match = 0
            ins += 1
        else:  # Match or mismatch
            if ins > 0:
                cigar.append(f"{ins}I")  
                ins = 0
            if del_ > 0:
                cigar.append(f"{del_}D")
                del_ = 0
            match += 1

    if match > 0:
        cigar.append(f"{match}M")
    if ins > 0:
        cigar.append(f"{ins}I")
    if del_ > 0:
        cigar.append(f"{del_}D")

    return ''.join(cigar)

### AFFINE ALIGNMENT

def AffineAlignment(match_reward: int, mismatch_penalty: int,
                    gap_opening_penalty: int, gap_extension_penalty: int,
                    s: str, t: str) -> tuple[int, str, str]:
    """Generates the affine alignment of two strings s and t."""
    sys.setrecursionlimit(1500)
    lower = [[0] * (len(t) + 1) for _ in range(len(s) + 1)] # insertions matrix
    upper = [[0] * (len(t) + 1) for _ in range(len(s) + 1)] # deletions matrix
    middle = [[0] * (len(t) + 1) for _ in range(len(s) + 1)] # match/mismatch matrix
    b_lower = [[None] * (len(t)) for _ in range(len(s))] # backtrack insertions
    b_upper = [[None] * (len(t)) for _ in range(len(s))] # backtrack deletions
    b_middle = [[None] * (len(t)) for _ in range(len(s))] # backtrack ms/mms
    for i in range(0, len(s) + 1):
        for j in range(0, len(t) + 1):
            # set base cases for middle using gap opening and extension penalties, base for lower and upper is -infinity.
            if i == 0 and j == 0:
                lower[i][j], upper[i][j] = float('-inf'), float('-inf')
                continue
            elif i == 0:
                lower[i][j], middle[i][j] = float('-inf'), -gap_opening_penalty - ((j-1) * gap_extension_penalty)
                continue
            elif j == 0:
                upper[i][j], middle[i][j] = float('-inf'), -gap_opening_penalty - ((i-1) * gap_extension_penalty)
                continue
            
            # test for match
            match = -mismatch_penalty
            if s[i-1] == t[j-1]:
                match = match_reward
            
            lower[i][j] = max(lower[i-1][j] - gap_extension_penalty, middle[i-1][j] - gap_opening_penalty)
            upper[i][j] = max(upper[i][j-1] - gap_extension_penalty, middle[i][j-1] - gap_opening_penalty)
            middle[i][j] = max(lower[i][j], upper[i][j], middle[i-1][j-1] + match)
            if lower[i][j] == lower[i-1][j] - gap_extension_penalty:
                b_lower[i-1][j-1] = 'd'
            elif lower[i][j] == middle[i-1][j] - gap_opening_penalty:
                b_lower[i-1][j-1] = 'open'
            if upper[i][j] == upper[i][j-1] - gap_extension_penalty:
                b_upper[i-1][j-1] = 'r'
            elif upper[i][j] == middle[i][j-1] - gap_opening_penalty:
                b_upper[i-1][j-1] = 'open'
            if middle[i][j] == lower[i][j]:
                b_middle[i-1][j-1] = 'in_close'
            elif middle[i][j] == upper[i][j]:
                b_middle[i-1][j-1] = 'del_close'
            elif middle[i][j] == middle[i-1][j-1] + match:
                b_middle[i-1][j-1] = 'dr'
    s_align, t_align = backtrack(s, t, b_lower, b_upper, b_middle, len(s) - 1, len(t) - 1, 'middle')
    return max(lower[len(s)][len(t)], middle[len(s)][len(t)], upper[len(s)][len(t)]), s_align, t_align
                
def backtrack(s: str, t: str, b_lower: list[list[str]], b_upper: list[list[str]], b_middle: list[list[str]], i: int, j: int, LEVEL: str) -> tuple[str,str]:
    if i < 0 and j < 0: # if both i and j reach -1 at the same time, we can just return empty string.
        return '',''
    elif i < 0: # if i reaches -1 first, need to append the rest of t up to index j to t prime, and a number of '-' equal to the length of that string to s prime.
        return '-' * (j + 1), t[0:j+1]
    elif j < 0: # same as i < 0 condition but for j.
        return s[0:i+1], '-' * (i + 1)
    # my use of the LEVEL variable tells us which matrix this call is backtracking in.
    if LEVEL == 'middle':
        if b_middle[i][j] == 'in_close':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i, j, 'lower')
            return s_prime, t_prime
        elif b_middle[i][j] == 'del_close':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i, j, 'upper')
            return s_prime, t_prime
        elif b_middle[i][j] == 'dr':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i-1, j-1, 'middle')
            return s_prime + s[i], t_prime + t[j]
    elif LEVEL == 'lower':
        if b_lower[i][j] == 'd':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i-1, j, 'lower')
            return s_prime + s[i], t_prime + '-'
        elif b_lower[i][j] == 'open':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i-1, j, 'middle')
            return s_prime + s[i], t_prime + '-'
    elif LEVEL == 'upper':
        if b_upper[i][j] == 'r':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i, j-1, 'upper')
            return s_prime + '-', t_prime + t[j]
        elif b_upper[i][j] == 'open':
            s_prime, t_prime = backtrack(s, t, b_lower, b_upper, b_middle, i, j-1, 'middle')
            return s_prime + '-', t_prime + t[j]

### SEED EXTENSION

def compute_max_seed(ref: str, read: str, seed_idxes: list[list[int]],
                     match_reward: int, mismatch_penalty: int,
                     gap_opening_penalty: int, gap_extension_penalty: int,
                     read_length: int) -> tuple[int, int, str, str]:
    """
    For each index in the seeds list, generates an affine alignment (50x50) for each seed index.
    By the end, returns position in ref and score of max scoring alignment. The alignment
    will be between the entire read and a length 50 segment of the reference starting at
    the calculated position. Version 2 of this function now also returns the alignments 
    themselves of the read and respective 50 base segment of the ref genome.
    """
    best_score = float('-inf')
    best_idx = -1
    s_best_align = ''
    t_best_align = ''
    for i in range(0, len(seed_idxes)):
        for ref_idx in seed_idxes[i]:
            ref_segment = ref[ref_idx - i:ref_idx - i + read_length]
            score, s_align, t_align, = AffineAlignment(match_reward, mismatch_penalty, 
                                            gap_opening_penalty, gap_extension_penalty,
                                            ref_segment, read)
            if score > best_score:
                best_score = score
                best_idx = ref_idx
                s_best_align = s_align
                t_best_align = t_align
    return best_idx, best_score, s_best_align, t_best_align

### SEED GENERATION

# SUFFIX ARRAY CONSTRUCTION

class suffix:
    """
    Class built to store suffix array indices, conserving memory.
    """
    def __init__(self):
        self.index = 0
        self.rank = [0,0]

def get_rank(char: str) -> int:
    """
    Converts the given char to its ascii value, then subtracts 'a' from it to get a
    clean rank value.
    """
    return ord(char) - ord('a')

def suffix_array(text: str) -> list[int]:
    """
    Generates the suffix array of a given database string text using O(n(logn)^2)
    time complexity and O(n) space. To improve to O(nlogn), can use radix sort to
    sort the suffix lists.
    
    Algorithm ripped from:
    https://www.geeksforgeeks.org/suffix-array-set-2-a-nlognlogn-algorithm/
    """
    
    # get the intial array of suffixes before starting to loop through and rank them.
    suffixes = [suffix() for _ in range(len(text))]
    
    # initial (k=2) ranking of suffixes
    for i in range(0, len(text)):
        suffixes[i].index = i
        suffixes[i].rank[0] = get_rank(text[i])
        if (i + 1) < len(text):
            suffixes[i].rank[1] = get_rank(text[i+1])
        else:
            suffixes[i].rank[1] = -1
    
    # https://stackoverflow.com/questions/9376384/sort-a-list-of-tuples-depending-on-two-elements
    suffixes = sorted(suffixes, key=lambda element: (element.rank[0], element.rank[1]))
    
    ind = [0] * len(text) # array to keep track of indices while computing ranks
    
    k = 4
    while (k < 2 * len(text)):
         
        # Assigning rank and index 
        # values to first suffix
        rank = 0
        prev_rank = suffixes[0].rank[0]
        suffixes[0].rank[0] = rank
        ind[suffixes[0].index] = 0
 
        # Assigning rank to suffixes
        for i in range(1, len(text)):
             
            # If first rank and next ranks are 
            # same as that of previous suffix in
            # array, assign the same new rank to 
            # this suffix
            if (suffixes[i].rank[0] == prev_rank and
                suffixes[i].rank[1] == suffixes[i - 1].rank[1]):
                prev_rank = suffixes[i].rank[0]
                suffixes[i].rank[0] = rank
                 
            # Otherwise increment rank and assign    
            else:  
                prev_rank = suffixes[i].rank[0]
                rank += 1
                suffixes[i].rank[0] = rank
            ind[suffixes[i].index] = i
 
        # Assign next rank to every suffix
        for i in range(len(text)):
            nextindex = suffixes[i].index + k // 2
            suffixes[i].rank[1] = suffixes[ind[nextindex]].rank[0] if (nextindex < len(text)) else -1
 
        # Sort the suffixes according to
        # first k characters
        suffixes = sorted(suffixes, key = lambda element: (element.rank[0], element.rank[1]))
 
        k *= 2
        
    to_return = []
    for i in range(0, len(text)):
        to_return.append(suffixes[i].index)
        
    return to_return

def partial_suffix_array(sa: list[int], k: int) -> dict[int, int]:
    """
    Generate a partial suffix array for the given text and interval K.
    """
    partial = dict()
    for idx in sa:
        if sa[idx] % k == 0:
            partial[idx] = sa[idx]
    return partial

## BWT creation
def bwt_from_suffix_array(text: str, suffix_array: List[int]) -> str:
    bwt = []
    for idx in suffix_array:
        bwt.append(text[idx-1])
    return ''.join(bwt)

def compute_rank_arr(bwt: str) -> list[int]:
    """
    This function generates the rank of each position in the last column given by the bwt.
    The rank is the number of occurrences of whatever character is at that position, up to
    that position. This can be done in linear time by iterating through the bwt. The ranks
    will be returned in the form of a list of ranks, obviously indices will be in-built.
    """
    rank = []
    counts = dict()
    for char in bwt:
        if char not in counts: counts[char] = 0
        counts[char] += 1
        rank.append(counts[char])
    return rank

def compute_first_occurrences(bwt: str) -> dict[str, int]: # the mapping of c in C is the row at which the character c appears in the first column for the first time.
    """
    Generate a dict where each 'character' is mapped to the index in first column where
    these characters first appeared. In other words because the first column is in alphabetical
    order, we can count the ascii code of each character in the last column, then iterate
    from 0 to 255 to get the count of each ascii character in ascending lexicographic order.
    This is done in linear time.
    """
    C = dict()
    counts = [0 for _ in range(256)]
    for char in bwt:
        C[char] = 0
        counts[ord(char)] += 1
    curr_idx = 0
    for i in range(0,256):
        if counts[i] != 0:
            C[chr(i)] = curr_idx
        for _ in range(counts[i]):
            curr_idx += 1
    return C

def compute_checkpoint_arrs(bwt: str) -> dict[int, list[int]]:
    """
    Similar to ranks, but instead the list stored contains the rank of every character up to
    that index, if the index % C is 0. More memory efficient.
    """
    C = 5
    ranks = dict()
    rank = [0 for _ in range(256)]
    for i in range(0, len(bwt)):
        rank[ord(bwt[i])] += 1
        if i % C == 0:
            ranks[i] = rank[:]
    return ranks

def compute_rank(bwt: str, idx: int, ranks: dict[int, list[int]], symbol: str, C: int) -> int: # idx can be either top or bot
    idx_dist_from_chkpnt = idx % C
    idx_rank = ranks[idx - idx_dist_from_chkpnt][ord(symbol)]
    for j in range(idx - idx_dist_from_chkpnt + 1, idx + 1):
        if bwt[j] == symbol:
            idx_rank += 1
    return idx_rank

def bw_better_match_pattern(bwt: str, pattern: str, first_occurrences: dict[str,int], ranks: list[list[int]]) -> tuple[int,int]:
    C = 5
    top = 0
    bot = len(bwt) - 1
    for i in range(len(pattern) - 1, -1, -1):
        symbol = pattern[i]
        if symbol not in first_occurrences: # in the case the symbol is not in text at all
            return (0,0)
        top_rank = compute_rank(bwt, top, ranks, symbol, C) # use checkpoint arrs to get the rank
        bot_rank = compute_rank(bwt, bot, ranks, symbol, C)
        marker = False
        if bwt[top] == symbol:
            marker = True
        top = first_occurrences[symbol] + top_rank
        if marker:
            top -= 1
        bot = first_occurrences[symbol] + bot_rank - 1
        if bot - top < 0:
            return (0,0)
    return (top, bot + 1)

def compute_idxes_from_top_bot(start: int, end: int, partial_s_array: dict[int, int], bwt: str, rank: list[int], occurrences: list[int]) -> list[int]:
    pattern_idxes = []
    for i in range(start, end):
        p = i
        plus_count = 0
        while True:
            predecessor = bwt[p]
            p = occurrences[predecessor] + rank[p] - 1
            plus_count += 1
            if p in iter(partial_s_array.keys()):
                break
        pattern_idxes.append((partial_s_array[p] + plus_count) % len(bwt))
    return pattern_idxes

def generate_seeds(read: str, bwt: str, k: int, psa: dict[int, int],
                                                first_occurrences: dict[str, int],
                                                checkpoint_arrs: dict[int, list[int]],
                                                ranks: list[int]) -> list[list[int]]:
    """
    Takes a read and bwt created from reference genome, and generates a list of lists
    with each index being an index i in the read from 0 to len(read) - k + 1. The corresponding list at each
    index is a list of exact match indices of the kmer at read[i:i+k] located in the reference
    genome. Note that even if two kmers are identical, their indices in the read are not.
    """
    seed_idxes = []
    for i in range(0, len(read) - k + 1):
        kmer = read[i:i+k]
        start, end = bw_better_match_pattern(bwt, kmer, first_occurrences, checkpoint_arrs)
        idxes = compute_idxes_from_top_bot(start, end, psa, bwt, ranks, first_occurrences)
        seed_idxes.append(idxes)
    return seed_idxes

### FASTQ PARSING

def parse_fastq(fastq_path: str) -> List[Tuple[str, str, List[int]]]:
    """
    Parse a FASTQ file and return a list of tuples where each tuple contains the
    sequence ID, the sequence itself, and the quality scores.
    
    :param fastq_path: Path to the FASTQ file
    :return: A list of tuples where each tuple contains the sequence ID, the sequence itself, and the quality scores
    """
    fastq_list = []
    with open(fastq_path, "r") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            fastq_list.append((record.id, str(record.seq), record.letter_annotations["phred_quality"]))
    return fastq_list

def parse_reference_genome(fasta_path: str) -> Tuple[str, str]:
    """
    Parse a FASTA file containing a reference genome and return a tuple containing
    the sequence ID and the sequence itself.

    :param fasta_path: Path to the FASTA file
    :return: A tuple containing the sequence ID and the sequence itself
    """
    with open(fasta_path, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            return record.id, str(record.seq)

def random_sequence(length: int) -> str:
    """
    Generate a random DNA sequence of the specified length.

    :param length: The length of the sequence
    :return: A random DNA sequence
    """
    return ''.join(random.choices('ACGT', k=length))

def random_quality_scores(length: int) -> List[int]:
    """
    Generate random quality scores for a sequence of the specified length.

    :param length: The length of the sequence
    :return: A list of random quality scores
    """
    return ''.join(random.choices('!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHI', k=length))

def random_id(length: int) -> str:
    """
    Generate a random sequence ID of the specified length.

    :param length: The length of the sequence ID
    :return: A random sequence ID
    """
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

def generate_fasta_file(fasta_path: str, sequence_id: str, sequence: str):
    """
    Generate a FASTA file with the specified sequence ID and sequence.

    :param fasta_path: Path to the FASTA file to be generated
    :param sequence_id: The sequence ID
    :param sequence: The sequence
    """
    with open(fasta_path, "w") as handle:
        handle.write(f">{sequence_id}\n")
        handle.write(sequence)

def generate_fastq_file(file, read_id, sequence, quality):
    """Append a read to the FASTQ file."""
    file.write(f"@{read_id}\n")
    file.write(sequence + "\n")
    file.write("+\n")
    file.write(quality + "\n")

def main():
    # Define parameters for random sequence and quality scores
    sequence_length = 100000
    sequence_id_length = 10

    # Generate random reference genome
    ref_sequence_id = random_id(sequence_id_length)
    ref_sequence = random_sequence(sequence_length)
    generate_fasta_file(r"C:\Users\Nabil\Desktop\School\Spring2024\CSE185 - Bioinfo Lab\project\bwalign\data\random_reference.fasta", ref_sequence_id, ref_sequence)

    # Parameters for FASTQ reads
    sequence_length = 50
    num_reads = 10
    fastq_filename = r"C:\Users\Nabil\Desktop\School\Spring2024\CSE185 - Bioinfo Lab\project\bwalign\data\random_reads.fastq"

    # Generate random FASTQ reads and write to a single file
    with open(fastq_filename, 'w') as file:
        for i in range(num_reads):
            read_id = random_id(sequence_id_length)
            read_sequence = random_sequence(sequence_length)
            read_quality = random_quality_scores(sequence_length)
            generate_fastq_file(file, read_id, read_sequence, read_quality)

if  __name__ == '__main__':
    main()
