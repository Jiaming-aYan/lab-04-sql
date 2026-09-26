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

INSERT INTO users (user_id, username, email, created_at) VALUES (1, 'alex', 'alex@email.com', '2024-01-10 09:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (2, 'blake', 'blake@email.com', '2024-01-15 10:30:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (3, 'casey', 'casey@email.com', '2024-02-02 14:15:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (4, 'drew', 'drew@email.com', '2024-02-20 08:45:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (5, 'eden', 'eden@email.com', '2024-03-05 16:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (6, 'frank', 'frank@email.com', '2024-03-18 11:20:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (7, 'gray', 'gray@email.com', '2024-04-01 13:10:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (8, 'harper', 'harper@email.com', '2024-04-22 09:40:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (9, 'indigo', 'indigo@email.com', '2024-05-09 15:25:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (10, 'jordan', 'jordan@email.com', '2024-05-30 12:05:00');

INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (1, 1, 'Hello', 'First post from Alex', '2024-02-01 12:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (2, 2, 'Morning', 'Blake checking in', '2024-03-01 08:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (3, 3, 'Notes', 'Casey wrote some notes', '2024-04-12 18:30:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (4, 4, 'Update', 'Drew has an update', '2024-05-20 10:15:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (5, 5, 'Summer', 'Eden starts summer', '2024-06-02 09:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (6, 6, 'Trip', 'Frank went on a trip', '2024-06-15 17:45:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (7, 7, 'Recipe', 'Gray shared a recipe', '2024-07-04 13:20:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (8, 8, 'Photo', 'Harper posted a photo', '2024-07-21 19:05:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (9, 9, 'Review', 'Indigo reviewed a book', '2024-08-08 11:30:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (10, 10, 'Goodbye', 'Jordan says goodbye', '2024-08-25 16:40:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (11, 1, 'Again', 'Alex posts a second time', '2024-09-01 10:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (12, 5, 'Later', 'Eden posts again', '2024-09-10 14:10:00');
