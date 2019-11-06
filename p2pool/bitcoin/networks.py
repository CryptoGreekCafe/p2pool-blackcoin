import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

@defer.inlineCallbacks
def get_subsidy(bitcoind, target):
    res = yield bitcoind.rpc_getblock(target)

    defer.returnValue(res)

nets = dict(
    denarius=math.Object(
        P2P_PREFIX='faf2efb4'.decode('hex'),
        P2P_PORT=33369,
        ADDRESS_VERSION=30,
        RPC_PORT=32369,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'denariusaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: 3000000*100000000,
        BLOCK_PERIOD=30, # s
        SYMBOL='D',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Denarius') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Denarius/') if platform.system() == 'Darwin' else os.path.expanduser('~/.denarius'), 'denarius.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://www.coinexplorer.net/D/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://www.coinexplorer.net/D/address/',
        TX_EXPLORER_URL_PREFIX='https://www.coinexplorer.net/D/transaction/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.01e8,
    ),
    denarius_testnet=math.Object(
        P2P_PREFIX='cdf2c0ef'.decode('hex'),
        P2P_PORT=33369,
        ADDRESS_VERSION=18,
        RPC_PORT=32368,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'denariuscoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda bitcoind, target: 10000*100000000,
        BLOCK_PERIOD=30, # s
        SYMBOL='D',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'BlackCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/BlackCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.blackcoin'), 'blackcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://testnet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://testnet/address/',
        TX_EXPLORER_URL_PREFIX='http://testnet/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.01e8,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
