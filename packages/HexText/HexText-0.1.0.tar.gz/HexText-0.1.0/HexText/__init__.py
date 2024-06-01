# hextext/hextext.py

class HexText:
    def __call__(self, text, color=None, gradient=None):
        if color:
            return self.apply_solid_color(text, color)
        elif gradient:
            return self.apply_gradient(text, gradient)
        else:
            return text

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_ansi(self, rgb_color):
        return ';'.join(map(str, (38, 2, *rgb_color)))

    def apply_solid_color(self, text, color):
        rgb_color = self.hex_to_rgb(color)
        ansi_code = self.rgb_to_ansi(rgb_color)
        return f"\033[{ansi_code}m{text}\033[0m"

    def apply_gradient(self, text, gradient):
        if isinstance(gradient, str):
            gradient = [gradient]

        num_colors = len(gradient)
        if num_colors == 1:
            return self.apply_solid_color(text, gradient[0])

        text_length = len(text)
        gradient_text = ""
        segment_length = max(1, text_length // (num_colors - 1))

        for i, char in enumerate(text):
            segment_index = min(i // segment_length, num_colors - 2)
            start_color = self.hex_to_rgb(gradient[segment_index])
            end_color = self.hex_to_rgb(gradient[segment_index + 1])

            ratio = (i % segment_length) / segment_length
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            ansi_code = self.rgb_to_ansi((r, g, b))

            gradient_text += f"\033[{ansi_code}m{char}\033[0m"

        return gradient_text
