from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from csv import DictReader
import logging
from config import DATA_DIR

logger = logging.getLogger()


class CvsReader:
    def __init__(self, filename: str):
        self.filepath = DATA_DIR + '/' + filename
        self.file = open(self.filepath, 'r')
        self.reader = DictReader(self.file)
        self.data = list(self.reader)
        self.lines = len(self.data)
        self.cur_index = 0

    def getCurOrNext(self, i: int):
        if i < self.lines:
            self.cur_index = i
            return self.data[self.cur_index]
        else:
            raise ValueError(f'Index out of range! i: {i}, total lines: {self.lines}')

    def reopen(self):
        self.cur_index = 0

    def close(self):
        self.file.close()


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_reader = None
        self.gps_reader = None
        self.life_time_count = None

    def read(self) -> AggregatedData | None:
        if not all([self.accelerometer_reader, self.gps_reader, self.life_time_count]):
            return None

        if self.time_index >= self.life_time_count:
            self.accelerometer_reader.reopen()
            self.gps_reader.reopen()
            self.time_index = 0

        p = self.time_index / self.life_time_count + 1e-4
        accelerometer_data_new_ind = int(self.accelerometer_reader.lines * p)
        gps_data_new_ind = int(self.gps_reader.lines * p)

        try:
            accelerometer_data = self.accelerometer_reader.getCurOrNext(
                accelerometer_data_new_ind
            )
            gps_data = self.gps_reader.getCurOrNext(gps_data_new_ind)

            accelerometer_values = [
                int(accelerometer_data['x']),
                int(accelerometer_data['y']),
                int(accelerometer_data['z']),
            ]
            gps_values = [float(gps_data['longitude']), float(gps_data['latitude'])]

            accelerometer = Accelerometer(*accelerometer_values)
            gps = Gps(*gps_values)
            timestamp = datetime.now()

            self.time_index += 1
            return AggregatedData(accelerometer, gps, timestamp)

        except (ValueError, IndexError) as e:
            logger.error(f'Failed to parse data: {e}')
            print(f'Failed to parse data: {e}')
            return None

    def startReading(self):
        if self.accelerometer_reader or self.gps_reader:
            raise ValueError('Files already opened.')

        self.accelerometer_reader = CvsReader(self.accelerometer_filename)
        self.gps_reader = CvsReader(self.gps_filename)
        self.life_time_count = max(
            self.accelerometer_reader.lines, self.gps_reader.lines
        )
        self.time_index = 0

    def stopReading(self):
        if not self.accelerometer_reader or not self.gps_reader:
            raise ValueError('Error opening file')

        self.accelerometer_reader.close()
        self.gps_reader.close()
