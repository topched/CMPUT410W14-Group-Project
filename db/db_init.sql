CREATE TABLE users (
    user_id VARCHAR(36) NOT NULL, 
    display_name VARCHAR(128) NOT NULL, -- username
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128), -- Probably best to separate these, since it isn't that difficult
    last_name VARCHAR(128),
    git_url VARCHAR(256), -- So we can pull their public stream
    email VARCHAR(256) NOT NULL,
    default_post_visibility INT,
    PRIMARY KEY(user_id)
 -- This way, we can set a default privacy level for each post
);

CREATE TABLE posts (
    post_id VARCHAR(36) NOT NULL PRIMARY KEY,
    author VARCHAR(36) NOT NULL,
    content LONGTEXT,
    content_type INT, -- Whether the content is text, HTML, or markdown. 
    visibility INT,
    FOREIGN KEY (author) REFERENCES users(user_id)
);

CREATE TABLE comments (
    comment_id VARCHAR(36) NOT NULL PRIMARY KEY,
    parent_post VARCHAR(36) NOT NULL,
    author VARCHAR(36) NOT NULL,
    content LONGTEXT,
    FOREIGN KEY (author) REFERENCES users(user_id),
    FOREIGN KEY (parent_post) REFERENCES posts(post_id)
);

CREATE TABLE friends (
    request_id VARCHAR(36) NOT NULL PRIMARY KEY,
    requester VARCHAR(36) NOT NULL,
    friend VARCHAR(36) NOT NULL,
    accepted TINYINT(1), -- A boolean to represent whether the status of the request is still "follow" or has been accepted
    FOREIGN KEY (requester) REFERENCES users(user_id),
    FOREIGN KEY (friend) REFERENCES users(user_id)
);

CREATE TABLE images (
    image_id VARCHAR(36) NOT NULL PRIMARY KEY,
    author VARCHAR(36) NOT NULL,
    filename VARCHAR(128) NOT NULL, -- I assume we'll probably store them in a folder somewhere
    visibility INT,
    FOREIGN KEY (author) REFERENCES users(user_id)
);
