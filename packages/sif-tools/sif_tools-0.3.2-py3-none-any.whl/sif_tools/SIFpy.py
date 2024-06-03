import os
import numpy as np
from scipy.interpolate import interp1d

from .utils import MATH, FILE

@staticmethod
def sif2array(target:str, reduce_noise:bool=False, window:str=None):
    """
    Convert SIF (Spectral Image Format) files to a NumPy array.

    This function processes SIF files from a given target (file or directory),
    optionally reduces noise, and slices the data to a specified window.

    Parameters:
    ----------
    target : str
        Path to a SIF file or a directory containing SIF files.
    reduce_noise : bool, optional
        If True, applies noise reduction to the data (default is False).
    window : str, optional
        Specify the window for slicing the data. The window slices around the center wavelength:
        - 'reduced': slices 10% of entries from each end
        - 'narrow' : slices 25% of entries from each end
        - 'pinched'    : slices 33% of entries from each end

    Returns:
    -------
    numpy.ndarray
        A NumPy array containing the combined spectral data from the SIF file(s).
        Each row corresponds to a pair of wavelength and count.

    Examples:
    ---------
    To use the full data without slicing:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window=None)

    To slice the first 100 data points:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window='0:100')

    To slice from the 50th to the 200th data point:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window='50:200')
    """
    # Check if the target is a file or a directory
    if os.path.isfile(target):
        paths = [target]
    else:
        paths = FILE.extract_files_from_folder(target)

    data_list = []

    for path in paths:
        data, _ = FILE.parse(path)

        if window:
            data = MATH.slice_window(data, window=window)

        wavelengths, counts = data[:, 0], data[:, 1]

        if reduce_noise:
            wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)

        data_list.append(np.column_stack((wavelengths, counts)))

    # Combine all data arrays into one ndarray
    if len(data_list) == 1:
        return data_list[0]
    else:
        return np.vstack(data_list)

@staticmethod
def hyperspectrum(directory:str, background:str, reduce_noise=True, window='pinched'):
    """
    Generates a heatmap from hyperspectral data.

    Args:
        directory (str): Directory containing spectrum files.
        background (str): Filename of the background spectrum file.
        reduce_noise (bool, optional): Whether to reduce noise in the data. Defaults to True.
        window (str, optional): The window of data to be sliced for plotting. Defaults to 'pinched'.

    Returns:
        np.ndarray: A 2D array representing the heatmap data.
    """
    
    # check if directory is directory
    if os.path.isfile(directory):
        raise Exception("'directory' parameter has to be a directory, not a file.")
    else:
        files = FILE.extract_files_from_folder(directory)
    
    # access and treat background image
    files.remove(background) # remove background file from list of files
    # Parse and process the background file
    background_data, _ = FILE.parse(os.path.join(directory, background))
    background_data = MATH.slice_window(background_data, window=window)
    bg_wavelengths, bg_counts = background_data[:, 0], background_data[:, 1]
    if reduce_noise: # remove spikes using gradient method with 3-sigma threshold.
        bg_wavelengths, bg_counts = MATH.gradient_n_sigma(bg_wavelengths, bg_counts)

    positions = FILE.extract_positions(files)

    pixels = []
    for file in files:
        data, _ = FILE.parse(os.path.join(directory, file))

        data = MATH.slice_window(data, window=window)
        wavelengths, counts = data[:, 0], data[:, 1]

        if reduce_noise:
            wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)
        
        # Interpolate background counts to match the wavelengths of the current data
        bg_interp = interp1d(bg_wavelengths, bg_counts, kind='linear', bounds_error=False, fill_value=0)
        bg_counts_interpolated = bg_interp(wavelengths)

        # Ensure counts do not go below zero after background subtraction
        adjusted_counts = np.maximum(counts - bg_counts_interpolated, 0)
        
        pixels.append(int(np.sum(adjusted_counts)))
    
    normalized_pixels = MATH.normalize_array(np.array(pixels))
    # Create a dictionary to hold the pixel values by position
    counts_by_position = {(float(pos[1]), float(pos[2])): normalized_pixels for pos, normalized_pixels in zip(positions, normalized_pixels)}

    # Determine the grid size
    max_x = int(max(float(pos[1]) for pos in positions)) + 1
    max_y = int(max(float(pos[2]) for pos in positions)) + 1
    heatmap_data = np.zeros((max_y, max_x))

    # Fill the heatmap data based on the positions
    for pos, count in counts_by_position.items():
        x, y = int(pos[0]), int(pos[1])
        heatmap_data[y, x] = count

    return heatmap_data
