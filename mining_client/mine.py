import hashlib
import requests
import sys
import json

from time import time, sleep
from datetime import timedelta
from traversal_util import get_player_status, get_room_info
from cool_down_util import cooldown_calc

# api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
PLAYER_STATUS = get_player_status()


def proof_of_work(last_proof, difficulty):
    start_time = time()
    block_string = json.dumps(last_proof, sort_keys=True)
    proof = 1
    while valid_proof(block_string, proof, difficulty) is False:
        proof += 1
    end_time = time()
    elapsed = end_time - start_time
    duration = str(timedelta(seconds=elapsed))
    print(f"Proof {proof} created in {duration}")
    return proof


def valid_proof(last_proof, proof, difficulty):
    # Use difficulty to calculate number of leading zeroes
    guess_hash = f'{last_proof}{proof}'.encode()
    prev_proof_hash = hashlib.sha256(guess_hash).hexdigest()
    # print(f"previous proof {prev_proof_hash}")
    return prev_proof_hash[:difficulty] == '0'.zfill(difficulty)
    # return prev_proof_hash[:difficulty] == '011010'
# def proof_of_work(last_proof, difficulty):
#     start_time = time()
#     proof = 1
#     while valid_proof(last_proof, proof, difficulty) is False:
#         proof += 1

#     end_time = time()
#     elapsed = end_time - start_time
#     duration = str(timedelta(seconds=elapsed))
#     print(f"Proof {proof} created in {duration}")

#     return proof


# def valid_proof(last_proof, proof, difficulty):
#     # Use difficulty to calculate number of leading zeroes
#     guess_hash = hashlib.sha256(str(proof).encode()).hexdigest()
#     prev_proof_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()

#     # return prev_proof_hash[:difficulty] == guess_hash[:difficulty]
#     return prev_proof_hash[:difficulty] == "0" * difficulty
if __name__ == '__main__':
    coins = 0
    # Load Game Token
    f = open("my_token.txt", "r")
    game_token = f.read()
    print(f"Game token is {game_token}")
    f.close()
    headers = {'Authorization': f'Token {game_token}'}

    # Run until 1 coin is mined
    while coins < 1:
        # Get the last valid proof from the /last_proof endpoint
        get_last_proof = requests.get(
            url=f"{BASE_URL}/last_proof", headers=headers)
        # Extract proof and difficulty attributes from the last proof data
        try:
            last_proof = get_last_proof.json()
            print(f"Received last_proof {last_proof}")
            proof = last_proof['proof']
            difficulty = last_proof['difficulty']
        except ValueError:
            print("Error: Non-json response")
            print(f"Response returned: {get_last_proof}")
            break
        # Generate new proof of work
        print("Start generating proof")
        new_proof = proof_of_work(proof, difficulty)
        print('after new proof')
        # Submit generated proof to the /mine endpoint
        post_data = {"proof": new_proof}
        print('after post data')
        submit_new_proof = requests.post(
            url=f"{BASE_URL}/mine/", headers=headers, json=post_data)
        print('after submit_new_proof')
        try:
            mined_coin = submit_new_proof.json()

            # Read response message
            # IF successful increment number of coins mined
            print(f"mined_coin {mined_coin}")
            if len(mined_coin['errors']) > 0:
                print(
                    f"Failed mining attempt: {mined_coin['errors']}, retrying...")
                cooldown = cooldown_calc(
                    PLAYER_STATUS['cooldown'], mined_coin['cooldown'], mined_coin['errors'])
                sleep(cooldown)
            else:
                print(f"Successful mining attempt:\n {mined_coin}")
                # Get Lambda coin balance
                get_coin_balance = requests.get(
                    url=f"{BASE_URL}/get_balance/", headers=headers)
                coin_balance = get_coin_balance.json()
                print(f"Current Lambda Coin Balance is: \n {coin_balance}")
                coins += 1

        except ValueError:
            error = submit_new_proof
            print(
                f"Response returned: {error} \n server overload, retrying...")
