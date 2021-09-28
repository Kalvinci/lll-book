import utility as util
from datetime import datetime
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_filepath):
	df = pd.read_csv("book_with_grids.csv")
	grid_deviceids_map = {}
	for row in df.itertuples():
		if row.grid in grid_deviceids_map:
			grid_deviceids_map[row.grid].append(row.device_id)
		else:
			grid_deviceids_map[row.grid] = [row.device_id]

	deviceid_datapoint_countmap = util.get_deviceid_datapoint_countmap(fields, start_datetime, end_datetime, list(df["device_id"]))

	data = []
	row = 0
	column = 'A'
	for grid in range(200):
		data_points = 0
		if grid in grid_deviceids_map:
			for device_id in grid_deviceids_map[grid]:
				if device_id in deviceid_datapoint_countmap:
					data_points += deviceid_datapoint_countmap[device_id]
		data.append([column, row, grid, data_points])
		column = chr(ord(column) + 1)
		if column == "U":
			row += 1
			column = "A"
			
	grid_df = pd.DataFrame(data, columns=["Column", "Row", "grid", "data_points"])
	# grid_df.to_csv("grid_datapoints.csv", index=False)
	grid_df = grid_df.pivot(index="Row", columns="Column", values="data_points")
	
	plt.figure(figsize=(25, 10))
	ax = sns.heatmap(grid_df, linewidths=1, cmap="YlGnBu", annot=True, fmt="d")
	field_str = ",".join(fields)
	plt.title(f"LinkLab Heatmap - [{field_str}]")
	filepath = f"{export_filepath}/LinkLab_Heatmap.png"
	plt.savefig(filepath)

	return filepath

start_datetime = datetime(2021,1,1)
end_datetime = datetime(2021,9,23)
generate_linklab_heatmap(start_datetime, end_datetime, fields=["Illumination_lx","Range select","Supply voltage_V","rssi"], export_filepath="./img")