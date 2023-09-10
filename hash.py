import hashlib
import time
def hashGen():
    seed = str(time.time_ns())

    # Create SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the data
    hash_object.update(seed.encode('utf-8'))

    # Generate the unique hash
    return hash_object.hexdigest()

