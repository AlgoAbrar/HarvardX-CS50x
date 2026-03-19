import cs50

while True:
    change_owed = cs50.get_float("Change owed: ")

    if change_owed > 0:
        remaining_cents = round(change_owed * 100)
        total_coins = 0

        # Coin values in cents
        QUARTER = 25
        DIME = 10
        NICKEL = 5
        PENNY = 1

        total_coins += remaining_cents // QUARTER
        remaining_cents %= QUARTER

        total_coins += remaining_cents // DIME
        remaining_cents %= DIME

        total_coins += remaining_cents // NICKEL
        remaining_cents %= NICKEL

        total_coins += remaining_cents // PENNY

        print(total_coins)
        break
