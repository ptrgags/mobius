import random
import math

def render_tag(tag_name, close_tag, **kwargs):
    """
    Render a XML tag.
    """
    attrs = ['{}="{}"'.format(key, val) for key, val in kwargs.items()]
    attr_str = " ".join(attrs)
    if close_tag:
        return "<{} {} />".format(tag_name, attr_str)
    else:
        return "<{} {}>".format(tag_name, attr_str)

def prefix_lines(prefix, lines):
    """
    Prefix each string in a list with a string
    """
    return ["{}{}".format(prefix, line) for line in lines]

class Palette(object):
    """
    Class that represents a 256-color RGB palette for Apophysis/Chaotica
    """
    TOTAL_COLORS = 256
    COLORS_PER_ROW = 8
    ROWS = TOTAL_COLORS // COLORS_PER_ROW
    def __init__(self, colors):
        if len(colors) != self.TOTAL_COLORS:
            raise ValueError(
                'Palettes must have {} colors'.format(self.TOTAL_COLORS))
        self.colors = colors

    def color_row(self, i):
        """
        Format a single row of colors in hexadecimal
        """
        start = i * self.COLORS_PER_ROW
        end = (i + 1) * self.COLORS_PER_ROW
        colors = self.colors[start:end]
        color_strs = [
            "{:02X}{:02X}{:02X}".format(r, g, b)
            for r, g, b in colors]
        return "".join(color_strs)

    @property
    def lines(self):
        """
        Format the palette tag including its 256 colors
        """
        start_tag = render_tag(
            'palette',
            close_tag=False,
            count=self.TOTAL_COLORS,
            format="RGB")
        color_lines = [self.color_row(i) for i in range(self.ROWS)]
        end_tag = "</palette>"
        return [start_tag] + prefix_lines('   ', color_lines) + [end_tag]

    @classmethod
    def rand_component(cls, t, c, d):
        """
        Compute a single color in a random cosine palette
        """
        a = 0.5
        b = 0.5
        val = a + b * math.cos(2.0 * math.pi * (c * t + d))
        return int(val * 255)

    @classmethod
    def random(cls):
        """
        Return a random cosine palette
        """
        pal = []

        red_c = random.randint(0, 5)
        red_d = random.random()
        green_c = random.randint(0, 5)
        green_d = random.random()
        blue_c = random.randint(0, 5)
        blue_d = random.random()
        for i in range(cls.TOTAL_COLORS):
            t = i / cls.TOTAL_COLORS
            r = cls.rand_component(t, red_c, red_d)
            g = cls.rand_component(t, green_c, green_d)
            b = cls.rand_component(t, blue_c, blue_d)
            pal.append((r, g, b))
        return cls(pal)

class Flame(object):
    """
    Class that represents a single flame fractal for
    Apophysis/Chaotica
    """
    def __init__(self, name, xforms, palette=None, zoom=1.0, size="1500 2100"):
        self.name = name
        self.xforms = xforms
        self.palette = palette or Palette.random()
        self.xforms = xforms
        self.size = size
        self.zoom = zoom

    @property
    def xform_lines(self):
        """
        Render each xforms to XML
        """
        N = len(self.xforms)
        return [
            # Evenly space the color along the palette
            xform.to_flame(i/(N + 1)) 
            for i, xform in enumerate(self.xforms)]

    @property
    def lines(self):
        """
        Render an XML <flame> tag
        """
        start_tag = render_tag(
            'flame',
            close_tag=False,
            name=self.name,
            version="Apophysis 7x Version 15C.9",
            size=self.size,
            center="0 0",
            scale=200,
            oversample=1,
            filter=0.2,
            quality=1,
            background="0 0 0",
            brightness=4,
            gamma=4,
            gamma_threshold=0.01,
            estimator_radius=9,
            estimator_minimum=0,
            estimator_curve=0.4,
            enable_de=0,
            plugins="",
            new_linear=1,
            curves=(
                "0 0 1 0 0 1 1 1 1 1 1 1 0 0 1 0 0 1 1 1 1 1 1 1 0 0 1 0 "
                "0 1 1 1 1 1 1 1 0 0 1 0 0 1 1 1 1 1 1 1"))

        # Format the neededtransformations
        xform_lines = prefix_lines('   ', self.xform_lines)

        # Final transform for quick zooming
        zoom_tag = render_tag(
            'finalxform',
            close_tag=True,
            color='0',
            symmetry='1',
            linear=self.zoom,
            coefs="1 0 0 1 0 0")

        # Palettes and the end tag
        palette_lines = prefix_lines('   ', self.palette.lines)
        end_tag = '</flame>'

        # Combine all the lines into one big list
        return (
            [start_tag] + xform_lines + [zoom_tag] + palette_lines + [end_tag])

class FlamePack(object):
    """
    Object that generates an apophysis .flame file
    """
    def __init__(self, name, flames):
        self.name = name
        self.flames = flames

    def __str__(self):
        flame_lines = sum([flame.lines for flame in self.flames], [])
        return (
            '<flames name={pack_name}>\n'
            '{flames}\n'
            '</flames>\n'
        ).format(pack_name=self.name, flames="\n".join(flame_lines))

    def save(self, fname):
        with open(fname, 'w') as f:
            f.write(str(self))
