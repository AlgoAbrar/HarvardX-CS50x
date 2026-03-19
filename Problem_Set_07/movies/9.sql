-- 9. Names of all people who starred in a movie released in 2004, ordered by birth year
SELECT name FROM people
JOIN stars ON stars.person_id = people.id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.year = 2004
ORDER BY people.birth;
