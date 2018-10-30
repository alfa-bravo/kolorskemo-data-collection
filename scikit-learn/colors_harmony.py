import colorsys


class Color:
    def __init__(self, RGB):
        self.RGB = RGB


def Normalize(Value, Min, Max):
    Output = Value
    if Value > Max:
        Output = Max
    elif Value < Min:
        Output = Min
    return Output


def monochromatic(ColorInput):
    # Convert RGB (base 256) to HSV (between 0 and 1)
    ColorInput.HSV = list(
        colorsys.rgb_to_hsv(ColorInput.RGB[0] / 255, ColorInput.RGB[1] / 255, ColorInput.RGB[2] / 255))

    # Generate 10 monochromatic colors with a step of 5%
    increment = [0, 0.05, 0.10]
    result = []
    output = []

    for x in increment:
        for y in increment:
            result.append(list(map(lambda x: Normalize(round(x * 255), 0, 255),
                                   colorsys.hsv_to_rgb(ColorInput.HSV[0], Normalize(ColorInput.HSV[1], 0, 100) + x,
                                                       Normalize(ColorInput.HSV[2] + y, 0, 100)))))
            result.append(list(map(lambda x: Normalize(round(x * 255), 0, 255),
                                   colorsys.hsv_to_rgb(ColorInput.HSV[0], Normalize(ColorInput.HSV[1], 0, 100) - x,
                                                       Normalize(ColorInput.HSV[2] - y, 0, 100)))))
    [output.append(x) for x in result if x not in output]
    return output
