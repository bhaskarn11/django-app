import hmac

def verify_payment_signanture(order_id, payment_id, signature, key):
    key = bytes(key, 'utf-8')
    mssg = bytes(f"{order_id}|{payment_id}", 'ascii')
    hash = hmac.digest(key, mssg, 'sha256').hex()
    matched = hmac.compare_digest(hash, signature)
    return matched
