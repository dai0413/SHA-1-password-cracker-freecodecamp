import hashlib


def read_and_add_arr(file_name, arr):
    # database is in the top-10000-passwords.txt
    with open(file_name, "rb") as f:
        arr = [line.strip() for line in f]

    return arr


def crack_sha1_hash(hash, use_salts=False):

    # database is in the top-10000-passwords.txt
    passwords_arr = []
    passwords_arr = read_and_add_arr("top-10000-passwords.txt", passwords_arr)

    # if the use_salts is true,
    if use_salts:
        top_salt_passwords = {}
        top_salts = []
        top_salts = read_and_add_arr("known-salts.txt", top_salts)
        for bsalt in top_salts:
            for bpassword in passwords_arr:
                # ソルトを前に付ける（ソルト + パスワード）
                prepended = hashlib.sha1(bsalt + bpassword).hexdigest()
                # ソルトを後ろに付ける（パスワード + ソルト）
                appended = hashlib.sha1(bpassword + bsalt).hexdigest()
                top_salt_passwords[prepended] = bpassword.decode("utf-8")
                top_salt_passwords[appended] = bpassword.decode("utf-8")

        if hash in top_salt_passwords:
            return top_salt_passwords[hash]

    # if the use_salts is false,
    passwords_dict = {}  # [byte] = str
    for p in passwords_arr:
        hash_line = hashlib.sha1(p).hexdigest()
        passwords_dict[hash_line] = p.decode("utf-8")

    if hash in passwords_dict:
        return passwords_dict[hash]

    # if the hash isn't of a password in the database, return "PASSWORD NOT IN DATABASE"
    return "PASSWORD NOT IN DATABASE"


# hash = "b305921a3723cd5d70a375cd21a61e60aabb84ec"
# result = crack_sha1_hash(hash)
# print(hash, "--------", result)

# hash = "c7ab388a5ebefbf4d550652f1eb4d833e5316e3e"
# result = crack_sha1_hash(hash)
# print(hash, "--------", result)

# hash = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
# result = crack_sha1_hash(hash)
# print(hash, "--------", result)

# hash = "53d8b3dc9d39f0184144674e310185e41a87ffd5"
# result = crack_sha1_hash(hash, True)
# print(hash, "--------", result)
