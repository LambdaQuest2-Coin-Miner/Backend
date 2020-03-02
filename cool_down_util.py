# Dynamically calculate cooldown points based on player and room factors
def cooldown_calc(player_cd, room_cd, errors, messages=[]):
    total_cooldown = float(player_cd) + float(room_cd)
    if len(errors) > 0:
        total_cooldown += parse_cooldown_message(errors)
    if len(messages) > 0:
        total_cooldown += parse_cooldown_message(messages)

    print(f"Total cooldown points: {total_cooldown}")
    return total_cooldown


# Extract cooldown numbers from errors and messages
def parse_cooldown_message(messages):
    total = 0

    if messages is not None or len(messages) > 0:
        is_cooldown = [
            cooldown_str for cooldown_str in messages if "CD" in cooldown_str]

        if len(is_cooldown) > 0:
            extract_cooldown_pts = [int(char)
                                    for char in is_cooldown[0] if char.isdigit()][0]
            print(f"Extra cooldown points extracted: {extract_cooldown_pts}")
            total += extract_cooldown_pts

        else:
            print(f"No extra cooldown points")

    return total
