

'''
	from recycling.mixes.brainpool_1.private_key.build import build_private_key
	private_key = build_private_key ({
		"seed": ""
	})
'''


# Generate a Brainpool curve key

'''

#
#	https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#cryptography.hazmat.primitives.asymmetric.ec.BrainpoolP512R1
#
#

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

def create_private_key ():
	private_key = ec.generate_private_key (
		ec.BrainpoolP512R1 (),
		default_backend ()
	)
'''	

from fastecdsa import keys, curve
	
def build_private_key (packet):
	seed = packet ["seed"]

	private_key = keys.gen_private_key (
		curve.brainpoolP512r1,
		randfunc = lambda * pos, ** keys : bytes.fromhex (seed)
	)
	
	return private_key