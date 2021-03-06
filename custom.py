import sys
import os
import errno
import multiprocessing
import cdecimal

FROZEN = getattr(sys, 'frozen', False)

peers = {
    '192.241.212.114:8900': {
        'port': 8900,
        'blacklist': 0,
        'lag': 40.0,
        'diffLength': '0',
        'length': 0,
    },
    '69.164.196.239:8900': {
        'port': 8900,
        'blacklist': 0,
        'lag': 0.15,
        'diffLength': '0',
        'length': 0,
    },
}

if FROZEN and sys.platform == 'win32':
    APPDATA = os.getenv('APPDATA', None)
    current_loc = os.path.dirname(sys.executable)
    if APPDATA is not None:
        appdata_path = os.path.join(APPDATA, 'augur')
        try:
            os.makedirs(appdata_path)
        except OSError as exception:
            if os.path.exists(appdata_path) and os.path.isdir(appdata_path):
                pass
            else:
                if exception.errno != errno.EEXIST:
                    raise
        database_name = os.path.join(appdata_path, 'DB')
        log_file = os.path.join(appdata_path, 'log')
        try:
            fp = open(database_name)
        except IOError:
            fp = open(database_name, 'w+')
        try:
            fpl = open(log_file)
        except IOError:
            fpl = open(log_file, 'w+')
        fp.close()
        fpl.close()
    else:
        database_name = os.path.join(current_loc, 'DB')
        log_file = os.path.join(current_loc, 'log')
else:
    current_loc = os.path.dirname(os.path.abspath(__file__))
    database_name = os.path.join(current_loc, 'DB')
    log_file = os.path.join(current_loc, 'log')

port = 8900
api_port = 8899
database_port = 8898

version = "0.0015"

max_key_length = 6**4
total_votecoins = 6**4
block_reward = 10**5
premine = 5 * 10**6
fee = 10 ** 3
propose_decision_fee = 10**5
create_jury_fee = 10**4
jury_vote_fee = 500
reveal_jury_vote_fee = 500
SVD_consensus_fee = 0
buy_shares_fee = 10**5
collect_winnings_reward = 5*10**4

# Lower limits on what the "time" tag in a block can say.
mmm = 100

# Take the median of this many of the blocks.
# How far back in history do we look when we use statistics to guess at
# the current blocktime and difficulty.
history_length = 400

# This constant is selected such that the 50 most recent blocks count for 1/2 the
# total weight.
inflection = cdecimal.Decimal('0.985')
download_many = 50  # Max number of blocks to request from a peer at the same time.
max_download = 58000

#buy_shares_target = '0'*4+'1'+'9'*59
buy_shares_target = '0'*3 + '1' + '9'*60
blocktime = 60
DB = {
    'reward_peers_queue':multiprocessing.Queue(),
    'suggested_blocks': multiprocessing.Queue(),
    'suggested_txs': multiprocessing.Queue(),
    'heart_queue': multiprocessing.Queue(),
}

# seconds_per_week = 604800
# cycle_length = seconds_per_week / blocktime #cycle_length
cycle_length = 40
vote_reveal_length = cycle_length / 10
SVD_length = cycle_length / 40
voting_length = cycle_length - vote_reveal_length-SVD_length
