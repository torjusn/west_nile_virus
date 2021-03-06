#standard library
import os
import argparse

#misc
import timeit

#data
import numpy as np
import pandas as pd
from sklearn import preprocessing, ensemble, model_selection, decomposition, manifold

#plotting
import seaborn as sns
import matplotlib.pyplot as plt

#local
from functions import *

#Example run options for visualization
###-------------------------------------------------------------------------
#python visualize.py

def main():

	#Load data and create directories
	###-------------------------------------------------------------------------

	root = os.path.abspath(os.getcwd())

	train_dir = os.path.join(root, 'data/train.csv')
	test_dir = os.path.join(root, 'data/test.csv')
	weather_dir = os.path.join(root, 'data/weather.csv')
	spray_dir = os.path.join(root, 'data/spray.csv')

	df_train = pd.read_csv(train_dir)
	df_test = pd.read_csv(test_dir)
	df_weather = pd.read_csv(weather_dir)
	df_spray = pd.read_csv(spray_dir)

	#Explore dataframe
	###-------------------------------------------------------------------------

	print('==> SHOWING DESCRIPTORY INFORMATION FOR THE WESTNILE DATASET\n')

	#assert image directory does not exist then create one
	image_dir = os.path.join(root, 'images')
	if not os.path.exists(image_dir):
		os.makedirs(image_dir)

	#print description and save sample from dataframe
	get_df_description(df_train, 42)
	plot_and_save_sample(df_train, 42, image_dir, 'train_sample')

	#get_df_description(df_weather, 42, 'weather_sample')
	#plot_and_save_sample(df_weather, 42, image_dir, 'weather_sample')

	#get_df_description(df_spray, 42, 'spray_sample')
	#plot_and_save_sample(df_spray, 42, image_dir, 'spray_sample')

	#Preprocess features
	###-------------------------------------------------------------------------

	#separate feature and target variables
	df_xy_train = df_train.drop(['Address', 'Block', 'Street', 'AddressNumberAndStreet'], axis=1)
	#df_x_train = df_train.drop(['WnvPresent', 'Address', 'Block', 'Street', 'AddressNumberAndStreet'], axis=1)
	#df_y_train = df_train['WnvPresent']

	#unique, counts = np.unique(y_train, return_counts=True)
	#test = dict(zip(unique, counts))

	#parse out day and month from df
	df_xy_train['month'] = pd.DatetimeIndex(df_xy_train['Date']).month
	#print(x_train['month'][-5:-1])

	df_xy_train['day'] = pd.DatetimeIndex(df_xy_train['Date']).day
	#print(x_train['day'][-5:-1])

	df_xy_train = df_xy_train.drop(['Date'], axis=1)
	#print(x_train.columns)


	#encode species into numerical variable (could also use OneHotEncoder)
	#print(x_train['Species'].value_counts())

	le = preprocessing.LabelEncoder()

	df_xy_train['Species'] = le.fit_transform(df_xy_train['Species'])

	#print(x_train['Trap'].value_counts())
	df_xy_train['Trap'] = le.fit_transform(df_xy_train['Trap'])
	#print(x_train['Trap'].value_counts())

	#plot sample after feature engineering
	plot_and_save_sample(df_xy_train, 42, image_dir, 'after_fe_sample')

	#Create descriptory images
	#
	###-------------------------------------------------------------------------

	#histogram
	fig = plt.figure()
	sns.distplot(df_xy_train['NumMosquitos'])
	file_name = 'num_mosq_histogram.png'
	file_path = os.path.join(image_dir, file_name)
	plt.savefig(file_path, bbox_inches='tight')

	#correlation heatmap
	correlation_matrix = df_xy_train.corr()

	fig = plt.figure()
	sns.heatmap(correlation_matrix, vmax=0.8, annot=True, fmt='.3f', square=True)
	plt.gcf().subplots_adjust(bottom=0.15)#adjust for long column names
	file_name = 'heatmap.png'
	file_path = os.path.join(image_dir, file_name)
	plt.savefig(file_path, bbox_inches='tight')

	#TODO FISCHER TEST?

	#Dimensionality reduction
	#
	###-------------------------------------------------------------------------

	df_x_train = df_xy_train.drop(['WnvPresent'], axis=1)

	#TODO pca
	pca = decomposition.PCA(n_components=2)
	pc = pca.fit_transform(df_x_train)
	df_pc = pd.DataFrame(data = pc
			, columns = ['pc1', 'pc2'])

	df_concat = pd.concat([df_pc, df_xy_train['WnvPresent']], axis=1)

	df_concat1 = df_concat.loc[df_concat['WnvPresent'] == 1]
	df_concat2 = df_concat.loc[df_concat['WnvPresent'] == 0]

	df_concat1 = df_concat1.drop(['WnvPresent'], axis=1)
	df_concat2 = df_concat2.drop(['WnvPresent'], axis=1)

	fig = plt.figure()
	plt.scatter(df_concat1['pc1'].values, df_concat1['pc2'].values, s=5)
	plt.scatter(df_concat2['pc1'].values, df_concat2['pc2'].values, s=5)
	file_name = 'pca.png'
	file_path = os.path.join(image_dir, file_name)
	plt.savefig(file_path, bbox_inches='tight')

	#TODO t-sne
	tsne = manifold.TSNE(n_components=2)
	embeddings = tsne.fit_transform(df_x_train)
	df_embeddings = pd.DataFrame(data = embeddings
			, columns = ['dim1', 'dim2'])

	df_concat = pd.concat([df_embeddings, df_xy_train['WnvPresent']], axis=1)

	df_concat1 = df_concat.loc[df_concat['WnvPresent'] == 1]
	df_concat2 = df_concat.loc[df_concat['WnvPresent'] == 0]

	df_concat1 = df_concat1.drop(['WnvPresent'], axis=1)
	df_concat2 = df_concat2.drop(['WnvPresent'], axis=1)

	fig = plt.figure()
	plt.scatter(df_concat1['dim1'].values, df_concat1['dim2'].values, s=5)
	plt.scatter(df_concat2['dim1'].values, df_concat2['dim2'].values, s=5)
	file_name = 'tsne.png'
	file_path = os.path.join(image_dir, file_name)
	plt.savefig(file_path, bbox_inches='tight')

	plt.show()


main()