# Include the Dropbox SDK
import dropbox
import gnupg
import os
import sys
from os import path

# Get your app key and secret from the Dropbox developer website
app_key = ''
app_secret = ''

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

#Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

#This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)
client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()
gpg = gnupg.GPG()
gpg.encoding='utf-8'

#generating key for sender
input_data_sender = gpg.gen_key_input(
    key_type="RSA",
    key_length=1024,
    name_real="sender",
    passphrase='spass')
key_sender = gpg.gen_key(input_data_sender)
print key_sender

#generating key for receiver
##input_data_receiver = gpg.gen_key_input(
##    key_type="RSA",
##    key_length=1024,
##    name_real="receiver",
##    passphrase='rpass')
##key_receiver = gpg.gen_key(input_data_receiver)
##print key_receiver

#filename = raw_input("Enter the file to upload to dropbox").strip()

#encrypt
temp = sys.argv[1]
fp = path.abspath(temp)
filename = os.path.basename(fp)
f = open(fp, 'rb')
print f
a = 'F:/Workspace/Temp/' + filename
status = gpg.sign_file(
    f, passphrase='qwerty')

#symmetric
status = gpg.encrypt_file(
        f, recipients='none',
        symmetric='AES256',
        passphrase='empty',
        output=a)

f = open(filename, 'rb')
response = client.put_file(filename, f, overwrite=True)
print 'uploaded: ', response

# folder_metadata = client.metadata('/')

f = client.get_file(filename)
#f = open(filename, 'rb')
b = 'F:/Workspace/Download/'+filename
#decrypted_file = gpg.decrypt_file(f, output=b)
decrypted_file = gpg.decrypt_file(f, passphrase = raw_input("Enter the authorization code here: ").strip(),  output=b)


print 'ok: ', decrypted_file.ok
print 'status: ', decrypted_file.status
print 'stderr: ', decrypted_file.stderr

#Checking if the Signature is valid
if decrypted_file.trust_level is not None and decrypted_file.trust_level >= decrypted_file.TRUST_FULLY:
    print('Trust level: %s' % decrypted_file.trust_text)

