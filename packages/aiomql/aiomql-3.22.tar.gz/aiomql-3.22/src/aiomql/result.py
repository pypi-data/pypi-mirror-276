import csv
import json
from logging import getLogger
from typing import Iterable, Literal

from .core import Config
from .core.models import OrderSendResult

logger = getLogger(__name__)


class Result:
    """A base class for handling trade results and strategy parameters for record keeping and reference purpose.
    The data property must be implemented in the subclass

    Attributes:
        config (Config): The configuration object
        name: Any desired name for the result file object
    """
    config: Config

    def __init__(self, result: OrderSendResult, parameters: dict = None, name: str = ''):
        """
        Prepare result data
        Args:
            result:
            parameters:
            name:
        """
        self.config = Config()
        self.parameters = parameters or {}
        self.result = result
        self.name = name or parameters.get('name', 'Trades')

    def get_data(self) -> dict:
        res = self.result.get_dict(exclude={'retcode', 'comment', 'retcode_external', 'request_id', 'request'})
        return self.parameters | res | {'actual_profit': 0, 'closed': False, 'win': False}

    async def save(self, *, trade_record_mode: Literal['csv', 'json'] = None):
        """Record trade results as a csv or json file
        Args:
            trade_record_mode (Literal['csv'|'json']): Mode of saving trade records
        """
        trade_record_mode = trade_record_mode or self.config.trade_record_mode
        if trade_record_mode == 'csv':
            await self.to_csv()
        else:
            await self.to_json()

    async def to_csv(self):
        """Record trade results and associated parameters as a csv file
        """
        try:
            data = self.get_data()
            file = self.config.records_dir / f"{self.name}.csv"
            file.touch(exist_ok=True) if not file.exists() else ...
            reader: Iterable[dict] = csv.DictReader(file.open('r', newline=''))
            rows: list[dict] = []
            headers = set()
            [(rows.append(row), headers.update(row.keys())) for row in reader]
            rows.append(data)
            headers.update(data.keys())
            writer = csv.DictWriter(file.open('w', newline=''), fieldnames=headers, restval=None,
                                    extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        except Exception as err:
            logger.error(f'Unable to save to csv: {err}')

    @staticmethod
    def serialize(value) -> str:
        """Serialize the trade records and strategy parameters
        """
        try:
            return str(value)
        except (ValueError, TypeError) as _:
            return ""

    async def to_json(self):
        """Save trades and strategy parameters in a json file
        """
        try:
            file = self.config.records_dir / f"{self.name}.json"
            data = self.get_data()
            exists = file.touch(exist_ok=True) if not file.exists() else True
            if not exists:
                json.dump([], file.open('w'))
            with file.open('r') as fh:
                rows = json.load(fh)
            rows.append(data)
            with file.open('w') as fh:
                json.dump(rows, fh, indent=2, skipkeys=True, default=self.serialize)
        except Exception as err:
            logger.error(f"Unable to save as json file: {err}")
