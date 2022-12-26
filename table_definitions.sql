CREATE TABLE IF NOT EXISTS info (
    cmdroot text NOT NULL,
    keyword text NOT NULL,
    message_body text NOT NULL,
    mod_version text,
    embed_image text,
    PRIMARY KEY (cmdroot, keyword, mod_version)
);

CREATE TABLE IF NOT EXISTS compat (
    mod_a text NOT NULL,
    mod_b text NOT NULL,
    message_body text NOT NULL,
    mod_a_version text,
    embed_image text,
    PRIMARY KEY (mod_a, mod_b, mod_a_version)
);