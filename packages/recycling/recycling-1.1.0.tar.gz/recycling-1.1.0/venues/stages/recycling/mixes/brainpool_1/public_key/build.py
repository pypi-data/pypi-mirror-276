






'''
	from recycling.mixes.brainpool_1.public_key.build import build_public_key
	private_key = build_private_key ({
		"private_key": ""
	})
'''

from fastecdsa import keys, curve

def build_public_key (packet):
	private_key = packet ["private_key"]
	public_key = keys.get_public_key (
		private_key,
		curve.brainpoolP512r1
	)

	return public_key