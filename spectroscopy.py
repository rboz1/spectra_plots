'''imported modules'''
import os
import glob
import math
import matplotlib.pyplot as plt

def my_name() -> str:
    '''function printing my name.'''
    return "Rachel Bozadjian"


def parse_spectrum(filename: str) -> list[float]:
    '''function that parses a standard .dat file 
    from a spectrophotometer and returns its transmittance values in a list.'''
    with open(filename, 'r+', encoding="utf-8") as f:
        # read file lines into a list
        spectrum_line_list = f.readlines()
        
        # remove header lines from list
        spectrum_list_no_header = spectrum_line_list[11:]
        
        # split list of file lines based on space character to make a nested list
        spectrum_nested_list = [sublist.split(" ") for sublist in spectrum_list_no_header]
        
        # loop through nested list and remove first element which is the wavenumber
        spectrum_no_first_element = [sublist[1:] for sublist in spectrum_nested_list]
                
        # flatten nested list
        spectrum_flat_list = [elem for sublist in spectrum_no_first_element for elem in sublist]
        
        # remove "\n" character
        spectrum_no_newline = [element.replace("\n", "") for element in spectrum_flat_list]
        
        # remove last list element which is a space from the split function used
        spectrum_no_newline.pop()
        
        # turn list elements from strings to floats
        spectrum_list = [float(element) for element in spectrum_no_newline]
        
    return spectrum_list


def remove_invalid_transmittance(spectrum: list[float]) -> list[float]:
    '''function that removes out of range 
    transmittance measurements if greater than 100 or less than 0.'''
    spectrum_in_range = [val for val in spectrum if 0 < val < 100]
    return spectrum_in_range


def absorbance(x: float) -> float:
    '''function that uses the beer lambert law to calculate absorbance from transmittance.'''
    absorbance_value = -math.log10(x / 100)
    return absorbance_value


def absorbance_list(spectrum: list[float]) -> list[float]:
    '''function that returns a list of absorbance values 
    calculated from each element in a list of transmittance values.'''
    # initialize list to append absorbance values to
    absorbance_values_list = []
    
    # loop through transmittance spectrum list and call absorbance function on each value
    # append value to absorbance_values_list
    for val in spectrum:
        absorbance_values_list.append(absorbance(val))
        
    return absorbance_values_list


def plot_transmittance(spectrum: list[float]) -> None:
    '''function that plots the transmittance spectrum 
    of a sample according against known wavenumbers.'''
    # list of infrared wavenumbers
    wavenumber = list(range(400, 4024, 24))
    
    # average every 6 measurements per wavenumber and save to new list
    average_spectrum = [sum(spectrum[i:i+6]) / 6 for i in range(0, len(spectrum), 6)]

    # plot average_spectrum ~ wavenumber
    plt.plot(wavenumber, average_spectrum)
    
    # invert x-axis (wavenumber)
    plt.gca().invert_xaxis()
    
    # plot labels and title
    plt.xlabel("Wavenumber (cm-1)")
    plt.ylabel("Transmittance")
    plt.title("Pure Antibiotic Infrared Spectrum")
    
    # plot x and y limits
    plt.xlim(4100,350)
    plt.ylim(10,110)
        
    # save figure locally
    plt.savefig("../pure_antibiotic_infrared_spectrum.png", dpi = 200)
    
    plt.close()
    
    return average_spectrum


def center_list(x: list[float]) -> list[float]:
    '''function that subtracts the mean of entire 
    absorbance list from each element and returns in new list.'''
    centered_data = [element - sum(x)/len(x) for element in x]
    
    return centered_data


def correlation(x: list[float], y: list[float]) -> float:
    '''function that calculates the correlation coefficient 
    between 2 lists of centered absorbance value data.'''
    # only run if absorbance lists are the same length
    if len(x) == len(y):
        # numerator: sum of x and y
        xy = [x * y for x, y in zip(x, y)]
        xy_sum = sum(xy)
        
        # denominator: sum of x squared
        x_sq = [element**2 for element in x]
        sum_x_sq = sum(x_sq)
        
        # denominator: sum of y squared
        y_sq = [element**2 for element in y]
        sum_y_sq = sum(y_sq)
        
        # pearson correlation coefficient
        corr = xy_sum / math.sqrt(sum_x_sq * sum_y_sq)
    
        return round(corr, 4)


def make_correlation_dict(corr_list: list[float], file_name_list: list[str]) -> dict:
    '''function that takes a list of file_names as keys 
    and a list of correlation coefficients as valuesand puts them in a dictionary. '''
    # remove '.dat' from file name strings
    file_names_formatted = [name.replace(".dat", "") for name in file_name_list]
    
    # combine into dictionary with corr_list
    corr_dict = {file_name: corr for file_name, corr in zip(file_names_formatted, corr_list)}
    
    return corr_dict


def make_correlation_table(all_corr_dict: dict, label: str) -> None:
    '''function that prints out a dictionary's keys 
    and values in 2 columns side by side.'''
    print("SAMPLE_NAME " + label)
    for key, value in all_corr_dict.items():
        print(f"{key}: {value}")
    return


def analyze_correlation(corr_dict: dict) -> None:
    '''function that calculates the mean correlation coefficient 
    and standard deviation then returns them as a value in a dictionary.'''
    # list of all strains
    strain_list = ["strainA", "strainB", "strainC", "strainD", "strainE", "strainF"]
    corr_mean_stdv = {}
    
    # find mean and standard deviation for each strain and save in a dict
    for strain in strain_list:
        corr_combined = [val for key, val in corr_dict.items() if strain in key and val is not None]
        corr_mean = round(sum(corr_combined) / len(corr_combined), 4)
        corr_stdv1 = [(x - corr_mean) ** 2 for x in corr_combined]
        corr_stdv2 = sum(corr_stdv1) / (len(corr_combined) - 1)
        corr_stdv3 = round(corr_stdv2 ** 0.5, 4)
        
        corr_mean_stdv[strain] = [corr_mean, corr_stdv3]
    
    return corr_mean_stdv


def plot_all_samples(pure_spectrum: list[float], spec_file_name_list: list[str], spec_file_path_list: list[str], strain_name: str) -> None:
    '''function that plots all samples for each strain (strainB, strainC, strainF) 
    each against pure antibiotic transmittance spectrum.'''       
    transmittance_vals = []
    
    # list of infrared wavenumbers
    wavenumber = list(range(400, 4024, 24))
    
    # get indices of all transmittance values for each strain sample
    strain_indices = [index for index, item in enumerate(spec_file_name_list) if strain_name in item]
    
    # parse spectrum for each sample
    for ind in strain_indices:
        transmittance_vals.append(parse_spectrum(spec_file_path_list[ind]))
     
    # take average of transmittance values and plot against pure_spectrum       
    for val_list in transmittance_vals:
        average_spectrum = [sum(val_list[i:i+6]) / 6 for i in range(0, len(val_list), 6)]
        plt.plot(wavenumber, average_spectrum, color = "#D3D3D3", linewidth = 1)
        plt.plot(wavenumber, pure_spectrum, color = "purple", linewidth = 1)
        
        # plot labels and title
        plt.xlabel("Wavenumber (cm-1)")
        plt.ylabel("Transmittance")
        plt.title(strain_name + " and Pure Antibiotic")
        
        # invert x-axis
        plt.gca().invert_xaxis()
    
    # legend
    custom_legend = [
        plt.Line2D([0], [0], color='purple', lw=2, label='Pure Antibiotic'),  
        plt.Line2D([0], [0], color='#D3D3D3', lw=2, label= strain_name + ' Sample Data')      
    ]
    
    # plot x and y limits
    plt.xlim(4100,350)
    plt.ylim(10,110)
    
    plt.legend(handles=custom_legend)
    plt.savefig(f"../{strain_name}.png", dpi=200)
    plt.close()
    
    return


def plot_transmittance_strainF_sample10(spectrum: list[float]) -> None:
    '''function that plots the transmittance spectrum 
    of a sample according against known wavenumbers.'''
    # list of infrared wavenumbers
    wavenumber = list(range(400, 4024, 24))
    
    # average every 6 measurements per wavenumber and save to new list
    average_spectrum = [sum(spectrum[i:i+6]) / 6 for i in range(0, len(spectrum), 6)]

    # plot average_spectrum ~ wavenumber
    plt.plot(wavenumber, average_spectrum)
    
    # invert x-axis (wavenumber)
    plt.gca().invert_xaxis()
    
    # plot labels and title
    plt.xlabel("Wavenumber (cm-1)")
    plt.ylabel("Transmittance")
    plt.title("strainF_sample10 Infrared Spectrum")
    
    # plot x and y limits
    plt.xlim(4100,350)
    plt.ylim(10,110)
        
    # save figure locally
    plt.savefig("../strainF_sample10.png", dpi = 200)
    
    plt.close()
    
    return

if __name__ == "__main__":
    # print name
    print(my_name())
    
    # change directory to access .dat files
    home_directory = os.path.expanduser("~")
    RELATIVE_PATH = "Desktop/assignmentFiles/data"
    DIRECTORY_PATH = os.path.join(home_directory, RELATIVE_PATH)
    file_path = os.chdir(DIRECTORY_PATH)

    # file name list
    spec_file_name_list = sorted(glob.glob('*'))
    
    # file path list
    spec_file_path_list = sorted(glob.glob(os.path.join(DIRECTORY_PATH, '*')))
    
    # pure spectrum, absorbance, and centered data   
    pure_spectrum = parse_spectrum(spec_file_path_list[0])
    pure_spectrum_abs = absorbance_list(pure_spectrum)
    pure_spectrum_centered = center_list(pure_spectrum_abs)
    
    # plot the transmittance of the pure antibiotic infrared spectrum and save pure transmittance averages
    pure_spectrum_averages = plot_transmittance(pure_spectrum)

    # sample spectra, absorbance, centered data, and correlations
    corrs = []
    
    for i in spec_file_path_list[1:]:
        spectrum = parse_spectrum(i)
        spectrum_outliers_removed = remove_invalid_transmittance(spectrum)
        spectrum_abs = absorbance_list(spectrum_outliers_removed)
        spectrum_centered = center_list(spectrum_abs)
        corrs.append(correlation(spectrum_centered, pure_spectrum_centered))
        
    all_corr_dict = make_correlation_dict(corrs, spec_file_name_list[1:])
 
    # make a table with the sample names and their corresponding correlation coefficients
    make_correlation_table(all_corr_dict, "CORRELATION_COEFFICIENT")
    
    # get mean correlation coefficients and standard deviations for each strain
    corr_mean_stddev = analyze_correlation(all_corr_dict)
    
    # make table with sample names and corresponding mean corr coeffs and standard dev
    make_correlation_table(corr_mean_stddev, "MEAN_CORRELATION_COEFFICIENT, STANDARD_DEVIATION")
    
    # plot for strainF_sample10
    strainF_sample10 = spec_file_name_list.index("strainF_sample10.dat")
    strainF_sample10_spectrum = parse_spectrum(spec_file_path_list[strainF_sample10])
    plot_transmittance_strainF_sample10(strainF_sample10_spectrum)

    # plot all samples for strains B, C, and F and antibiotic
    plot_all_samples(pure_spectrum_averages, spec_file_name_list, spec_file_path_list, "strainB")
    plot_all_samples(pure_spectrum_averages, spec_file_name_list, spec_file_path_list, "strainC")
    plot_all_samples(pure_spectrum_averages, spec_file_name_list, spec_file_path_list, "strainF")