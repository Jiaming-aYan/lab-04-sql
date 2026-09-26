DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at DATETIME
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(100),
    body TEXT,
    posted_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username, email, created_at)
VALUES (1, 'alex', 'alex@email.com', '2024-01-10 09:00:00');

INSERT INTO posts (post_id, user_id, title, body, posted_at)
VALUES (1, 1, 'Hello', 'First post', '2024-02-01 12:00:00');
