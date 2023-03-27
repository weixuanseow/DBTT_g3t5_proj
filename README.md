# DBTT_g3t5_proj

https://github.com/weixuanseow/DBTT_g3t5_proj
Make a clone of this repository, then access <your path>/DBTT_g3t5_proj/processing_files and run Flask on your terminal for the features of the website to work


For Twilio to work, create a Twilio account on https://www.twilio.com/try-twilio.
Create a `.env` file in the `processing_files` folder on your machine with:
`TWILIO_ACCOUNT_SID=your_account_sid_here`
`TWILIO_AUTH_TOKEN=your_auth_token_here`
`TWILIO_PHONE_NUMBER=your_phone_number_here`

The phone number submitted in the contact form must also be in the list of "Verified Caller IDs" in your Twilio account.
Else, the Contact Us Page will still work, but you will not receive any SMS


Spacy installation:
`pip install spacy`
`python -m spacy download en_core_web_sm`
