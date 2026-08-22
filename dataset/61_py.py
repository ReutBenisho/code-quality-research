class MinMax_s:

  def __init__(self, min: int, max: int):
    self.min = min
    self.max = max


class SnippetManager:

  def GetMinAndMaxSnippetLength(self, snippets: list[str]) -> MinMax_s:
    min_len = 100
    max_len = 0
    # ... inner logic to calculate lengths (can assume it's correct)
    minMax = MinMax_s(min_len, max_len)
    return minMax