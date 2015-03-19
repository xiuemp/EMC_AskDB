import read_log
import statistic_log
import plot

def export_pd(log_path, category_key, output_path, index_time, index_type, index_sent, index_received, index_latency, filter_key):
	"""
	Transfer the original log to .pd file
	"""
	return read_log.parse(log_path, category_key, output_path, int(index_time), int(index_type), \
		int(index_sent), int(index_received), int(index_latency), filter_key)

def export_domain(pd_path, category_name, type_name):
	"""
	Analyze .pd file & export the result_set contain the scale range of selected domain
	"""
	return statistic_log.statistic(pd_path, category_name, type_name)

def export_refine(source_path, category, type_, dimension, time_range, size_range, latency_range, output_path_directory):
	"""
	Transfer the .pd file to .refine file, which is ready to plot, return output file name
	"""
	return statistic_log.refine(source_path, category, type_, dimension, time_range, size_range, latency_range, output_path_directory)

def export_plot(pic_type, refine_file, output_path, x_label_tip, y_label_tip, y_min, y_max):
	"""
	Export the png file for given .refine file, return the pic_name.png
	"""
	if pic_type == 'scatter':
		return plot.scatter(refine_file, output_path, x_label_tip, y_label_tip, y_min, y_max)
