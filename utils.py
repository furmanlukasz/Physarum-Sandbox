import numba
import numpy as np

# This is a helper function that can be used to interpolate between two RGB colors (must be moved outside of the class to work with Numba)
@numba.jit(nopython=True)
def interpolate_color(color1, color2, factor):
    """ Interpolates between two RGB colors. """
    result = np.empty(3, dtype=np.int32)  # Use NumPy array for fixed-size sequence
    for i in range(3):  # RGB channels
        result[i] = int(color1[i] + (color2[i] - color1[i]) * factor)
    return result  # Return as NumPy array which is supported by Numba

@numba.jit(nopython=True)
def color_from_value(value, max_trail_value):
    """
    Determine the color of a cell based on its value using the 'viridis' colormap.
    """
    # Define the 'viridis' colormap segments
    viridis = np.array([
        (68, 1, 84),  # Dark purple
        (58, 82, 139),  # Purple to blue
        (32, 144, 140),  # Blue to green
        (94, 201, 97),  # Green
        (253, 231, 36)  # Yellow
    ], dtype=np.int32)

    # Normalize the value to be within 0 and 1
    normalized_value = min(max(value / max_trail_value, 0), 1)  # Clamp between 0 and 1
    
    # Determine the segment of the colormap to use based on the normalized value
    if normalized_value < 0.25:
        color = interpolate_color(viridis[0], viridis[1], normalized_value / 0.25)
    elif normalized_value < 0.5:
        color = interpolate_color(viridis[1], viridis[2], (normalized_value - 0.25) / 0.25)
    elif normalized_value < 0.75:
        color = interpolate_color(viridis[2], viridis[3], (normalized_value - 0.5) / 0.25)
    else:
        color = interpolate_color(viridis[3], viridis[4], (normalized_value - 0.75) / 0.25)
    return color


