"""CLI quiz correcter.

The quiz needs a solutions file and 1 or multiple answer files. All
text based.

The tool checks if the answers match up with the solution and prints
a small summary of the results.

Examples:
    `cqc ./examples/solution.txt ./examples/player*.txt`

    `Score board:
        Player 1        10
        Player 2        4
    `
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Optional, Union, TypeAlias
import rich_click as click
import logging

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.logging import RichHandler
from rich.align import Align

from . import __VERSION__
from .colorbox import get_color

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
_LOGGER = logging.getLogger()

AnswerTypes = Union[float, str]
GameRecord = dict[int, AnswerTypes]


def _value_parser(v: str, constructor: Callable) -> Optional[AnswerTypes]:
	try:
		return constructor(v.rstrip('\n'))
	except ValueError:
		# _LOGGER.debug("%s Not a %s", v, constructor.__name__)
		pass
	return None


def _parser(v: str) -> AnswerTypes:
	"""Parse `char` or `int` values on each line"""
	ret = _value_parser(v, float)
	if ret:
		return ret
	ret = _value_parser(v, str)
	if ret:
		return ret
	raise ValueError('Could not parse value')


def read_file(solution: Path) -> GameRecord:
	"""Parse solution file"""
	with open(solution, 'r', encoding='utf-8') as f:
		raw = f.readlines()

	return {idx: _parser(v) for idx, v in enumerate(raw)}


def get_score(solution: GameRecord, answers: dict[str, GameRecord]) -> dict[str, float]:
	scores = {player: 0.0 for player in answers.keys()}
	_LOGGER.info(f'{scores}')

	for idx, ans in solution.items():
		for p in answers:
			_LOGGER.debug(f'{p=} q={idx} a={ans} pa={answers[p][idx]}')
			if idx == 1:
				if not isinstance(answers[p][idx], float) and not isinstance(
					ans, float
				):
					raise ValueError('IDX 2 should be float')
				_diff = abs(float(ans) - float(answers[p][idx]))
				if _diff < 3:
					scores[p] += 1
				elif _diff < 6:
					scores[p] += 0.5
				else:
					continue

			if ans == answers[p][idx]:
				scores[p] += 1

	return scores


def _sort_by_value(d: dict[str, float], reverse=True) -> dict[str, float]:
	return dict(sorted(d.items(), key=lambda x: x[1], reverse=reverse))


def color_value(v: float) -> Text:
	color, _ = get_color(int(v))
	return Text(str(v), Style(color=color, bgcolor=None))


def build_rich_renderable(scores: dict[str, float]):
	table = Table(title=Text('🎉 Quiz score board 🎉', no_wrap=True, overflow='ignore'))

	table.add_column('Name', justify='left', style='cyan', no_wrap=True)
	table.add_column('Score', style='magenta')

	for player, score in scores.items():
		score_text = color_value(score)
		table.add_row(player, score_text)

	return table


@click.command()
@click.argument('solution', type=click.Path(exists=True))
@click.argument('answer', type=click.Path(exists=True), nargs=-1)
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.version_option(__VERSION__, prog_name='cqc')
def main(solution: Path, answer: Iterable[Path], debug: bool):
	"""CLI entry point"""
	if debug:
		logging.basicConfig(level=logging.DEBUG)
	_LOGGER.debug('%s', solution)
	_LOGGER.debug('%s', answer)

	ans = (Path(a) for a in answer)

	answers = {_a.stem: read_file(_a) for _a in ans}
	scr = _sort_by_value(get_score(read_file(solution), answers))
	_LOGGER.debug(scr)

	table = Align.center(build_rich_renderable(scr), vertical='middle')
	console = Console()
	console.print(table)


if __name__ == '__main__':
	main()
