""" Chart rendering technology / library """
from enum import Enum


class ChartRenderTechnology(Enum):
  """
  Chart Alignment
  """
  CANVAS_JS = 'CANVAS_JS'
  GRAPHIC = 'GRAPHIC'
  SYNCFUSION_FLUTTER_CHARTS = 'SYNCFUSION_FLUTTER_CHARTS'

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'ChartRenderTechnology.{self.value}'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
