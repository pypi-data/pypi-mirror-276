# == Native Modules
import re
import sys
import sys
# == Installed Modules
from Bio import SeqIO
# == Project Modules


def main():
	INPUT_FASTA = sys.argv[1]
	OUTPUT_FASTA = sys.argv[2]

	# INPUT_CHROMOSOME = "/home/ubuntu/genomes/toy_genome.fna"

	record = SeqIO.parse(open(INPUT_FASTA), "fasta")
	changed_recs = []
	for rec in record:
		a = re.search(r"Homo sapiens chromosome (\w+), GRCh38 reference primary assembly", rec.description)
		try:
			rec.id = f"chr{a.group(1)}"
			rec.name = f"chr{a.group(1)}"
			rec.description = ""
		except AttributeError:
			a = re.search(r"Homo sapiens (m)itochondrion", rec.description)
			try:
				mit_id = a.group(1)
				rec.id = f"chrMT"
				rec.name = f"chrMT"
				rec.description = ""
			except AttributeError:
				continue
		changed_recs.append(rec)

	SeqIO.write(changed_recs, OUTPUT_FASTA, 'fasta')


if __name__ == "__main__":
	main()
