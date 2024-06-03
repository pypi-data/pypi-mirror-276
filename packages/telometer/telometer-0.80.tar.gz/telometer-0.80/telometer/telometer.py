#!/usr/bin/env python3
# Telometer v0.79
# Created by: Santiago E Sanche8
# Artandi Lab, Stanford University, 2024
# Measures telomeres from ONT or PacBio long reads aligned to a T2T genome assembly
# Simple Usage: telometer -b sorted_t2t.bam -o output.ts8
import pysam
import re
import regex as re
import csv
import argparse
from multiprocessing import Pool, cpu_count

def reverse_complement(seq):
    """Returns the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join(complement[base] for base in reversed(seq))

def get_adapters(chemistry):
    """Returns the adapter sequences based on the sequencing chemistry."""
    if chemistry == 'r10':
        adapters = ['TTTTTTTTCCTGTACTTCGTTCAGTTACGTATTGCT', 'GCAATACGTAACTGAACGAAGTACAGG']
    else:
        adapters = ['TTTTTTTTTTTAATGTACTTCGTTCAGTTACGTATTGCT', 'GCAATACGTAACTGAACGAAGT']

    adapters_rc = [reverse_complement(adapter) for adapter in adapters]
    return adapters + adapters_rc

def get_flexible_telomere_patterns():
    """Returns flexible telomere repeat patterns for both G-rich and C-rich strands."""
    g_rich_telomere_pattern = r'(T{1,2}T{1,2}A{1,2}G{1,2}G{1,2}G{1,2}){2,}'
    c_rich_telomere_pattern = r'(C{1,2}C{1,2}C{1,2}T{1,2}A{1,2}A{1,2}){2,}'
    return g_rich_telomere_pattern, c_rich_telomere_pattern

def find_initial_boundary_region(sequence, patterns, max_mismatches):
    """Finds the initial boundary region with allowed mismatches."""
    boundary_length = 0
    combined_pattern = '|'.join(f'({pattern})' for pattern in patterns)
    regex_pattern = f'({combined_pattern}){{2,}}'

    for match in re.finditer(f'({regex_pattern}){{e<={max_mismatches}}}', sequence, re.BESTMATCH):
        boundary_length = max(boundary_length, len(match.group(0)))
    return boundary_length

def determine_arm(reference_name, alignment_start, reference_length):
    """Determine the chromosome arm based on the alignment start position and reference name."""
    if alignment_start < 15000 and "q" not in reference_name:
        return "p"
    return "q"

def process_read(args):
    read_data, g_rich_telomere_pattern, c_rich_telomere_pattern, adapters, minreadlen = args

    if read_data['is_unmapped'] or read_data['query_sequence'] is None or len(read_data['query_sequence']) < minreadlen:
        print(f"Skipping read {read_data['read_id']}: unmapped or too short")
        return None

    alignment_start = read_data['reference_start']
    alignment_end = read_data['reference_end']
    seq_to_check = read_data['query_sequence']

    if read_data['is_reverse']:
        direction = "rev"
        seq_to_check = reverse_complement(seq_to_check)
    else:
        direction = "fwd"

    reference_genome_length = read_data['reference_length']
    if alignment_start >= 15000 and alignment_start <= reference_genome_length - 30000:
        print(f"Skipping read {read_data['read_id']}: alignment start {alignment_start} within filtered range")
        return None

    arm = determine_arm(read_data['reference_name'], alignment_start, reference_genome_length)

    telomere_starts = [m.start() for m in re.finditer(g_rich_telomere_pattern, seq_to_check)]
    if not telomere_starts:
        telomere_starts = [m.start() for m in re.finditer(c_rich_telomere_pattern, seq_to_check)]

    if telomere_starts:
        telomere_start = telomere_starts[0]

        # Find the end of the telomere region
        telomere_end = min((pos for pos in (seq_to_check.find(adapter) for adapter in adapters) if pos != -1), default=len(seq_to_check))

        telomere_region = seq_to_check[telomere_start:telomere_end]
        telomere_repeat = [m.group() for m in re.finditer(g_rich_telomere_pattern, telomere_region)]
        if not telomere_repeat:
            telomere_repeat = [m.group() for m in re.finditer(c_rich_telomere_pattern, telomere_region)]

        telomere_length = len(''.join(telomere_repeat))
        if telomere_length > 0:
        # Find the region immediately adjacent to the telomere region
            boundary_mm1_region = seq_to_check[telomere_end:]
            boundary_mm1_length = find_initial_boundary_region(boundary_mm1_region, g_rich_telomere_pattern.split('|') + c_rich_telomere_pattern.split('|'), max_mismatches=2)
            result = {
                'chromosome': read_data['reference_name'],
                'arm': arm,
                'telomere_start': telomere_start,
                'telomere_end': telomere_end,
                'telomere_length': telomere_length,
                'subtel_boundary_length': boundary_mm1_length,
                'read_id': read_data['read_id'],
                'mapping_quality': read_data['mapping_quality'],
                'direction': direction
            }
            return result
        else:
            return None


def calculate_telomere_length():
    parser = argparse.ArgumentParser(description='Calculate telomere length from a BAM file.')
    parser.add_argument('-b', '--bam', help='The path to the sorted BAM file.', required=True)
    parser.add_argument('-o', '--output', help='The path to the output file.', required=True)
    parser.add_argument('-c', '--chemistry', default="r10", help="Sequencing chemistry (r9 or r10, default=r10). Optional", required=False)
    parser.add_argument('-m', '--minreadlen', default=1000, type=int, help='Minimum read length to consider (Default: 1000 for telomere capture, use 4000 for WGS). Optional', required=False)
    args = parser.parse_args()

    adapters = get_adapters(args.chemistry)
    g_rich_telomere_pattern, c_rich_telomere_pattern = get_flexible_telomere_patterns()

    bam_file = pysam.AlignmentFile(args.bam, "rb")
    read_data_list = [{
        'read_id': read.query_name,
        'is_unmapped': read.is_unmapped,
        'reference_start': read.reference_start,
        'reference_end': read.reference_end,
        'reference_name': read.reference_name,
        'mapping_quality': read.mapping_quality,
        'query_sequence': read.query_sequence,
        'reference_length': bam_file.get_reference_length(read.reference_name) if read.reference_name is not None else None,
        'is_reverse': read.is_reverse
    } for read in bam_file if read.reference_name is not None and read.reference_name != 'chrM']

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(
            process_read,
            [(read_data, g_rich_telomere_pattern, c_rich_telomere_pattern, adapters, args.minreadlen) for read_data in read_data_list]
        )

    results = [result for result in results if result]

    # Ensure only the best result per read_id is saved
    best_results = {}
    for result in results:
        read_id = result['read_id']
        if read_id not in best_results:
            best_results[read_id] = result
        else:
            existing_result = best_results[read_id]
            if result['mapping_quality'] > existing_result['mapping_quality']:
                best_results[read_id] = result
            elif result['mapping_quality'] == existing_result['mapping_quality']:
                if result['telomere_length'] > existing_result['telomere_length']:
                    best_results[read_id] = result
                elif result['telomere_length'] == existing_result['telomere_length']:
                    # Arbitrarily keep the existing one if both telomere_length and mapping_quality are the same
                    pass

    final_results = list(best_results.values())

    if final_results:
        with open(args.output, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=final_results[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(final_results)

    print(f"Telometer completed successfully. Total telomeres measured: {len(final_results)}")

if __name__ == "__main__":
    calculate_telomere_length()
