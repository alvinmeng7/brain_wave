from pyOpenBCI import OpenBCICyton

def print_raw(sample):
    print(sample.channels_data)

board = OpenBCICyton(daisy=False)

board.start_stream(print_raw)