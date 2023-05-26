import time
from datetime import datetime

# assuming the earliest timestamp is from 01/01/2000
earliest_time = datetime(2000, 1, 1)
# subtract the epoch, convert to seconds, and multiply by 1000 to get milliseconds
time_start = int((earliest_time - datetime(1970, 1, 1)).total_seconds() * 1000)


def is_positive_int32(num):
    # assuming the device id is a positive integer from 0 to 2^31 -1
    return 0 <= num <= 2**31 - 1


def is_valid_timestamp(timestamp_ms):
    # valid timestamp is between the earliest time defined above and the current time, can not be in the future.
    current_time_ms = int(time.time()) * 1000
    return time_start <= timestamp_ms <= current_time_ms


def is_float64(num):
    # float64 should always have decimal places, up to 16.
    if '.' in str(num):
        parts = str(num).split('.')
        return 1 <= len(parts[1]) <= 16
    else:
        return False


