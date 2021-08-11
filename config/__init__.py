## Ideally, they have one file with the settings for the strat and deployment
## This file would allow them to configure so they can test, deploy and interact with the strategy

BADGER_DEV_MULTISIG = "0x4977110Ed3CD5eC5598e88c8965951a47dd4e738"

WANT = "0xF6a637525402643B0654a54bEAd2Cb9A83C8B498" ## WBTC-USDC
REWARD_TOKEN = "0x831753dd7087cac61ab5644b308642cc1c33dc13" ## QUICK

PROTECTED_TOKENS = [WANT, REWARD_TOKEN]
## Fees in Basis Points
DEFAULT_GOV_PERFORMANCE_FEE = 1000
DEFAULT_PERFORMANCE_FEE = 1000
DEFAULT_WITHDRAWAL_FEE = 50

FEES = [DEFAULT_GOV_PERFORMANCE_FEE, DEFAULT_PERFORMANCE_FEE, DEFAULT_WITHDRAWAL_FEE]

CONTROLLER = "0xc00e71719d1494886942d6277daea20494cf0eec"
KEEPER = "0x46fa8817624eea8052093eab8e3fdf0e2e0443b2"
GUARDIAN = "0xCD3271021e9b35EF862Dd98AFa826b8b5198826d"