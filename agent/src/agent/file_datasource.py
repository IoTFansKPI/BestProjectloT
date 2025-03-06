from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from csv import reader, DictReader

from typing import Iterable
import uuid
import logging


logger = logging.getLogger()
#CustomReader
class CsvReader:
    def __init__(self, filename: str):
        self.file = open(filename, "r")
        self.reader = DictReader(self.file)
        self.lines = self.countLines()
        self.cur_index = 0
        self.cur_data = next(self.reader, None)

    # def nextNotEmpty(self):
    #    while True:
    #        val = next(self.reader, None)
    #        if val or val is None:
    #            return val

    def getCurOrNext(self, i: int):
        if i == self.cur_index:
            return self.cur_data
        elif i == self.cur_index + 1:
            self.cur_data = next(self.reader, None)
            self.cur_index += 1
            return self.cur_data
        else:
            raise ValueError(
                f"Something very bad happened! Cannot get next value from csv! i: {i}, self.cur_index: {self.cur_index}"
            )

    def countLines(self):
        count = 0
        while next(self.reader, None) is not None:
            count += 1
        self.reopen()
        return count

    def reopen(self):
        self.file.seek(0)
        self.reader = DictReader(self.file)
        self.cur_index = 0

    def close(self):
        pass

class FileDatasource:
    def __init__(
        self, accelerometer_filename: str, gps_filename: str, parking_filename: str
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_reader = None
        self.gps_reader = None
        self.parking_reader = None
        self.life_time_count = None #загальна кількість рядків у найбільшому файлі
        self.time_index = None #поточний індекс прочитаних даних
        self.uuid = str(uuid.uuid4()) #унікальний ідентифікатор сесії читання

    def read(self) -> AggregatedData | None:
        if (
            self.accelerometer_reader is None
            or self.gps_reader is None
            or self.parking_reader is None
            or self.life_time_count is None
            or self.time_index is None
        ):
            return None

        while True:
            if self.time_index == self.life_time_count: #якщо досягнуто кінця файлу, перезапускаємо читачі та обнуляємо індекс
                self.accelerometer_reader.reopen()
                self.gps_reader.reopen()
                self.parking_reader.reopen()
                self.time_index = 0

            #обчислюємо індекси для вибірки даних
            p = self.time_index / self.life_time_count + 1e-4

            #отримуємо дані з файлів
            accelerometer_data_new_ind = int(self.accelerometer_reader.lines * p)
            gps_data_new_ind = int(self.gps_reader.lines * p)
            parking_data_new_ind = int(self.parking_reader.lines * p)

            accelerometer_data = self.accelerometer_reader.getCurOrNext(
                accelerometer_data_new_ind
            )
            gps_data = self.gps_reader.getCurOrNext(gps_data_new_ind)
            parking_data = self.parking_reader.getCurOrNext(parking_data_new_ind)

            if accelerometer_data is None or gps_data is None or parking_data is None:
                raise ValueError(
                    "Error with data exporting"
                )

            #логування отриманих даних
            logger.debug(f"Accelerometer data: {accelerometer_data}")
            logger.debug(f"GPS data: {gps_data}")
            logger.debug(f"Parking data: {parking_data}")

            try:
                #парсимо дані акселерометра
                accelerometer_values = [
                    int(accelerometer_data["X"]),
                    int(accelerometer_data["Y"]),
                    int(accelerometer_data["Z"]),
                ]

                #парсимо дані GPS
                gps_values = [
                    float(gps_data["longitude"]),
                    float(gps_data["latitude"]),
                ]

                #парсимо дані паркування
                empty_count = int(parking_data["empty_count"])
                gps_parking = Gps(
                    float(parking_data["longitude"]), float(parking_data["latitude"])
                )
            except (ValueError, IndexError):
                logger.error(
                    f"Failed to parse data, Accelerometer data: {accelerometer_data}, GPS data: {gps_data}, Parking data: {parking_data}"
                )
                continue

            #створюємо об'єкти класів
            accelerometer = Accelerometer(*accelerometer_values)
            parking = Parking(empty_count, gps_parking)
            gps = Gps(*gps_values)

            #отримуємо поточний часовий штамп
            timestamp = datetime.now()

            self.time_index += 1

            return AggregatedData(accelerometer, gps, parking, timestamp, self.uuid)

    def startReading(self, *args, **kwargs):
        if self.accelerometer_reader is not None or self.gps_reader is not None:
            raise ValueError("Files already opened.")

        #відкриваємо файли для читання
        self.accelerometer_reader = CvsReader(self.accelerometer_filename)
        self.gps_reader = CvsReader(self.gps_filename)
        self.parking_reader = CvsReader(self.parking_filename)

        self.life_time_count = max(
            self.accelerometer_reader.lines,
            self.gps_reader.lines,
            self.parking_reader.lines,
        )

        self.time_index = 0

    def stopReading(self, *args, **kwargs):
        if (
            self.accelerometer_reader is None
            or self.gps_reader is None
            or self.parking_reader is None
        ):
            raise ValueError("Error opening file")
        #закриваємо всі файли
        self.accelerometer_reader.close()
        self.gps_reader.close()
        self.parking_reader.close()

