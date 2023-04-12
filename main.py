import rsa


def generateKeys(length):
    (public_key, private_key) = rsa.newkeys(length)
    with open('keys/publicKey.txt', 'wb') as p:
        p.write(public_key.save_pkcs1('PEM'))
    with open('keys/privateKey.txt', 'wb') as p:
        p.write(private_key.save_pkcs1('PEM'))


def loadKeys():
    with open('keys/publicKey.txt', 'rb') as p:
        public_key = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.txt', 'rb') as p:
        private_key = rsa.PrivateKey.load_pkcs1(p.read())
    return public_key, private_key


def encrypt(filename, key):
    with open(filename, 'r') as f:
        message = f.read()
        with open('cipher_' + filename, 'w') as ff:
            cipher_message = rsa.encrypt(message.encode('ascii'), key)
            ff.write(str(cipher_message))
        return cipher_message


def decrypt(ciphertext2, key):
    try:
        return rsa.decrypt(ciphertext2, key).decode('ascii')
    except:
        return False


def sign(filename, key):
    with open(filename, 'r') as f:
        message = f.read()
        with open('sign_' + filename, 'w') as ff:
            signed_message = rsa.sign(message.encode('ascii'), key, 'SHA-1')
            ff.write(str(signed_message))
            return signed_message


def verify(message2, signature2, key):
    try:
        return rsa.verify(message2.encode('ascii'), signature2, key, ) == 'SHA-1'
    except:
        return False


def main():
    generateKeys(int(input('Write key length:')))
    public_key, private_key = loadKeys()

    file_name = input('Write the path to the file here:')
    ciphertext = encrypt(file_name, public_key)
    signature = sign(file_name, private_key)
    text = decrypt(ciphertext, private_key)

    print(f'Cipher text saved to this file: cipher_{file_name}')
    print(f'Signature saved to this file: sign_{file_name}')

    if text:
        print(f'Message text: {text}')
    else:
        print(f'Unable to decrypt the message.')

    if verify(text, signature, public_key):
        print('Successfully verified signature')
    else:
        print('The message signature could not be verified')


if __name__ == "__main__":
    main()
