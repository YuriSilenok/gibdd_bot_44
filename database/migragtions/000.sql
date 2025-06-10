PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM forwardmessage;

DROP TABLE forwardmessage;

CREATE TABLE forwardmessage (
    id              INTEGER  NOT NULL
                             PRIMARY KEY,
    user_message_id INTEGER  NOT NULL,
    to_user_id      INTEGER  NOT NULL,
    at_created      DATETIME NOT NULL,
    tg_message_id   INTEGER  NOT NULL,
    is_delete       INTEGER  NOT NULL,
    ban_count       INTEGER  DEFAULT (0) 
                             NOT NULL,
    ban_until       DATETIME NOT NULL,
    FOREIGN KEY (
        user_message_id
    )
    REFERENCES usermessage (id) ON DELETE CASCADE
                                ON UPDATE CASCADE,
    FOREIGN KEY (
        to_user_id
    )
    REFERENCES user (id) ON DELETE CASCADE
                         ON UPDATE CASCADE
);

INSERT INTO forwardmessage (
                               id,
                               user_message_id,
                               to_user_id,
                               at_created,
                               tg_message_id,
                               is_delete
                           )
                           SELECT id,
                                  user_message_id,
                                  to_user_id,
                                  at_created,
                                  tg_message_id,
                                  is_delete
                             FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

CREATE INDEX forwardmessage_to_user_id ON forwardmessage (
    "to_user_id"
);

CREATE INDEX forwardmessage_user_message_id ON forwardmessage (
    "user_message_id"
);

PRAGMA foreign_keys = 1;
