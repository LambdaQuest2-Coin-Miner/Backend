import hashlib
import requests
import sys
import json

from time import time, sleep
from datetime import timedelta

#api endpoints
BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

def proof_of_work(last_proof, difficulty):
    start_time = time()
    proof = 1
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    
    end_time = time()
    elapsed = end_time - start_time
    duration = str(timedelta(seconds=elapsed))
    print(f"Proof {proof} created in {duration}")

    return proof


def valid_proof(last_proof, proof, difficulty):
    # Use difficulty to calculate number of leading zeroes
    guess_hash = hashlib.sha256(str(proof).encode()).hexdigest()
    prev_proof_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()

    return prev_proof_hash[:difficulty] == guess_hash[:difficulty]

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
        get_last_proof = requests.get(url=f"{BASE_URL}/last_proof", headers=headers)
        # Extract proof and difficulty attributes from the last proof data
        try:
            last_proof = get_last_proof.json()
            print(f"Received last_proof {last_proof}")
            proof = last_proof['proof']
            difficulty = last_proof['difficulty']
            cooldown = last_proof['cooldown'] + 1
        except ValueError:
            print("Error: Non-json response")
            print(f"Response returned: {get_last_proof}")
            break
        # Generate new proof of work
        print("Start generating proof")
        sleep(cooldown)
        new_proof = proof_of_work(proof, difficulty)
        sleep(cooldown)
        # Submit generated proof to the /mine endpoint
        post_data = {"proof": new_proof}
        submit_new_proof = requests.post(
            url=f"{BASE_URL}/mine", headers=headers, json=post_data)

        try:
            mined_coin = submit_new_proof.json()
        except ValueError:
            print("Error: Non-json response")
            print(f"Response returned: {submit_new_proof}")

        # Read response message
        # IF successful increment number of coins mined
        if mined_coin['messages'] == 'New Block Forged':
            sleep(cooldown)
            get_coin_balance = requests.get(url=f"{BASE_URL}/get_balance", headers=headers)
            coins += 1
        # If unsuccessful repeat the process
        else:
            print(f"Failed mining attempt: {mined_coin['messages']}")
            sleep(cooldown)