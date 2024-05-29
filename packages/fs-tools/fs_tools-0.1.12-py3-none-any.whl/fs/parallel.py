from typing import TextIO, Iterable, Sequence, Callable
import multiprocessing
import os

def chunked_read(file: TextIO, chunk_size: int = 10000) -> Iterable[Sequence[str]]:
  while True:
    lines = file.readlines(chunk_size)
    if not lines:
      break
    yield lines

def parallel_apply(
  input: TextIO, output: TextIO,
  func: Callable[[Sequence[str]], Iterable[str]],
  *, chunk_size: int = 10000, num_procs: int | None = None
):
  pool = multiprocessing.Pool(processes=num_procs or os.cpu_count())
  for chunk in chunked_read(input, chunk_size):
    results = pool.map(func, [chunk])
    for result in results:
      output.writelines(result)
