import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence, Coroutine, Callable
from logging import getLogger

from .strategy import Strategy

logger = getLogger(__name__)


class Executor:
    """Executor class for running multiple strategies on multiple symbols concurrently.

    Attributes:
        executor (ThreadPoolExecutor): The executor object.
        workers (list): List of strategies.
        coroutines (dict[Coroutine, dict]): A dictionary of coroutines to run in the executor
        functions (dict[Callable, dict]): A dictionary of functions to run in the executor
    """

    def __init__(self):
        self.executor = ThreadPoolExecutor
        self.workers: list[type(Strategy)] = []
        self.coroutines: dict[Coroutine | Callable: dict] = {}
        self.functions: dict[Callable: dict] = {}

    def add_function(self, func: Callable, kwargs: dict):
        self.functions[func] = kwargs

    def add_coroutine(self, coro: Coroutine, kwargs: dict):
        self.coroutines[coro] = kwargs

    def add_workers(self, strategies: Sequence[type(Strategy)]):
        """Add multiple strategies at once

        Args:
            strategies (Sequence[Strategy]): A sequence of strategies.
        """
        self.workers.extend(strategies)

    def remove_workers(self, *, symbols: set):
        """Removes any worker running on a symbol not successfully initialized."""
        self.workers = [worker for worker in self.workers if worker.symbol in symbols]

    def add_worker(self, strategy: type(Strategy)):
        """Add a strategy instance to the list of workers

        Args:
            strategy (Strategy): A strategy object
        """
        self.workers.append(strategy)

    @staticmethod
    def trade(strategy: type(Strategy)):
        """Wraps the coroutine trade method of each strategy with 'asyncio.run'.

        Args:
            strategy (Strategy): A strategy object
        """
        asyncio.run(strategy.trade())

    def run(self, func, kwargs: dict):
        """
        Run a coroutine function

        Args:
            func: The coroutine. A variadic function.
            kwargs: A dictionary of keyword arguments for the function
        """
        try:
            asyncio.run(func(**kwargs))
        except Exception as err:
            logger.error(f'Error: {err}. Unable to run function')

    async def execute(self, workers: int = 5):
        """Run the strategies with a threadpool executor.

        Args:
            workers: Number of workers to use in executor pool. Defaults to 5.

        Notes:
            No matter the number specified, the executor will always use a minimum of 5 workers.
        """
        workers_ = sum([len(self.workers), len(self.functions), len(self.coroutines)])
        workers = max(workers, workers_)
        loop = asyncio.get_running_loop()
        with self.executor(max_workers=workers) as executor:
            [loop.run_in_executor(executor, self.trade, worker) for worker in self.workers]
            [loop.run_in_executor(executor, self.run, coro, kwargs) for coro, kwargs in self.coroutines.items()]
            [loop.run_in_executor(executor, func, kwargs) for func, kwargs in self.functions.items()]
