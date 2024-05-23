import rsa

class Signature:
    def GenerateKeys(self):
        (pubkey, privkey) = rsa.newkeys(512)
        pub = '{} {}'.format(pubkey.e, pubkey.n)
        pri = '{} {} {} {} {}'.format(pubkey.n, pubkey.e, privkey.d, privkey.p, privkey.q)
        return (pub, pri)
    def sign(self, data, private_key):
        n, e, d, p, q = map(int, private_key.split())
        pri = rsa.PrivateKey(n=n, e=e, d=d, p=p, q=q)
        signature = rsa.sign(data, pri, 'SHA-256')
        return signature
    def check(self, data, cert, public_key):
        e, n = map(int, public_key.split())
        pub = rsa.PublicKey(e=e, n=n)
        try:
            rsa.verify(data, cert, pub)
            return True
        except:
            return False
    
