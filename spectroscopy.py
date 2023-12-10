# These are the only packages you are allowed import:
import os
import glob
import math
import matplotlib.pyplot as plt

# "pass" indicates an empty block of code,
# remove it when filling in the functions.


def my_name() -> str:
    return "Rachel Bozadjian"


def parse_spectrum(filename: str) -> list[float]:
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
        spectrum_flattened_list = [element for sublist in spectrum_no_first_element for element in sublist]
        
        # remove "\n" character
        spectrum_no_newline = [element.replace("\n", "") for element in spectrum_flattened_list]
        
        # remove last list element which is a space from the split function used
        spectrum_no_newline.pop()
        
        # turn list elements from strings to floats
        spectrum_list = [float(element) for element in spectrum_no_newline]
        
    return spectrum_list


def remove_invalid_transmittance(spectrum: list[float]) -> list[float]:
    # remove out of range transmittance measurements if greater than 100 or less than 0
    new_spectrum = [val for val in spectrum if 0 < val < 100]
    return new_spectrum


def absorbance(x: float) -> float:
    # beer lambert law to calculate absorbance from transmittance
    absorbance_value = -math.log10(x / 100)
    return absorbance_value


def absorbance_list(spectrum: list[float]) -> list[float]:
    # initialize list to append absorbance values to
    absorbance_values_list = []
    
    # loop through transmittance spectrum list and call absorbance function on each value
    # append value to absorbance_values_list
    for val in spectrum:
        absorbance_values_list.append(absorbance(val))
        
    return absorbance_values_list


def plot_transmittance(spectrum: list[float]) -> None:
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
    plt.savefig("pure_antibiotic_infrared_spectrum.png", dpi = 200)
    
    return


def center_list(x: list[float]) -> list[float]:
    # subtract mean of entire absorbance list from each element and save in new list
    centered_data = [element - sum(x)/len(x) for element in x]
    
    return centered_data


def correlation(x: list[float], y: list[float]) -> float:
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
    
    return corr


if __name__ == "__main__":
    # print name
    # print(my_name())
    
    # change directory to access .dat files
    # MIGHT NEED TO CHANGE THIS TO JUST DESKTOP
    directory_path = "/Users/rachelbozadjian/Desktop/intro_bioinformatics/assignment2/assignmentFiles/data"
    file_path = os.chdir(directory_path)

    # file name list
    #spec_file_name_list = glob.glob('*')

    # file path list
    spec_file_path_list = glob.glob(os.path.join(directory_path, '*'))
    
    # pure spectrum, absorbance, and centered data   
    pure_spectrum = parse_spectrum(spec_file_path_list[0])
    pure_spectrum_abs = absorbance_list(pure_spectrum)
    pure_spectrum_centered = center_list(pure_spectrum_abs)
    
    # plot the transmittance of the pure antibiotic infrared spectrum
    # plot_transmittance(pure_spectrum)

    # test case with one spectrum
    spectrum = parse_spectrum(spec_file_path_list[91])
    cat = remove_invalid_transmittance(spectrum)
    print(spectrum)
    print(cat)
    # spectrum_abs = absorbance_list(spectrum)
    # spectrum_centered = center_list(spectrum_abs)
    
    
    # print(len(spectrum_centered))
    # print(len(pure_spectrum_centered))
    
    # for i in spec_file_path_list[1:]:
    #     spectrum = parse_spectrum(i)
        # spectrum_abs = absorbance_list(spectrum)
        # spectrum_centered = center_list(spectrum_abs)
        # corrs = correlation(spectrum_centered, pure_spectrum_centered)
        
    
# change file path
# add docstrings
# remove spectrum_abs with out_of_range values
# make a 'table' of the correlations with their associated sample name