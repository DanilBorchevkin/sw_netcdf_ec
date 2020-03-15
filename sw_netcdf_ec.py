# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:55:17 2019

@author: Danil Borchevkin
"""

#import netCDF4 as nc # netcdf module
import xarray as xr
import glob

def process_file(filepath, min_alt, max_alt):
    dataset = xr.open_dataset(filepath)

    alt_list = list()
    for alt in dataset.coords['MSL_alt'].data:
        if (alt >= min_alt) and (alt <= max_alt):
            alt_list.append(alt)

    return_list = list()
    for alt in alt_list:
        dataset_local = dataset.sel(MSL_alt=alt)
        
        return_list.append(
            [
                alt, 
                dataset_local.data_vars['ELEC_dens'].data, 
                dataset_local.data_vars['GEO_lat'].data,
                dataset_local.data_vars['GEO_lon'].data
            ]
        )
    
    return return_list

def save_to_ascii_file(data_list, out_filepath, header=[]):
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def main():
    # get all files
    files = glob.glob("./samples/2018.295/*.*")

    # get from each file data - level, electron density, lat, long
    extracted_data = []
    for filepath in files:
        # Append data from each processed file
        # Second argument is a minimum altitude
        # Third parameter is a maximum altitude
        data_from_file = process_file(filepath, 195, 200)

        for data in data_from_file:
            extracted_data.append(data)
    
    save_to_ascii_file(extracted_data, "./out.txt")

if __name__ == "__main__":
    main()