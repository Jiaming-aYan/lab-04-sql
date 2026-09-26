SELECT users.username, posts.title, posts.posted_at
FROM users
JOIN posts ON users.user_id = posts.user_id
WHERE posts.posted_at >= '2024-06-01';
