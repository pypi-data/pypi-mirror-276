from .normalizer import normalize
from .interpolator import get_color_interpolator, rgb_to_hex

def value_to_color(values, color_bases):
    """Normalize the values and map them to a color gradient based on provided color bases."""
    min_value = min(values)
    max_value = max(values)
    interpolator = get_color_interpolator(color_bases)

    color_data = []
    for value in values:
        normalized_value = normalize(value, min_value, max_value)
        rgb_color = interpolator(normalized_value)
        hex_color = rgb_to_hex(rgb_color[:3])  # Convert only the RGB part, ignore alpha
        color_data.append({
            'value': value,
            'color': hex_color
        })

    return color_data
