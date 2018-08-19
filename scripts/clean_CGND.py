import os, sys, pickle

def flatten(list_of_lists): return [item for sublist in list_of_lists for item in sublist]

def removeEmptyFolders(path, removeRoot=True):

	if not os.path.isdir(path):
		return

	# remove empty subfolders
	files = os.listdir(path)
	if len(files):
		for f in files:
			fullpath = os.path.join(path, f)
			if os.path.isdir(fullpath):
				removeEmptyFolders(fullpath)

	# if folder empty, delete it
	files = os.listdir(path)
	if len(files) == 0 and removeRoot:
		os.rmdir(path)


# Usage: python ~/galaxy-neurolincs/scripts/clean_CGND.py /pool/data/globus/PUSHED_FROM_NYGC/CGND_XXXXX

# TODO this script now needs to take into account level1_fastq / level2_bam / level3_vcf

if __name__ == '__main__':

	base_filepath = sys.argv[1]

	all_file_paths = flatten([[os.path.join(path, file) for file in files] for path, subdirs, files in os.walk(base_filepath) if len(files)])

	for filepath in all_file_paths:

		if filepath[-4:] == '.md5':
			os.remove(filepath)

		else:
			filepath_parts = filepath.split('/')
			sample_name = [part for part in filepath_parts if 'Sample_' in part]

			if len(sample_name) == 0:

				if 'StructuralVariants' in filepath:
					os.renames(os.path.join(base_filepath, filepath), os.path.join(base_filepath, 'StructuralVariants', filepath_parts[-1]))
				elif 'ExpansionHunter' in filepath:
					os.renames(os.path.join(base_filepath, filepath), os.path.join(base_filepath, 'ExpansionHunter', filepath_parts[-1]))
				else: print('no sample name in: ' + filepath)

			elif len(sample_name) == 1:

				if 'StructuralVariants' in filepath:
					os.renames(os.path.join(base_filepath, filepath), os.path.join(base_filepath, sample_name[0], 'StructuralVariants', filepath_parts[-1]))
				else:
					os.renames(os.path.join(base_filepath, filepath), os.path.join(base_filepath, sample_name[0], filepath_parts[-1]))

			else: print('possibly too many sample names in: ' + filepath)


	removeEmptyFolders(base_filepath)




