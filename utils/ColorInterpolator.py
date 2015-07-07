class ColorInterpolator(object):

    def __init__(self, start_hex="#00C911", end_hex="#E63030", mid_hex = "#FFFFFF"):
        self.start_hex = start_hex
        self.end_hex = end_hex
        self.mid_hex = mid_hex
        self.color_array = self.create_gradient_array()

    def get_color(self, cost):
        '''
        :param cost: Number between 0 and 1 that represents the cost of a route
        :return: RGB color that represents the cost
        '''

        index = int(cost * 100)
        return self.hex_to_RGB(self.color_array[index])

    def create_gradient_array(self):
        ''' Constructs array with gradient, passing by the mid color defined '''
        res = []
        left_gradient = self.linear_gradient(self.start_hex, self.mid_hex, 50)['hex']
        right_gradient = self.linear_gradient(self.mid_hex, self.end_hex, 51)['hex']
        res.extend(left_gradient)
        res.extend(right_gradient)
        return res

    def hex_to_RGB(self, hex):
        ''' "#FFFFFF" -> [255,255,255] '''
        # Pass 16 to the integer function for change of base
        return [int(hex[i:i+2], 16) for i in range(1,6,2)]


    def RGB_to_hex(self, RGB):
        ''' [255,255,255] -> "#FFFFFF" '''
        # Components need to be integers for hex to make sense
        RGB = [int(x) for x in RGB]
        return "#"+"".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB])

    def color_dict(self, gradient):
        ''' Takes in a list of RGB sub-lists and returns dictionary of
        colors in RGB and hex form for use in a graphing function
        defined later on '''
        return {"hex":[self.RGB_to_hex(RGB) for RGB in gradient], "r":[RGB[0] for RGB in gradient], "g":[RGB[1] for RGB in gradient], "b":[RGB[2] for RGB in gradient]}

    def linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
        ''' returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF") '''
        # Starting and ending colors in RGB form
        s = self.hex_to_RGB(start_hex)
        f = self.hex_to_RGB(finish_hex)
        # Initilize a list of the output colors with the starting color
        RGB_list = [s]
        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [ int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
            # Add it to our list of output colors
            RGB_list.append(curr_vector)
        return self.color_dict(RGB_list)


