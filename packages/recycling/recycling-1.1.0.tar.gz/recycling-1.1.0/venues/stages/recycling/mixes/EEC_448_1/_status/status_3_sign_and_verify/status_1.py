


'''
	python3 insurance.proc.py "_status/guarantees/status_3_sign_and_verify/status_1.py"
'''


import recycling.mixes.EEC_448_1.private_key.creator as EEC_448_1_private_key_creator
import recycling.mixes.EEC_448_1.public_key.creator as EEC_448_1_public_key_creator
import recycling.mixes.EEC_448_1.sign as sign
import recycling.mixes.EEC_448_1.verify as verify
	
import pathlib
from os.path import dirname, join, normpath
import os


def erase (path):
	try:
		os.remove (path)
	
	except Exception as E:
		pass;
	
	return;

def check_1 ():
	'''
		length 	= 114 
				= 6 * 19 
				= 2 * 3 * 19
	'''
	seeds = [ 
		"4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"5986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8",
		"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",		
		"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
		"123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412341234123412",
		"0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f1e0f",	
		"135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357913579135791357",	
		"2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef2468ef"	
	]
	formats = [ "DER", "PEM" ]
	
	for seed in seeds:
		for format in formats:
			private_key_path = normpath (join (pathlib.Path (__file__).parent.resolve (), "EEC_448_1_private_key")) + "." + format
			public_key_path = normpath (join (pathlib.Path (__file__).parent.resolve (), "EEC_448_1_public_key")) + "." + format
			
			erase (private_key_path)
			erase (public_key_path)
			
			private_key = EEC_448_1_private_key_creator.create (seed, format, private_key_path)
			private_key_instance = private_key ["instance"]
			private_key_string = private_key ["string"]

				
			public_key = EEC_448_1_public_key_creator.create (
				private_key_path = private_key_path,
				public_key_path = public_key_path,
				public_key_format = format
			)
			public_key_instance = public_key ["instance"]
			public_key_string = public_key ["string"]
			
			
			unsigned_bytes = b"{}"
			
			signed = sign.start (
				private_key_path = private_key_path,
				unsigned_bytes = unsigned_bytes
			)
			
			signed_bytes = signed.bytes
			
			verification_status = verify.start (
				public_key_path = public_key_path,
				
				signed_bytes = signed_bytes,
				unsigned_bytes = unsigned_bytes
			)	
			
			assert (verification_status == True), verification_status
					
			erase (private_key_path)
			erase (public_key_path)
			
			

		
checks = {
	"elliptic public and private key generators": check_1
}