from numpy import clip, inf, percentile, asarray, where, size, prod, unique, bincount
from scipy.ndimage import median_filter
from sklearn.decomposition import SparsePCA
from skimage.measure import label
from skimage.morphology import remove_small_objects
from extraction import NMF
from regional import one, many
import thunder as td
import itertools
import json
import os


def sparse_pca():
	datasets = ['04.00.test']

	submission = []
	for dataset in datasets:
		print('Loading dataset: %s ' %dataset)
		dataset_path = 'neurofinder.' + dataset
		path = os.path.join('D:/Spring2019/DataSciencePracticum/p3', dataset_path, 'images')
		# Getting the images data from path
		data = td.images.fromtif(path, ext='tiff')
		sparse_pca_model = SparsePca(k=5, percentile=97, overlap=0.1)
		# Fitting on the given dataset
		model = sparse_pca_model.fit(data, chunk_size=(50,50), padding=(25,25))
		merged = model.merge(0.5)
		# Storing found regions
		regions = [{'coordinates': region.coordinates.tolist()} for region in merged.regions]
		result = {'dataset': dataset, 'regions': regions}
		submission.append(result)
	# Writing the results to submission.json
	with open('submission.json', 'w') as f:
	    f.write(json.dumps(submission))


class SparsePca(NMF):
	def __init__(self, k=5, max_iter=20, min_size=20, max_size='full', percentile=95, overlap=0.1):
		self.k = k
		self.max_iter = max_iter
		self.min_size = min_size
		self.max_size = max_size
		self.overlap = overlap
		self.percentile = percentile

	def _get(self, block):
		dims = block.shape[1:]
		max_size = prod(dims) / 2 if self.max_size == 'full' else self.max_size
		data = block.reshape(block.shape[0], -1)
		model = SparsePCA(self.k, normalize_components=True)
		model.fit(clip(data, 0, inf)) 
		components = model.components_.reshape((self.k, ) + dims)

		combined = []
		for component in components:
			tmp = component > percentile(component, self.percentile)
			labels, num = label(tmp, return_num=True)
			if num == 1:
				counts = bincount(labels.ravel())
				if counts[1] < self.min_size:
					continue
				else:
					regions = labels
			else:
				regions = remove_small_objects(labels, min_size=self.min_size)
		  
			ids = unique(regions)
			ids = ids[ids > 0]
			for ii in ids:
				r = regions == ii
				r = median_filter(r, 2)
				coords = asarray(where(r)).T
				if (size(coords) > 0) and (size(coords) < max_size):
					combined.append(one(coords))

		# merge overlapping sources
		if self.overlap is not None:

			# iterate over source pairs and find a pair to merge
			def merge(sources):
				for i1, s1 in enumerate(sources):
					for i2, s2 in enumerate(sources[i1+1:]):
						if s1.overlap(s2) > self.overlap:
							return i1, i1 + 1 + i2
					return None

		  # merge pairs until none left to merge
			pair = merge(combined)
			testing = True
			while testing:
				if pair is None:
					testing = False
				else:
					combined[pair[0]] = combined[pair[0]].merge(combined[pair[1]])
					del combined[pair[1]]
					pair = merge(combined)

		return combined		


sparse_pca()