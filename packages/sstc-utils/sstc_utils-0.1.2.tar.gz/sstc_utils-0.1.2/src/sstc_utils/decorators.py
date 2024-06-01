# SITES Spectral Thematic Center
# Mantainer: @jobelund


def rearrange_by_spectral_band(bands:list =  ['RED', 'GRE', 'BLUE', 'NIR', 'REG'] )->dict:
    """
    The function acts as a decorator. It modifies the output of the decorated function to reorganize file paths into categories based on their spectral band. 
    The spectral bands are specified in the bands parameter, and the function will create a key for each band in the output dictionary.
    The function will only categorize file paths into the bands specified in the bands parameter. Any file type not listed in bands will be ignored in the output.
   
    Args:
        bands (optional): A list of strings representing the spectral bands. Defaults to `['RED', 'GRE', 'BLUE', 'NIR', 'REG']`.

    Returns:
        A dictionary where each key corresponds to a spectral band (e.g., `'RED', 'GRE', 'BLUE', 'NIR', 'REG'`). The value for each key is another dictionary 
        containing the original key-value pairs that correspond to that specific spectral band.
        
    Note:
        The function assumes that the file type (spectral band) is always the last part of the file name before the extension (e.g., `FILENAME_RED.TIF`). 
        If your file naming convention is different, you may need to adjust the logic in the wrapper function of the decorator.
        
    Usage:
        To use this decorator, simply define it above a function that returns a dictionary of file paths. The file names in the keys of this dictionary should contain
        the spectral band as the last part before the file extension.
        
        >>> @rearrange_by_spectral_band(bands=['RED', 'GRE', 'BLUE', 'NIR', 'REG'])
        >>> def get_file_paths(*args, **kwargs):
        >>>     # Function implementation that returns a dictionary of file paths    
    """
    def decorator(func):
        """ Decorator function to `rearrange_by_spectral_band`.

        Args:
            func: A function that is expected to output a dictionary. This dictionary should have keys formatted as `FILENAME_BAND.TIF` and values as full file paths.
        
        """
        def wrapper(*args, **kwargs):
            # Call the original function
            original_output = func(*args, **kwargs)

            # Initialize the new dictionary structure
            # {'RED': {}, 'GRE': {}, 'BLU': {}, 'NIR': {}, 'REG': {}}
            new_output = {band : {} for band in bands }   

            # Iterate over items in the original output
            for key, value in original_output.items():
                # Determine the file type based on the key
                file_type = key.split('_')[-1].split('.')[0]

                # Add the key-value pair to the corresponding file type in the new dictionary
                if file_type in new_output:
                    new_output[file_type][key] = value

            return new_output
        return wrapper
    return decorator