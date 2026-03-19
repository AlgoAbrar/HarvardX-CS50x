-- Keep a log of any SQL queries you execute as you solve the mystery.

-- size of the reports
SELECT COUNT(*) FROM crime_scene_reports;

-- entire reports
SELECT * FROM crime_scene_reports;

-- reports on July 28, 2021 and on Humphrey Street
SELECT * FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND year = 2021;

-- find bakery
SELECT * FROM interviews WHERE transcript LIKE '%bakery%';

-- bakery
SELECT * FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2021
AND hour = 10 AND minute <= 25
AND activity = 'exit';

-- ATM
SELECT * FROM atm_transactions
WHERE day = 28 AND month = 7 AND year = 2021
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- cross owners
SELECT people.*, logs.hour, logs.minute FROM people
JOIN (
    SELECT license_plate, hour, minute
    FROM bakery_security_logs
    WHERE day = 28 AND month = 7 AND year = 2021
    AND hour = 10 AND minute <= 25
    AND activity = 'exit'
) AS logs ON people.license_plate = logs.license_plate
WHERE people.id IN (
    SELECT person_id FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE day = 28 AND month = 7 AND year = 2021
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
)
ORDER BY logs.minute;

-- phonecall
SELECT * FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2021
AND caller is '(367) 555-5533'; -- Bruce
AND caller is '(389) 555-5198'; -- Luca
AND caller is '(829) 555-5269'; -- Iman
AND caller is '(770) 555-1861'; -- Diana

-- SUSPECT
SELECT people.*, logs.hour, logs.minute FROM people
JOIN (
    SELECT license_plate, hour, minute FROM bakery_security_logs
    WHERE day = 28 AND month = 7 AND year = 2021
    AND hour = 10 AND minute <= 25
    AND activity = 'exit'
) AS logs ON people.license_plate = logs.license_plate
WHERE people.id IN (
    SELECT person_id FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE day = 28 AND month = 7 AND year = 2021
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
)
AND people.phone_number IN (
    SELECT caller FROM phone_calls
    WHERE day = 28 AND month = 7 AND year = 2021
)
ORDER BY logs.minute;

-- Fiftyville airport info
SELECT * FROM airports WHERE city = 'Fiftyville';

-- Find flights
SELECT * FROM flights
WHERE day = 29 AND month = 7 AND year = 2021
AND origin_airport_id = 8
ORDER BY hour
LIMIT 1;

-- find passgengers in flights
SELECT people.name, passengers.seat FROM people
JOIN (
    SELECT passport_number, seat FROM passengers
    WHERE flight_id IN (
        SELECT id
        FROM flights
        WHERE day = 29 AND month = 7 AND year = 2021
        AND origin_airport_id = 8
        AND hour = 8
    )
) AS passengers ON people.passport_number = passengers.passport_number;


-- match past calls
SELECT name FROM people
WHERE phone_number IN (
    SELECT receiver FROM phone_calls
    WHERE day = 28 AND month = 7 AND year = 2021
    AND duration < 60
    AND caller is '(367) 555-5533' -- Bruce
);


-- find the city
SELECT city FROM airports
WHERE id IN (
    SELECT destination_airport_id FROM flights
    WHERE day = 29 AND month = 7 AND year = 2021
    AND origin_airport_id = 8
    ORDER BY hour
    LIMIT 1
);

