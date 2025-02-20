import os


def generate_otp():
	return str(int.from_bytes(os.urandom(5), byteorder="big") % 900000 + 100000)
