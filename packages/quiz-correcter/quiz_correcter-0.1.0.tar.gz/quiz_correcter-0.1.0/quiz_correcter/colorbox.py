import colorsys

from rich.color import Color
from rich.text import Text
from rich.style import Style
from rich import print


def make_colors() -> dict[int, tuple[Color, Color]]:
	y = 3
	offset = 10
	max_width = 108
	map = {}
	for x in range(0, 40, 10):
		h = x / max_width
		l = 0.1 + ((y / 5) * 0.7)
		r1, g1, b1 = colorsys.hls_to_rgb(h, l, 1.0)
		r2, g2, b2 = colorsys.hls_to_rgb(h, l + 0.7 / 10, 1.0)
		bgcolor = Color.from_rgb(r1 * 255, g1 * 255, b1 * 255)
		color = Color.from_rgb(r2 * 255, g2 * 255, b2 * 255)
		map[x + offset] = (color, bgcolor)
	return map


COLOR_MAP = make_colors()


def get_color(i: int) -> tuple[Color, Color]:
	for j in COLOR_MAP.keys():
		if i < j:
			return COLOR_MAP[j]
	raise ValueError


if __name__ == '__main__':
	for i in range(40):
		color, bgcolor = get_color(i)
		print(Text(str(i), Style(color=color, bgcolor=None)))
