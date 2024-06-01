import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def get_color_interpolator(colors):
    """Create a color interpolator from the provided base colors."""
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
    def interpolator(value):
        return cmap(value)
    return interpolator

def rgb_to_hex(rgb):
    """Convert RGB color to hex format."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
