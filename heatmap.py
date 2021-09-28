import utility as util
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt, image as mpimg

def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_filepath):
	try:
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
		grid_df = grid_df.pivot(index="Row", columns="Column", values="data_points")
		
		plt.figure(figsize=(25, 10))
		map_img = mpimg.imread('./img/lll_grid.png')
		heatmap = sns.heatmap(grid_df, linewidths=1, cmap="Reds", annot=True, fmt="d", alpha=0.8, zorder=2)
		heatmap.imshow(map_img, aspect=heatmap.get_aspect(), extent=heatmap.get_xlim()+heatmap.get_ylim(), zorder=1)
		plt.title(f"LinkLab Heatmap [{start_datetime.date()} - {end_datetime.date()}]")
		filepath = f"{export_filepath}/LinkLab_Heatmap_{start_datetime.date()}_{end_datetime.date()}.png"
		plt.savefig(filepath)
		return filepath
	except Exception as e:
		print(e)
		return None

def get_all_fields():
	df = pd.read_csv("book_with_grids.csv")
	field_set = set()
	for fields in df["fields"].to_list():
		field_set.update(set(fields.split(",")))
	fields = list(field_set)
	return fields

def generate_heatmap_collection_for_video():
	fields = get_all_fields()
	start_datetime = datetime(2019,1,1)
	end_datetime = datetime(2021,10,1)
	date_after_month = start_datetime + relativedelta(months=1)
	while date_after_month <= end_datetime:
		filepath = generate_linklab_heatmap(start_datetime, date_after_month, fields, export_filepath="./heatmap_collection")
		print("filepath", filepath)
		date_after_month = date_after_month + relativedelta(months=1)


def generate_annual_aggregated_heatmap():
	fields = get_all_fields()
	start_datetime = datetime(2021,1,1)
	end_datetime = datetime(2021,9,28)
	generate_linklab_heatmap(start_datetime, end_datetime, fields, export_filepath="./img")

if __name__ == "__main__":
	generate_annual_aggregated_heatmap()