# Bra och mindre bra saker jag gjort i detta projekt:
Bra saker: \
All funktionalitet ska fungera: \
Inloggning, registrering, köpfunktion, kontakta oss, produktfiltreringar etcetera.\
Mindre bra saker: \
Har ingen paketuppdelning alls i princip och massa onödiga dependencies lite överallt samt sett till cybersäkerhet så finns det en hel del brister. 

# i terminalen , kör :
export STRIPE_PUBLISHABLE_KEY=pk_test_78pDkolg6t41w0AnhbMGZHA100La2mslRc \
export STRIPE_SECRET_KEY=sk_test_15xXj4SyiGrtuWs6altppf4n00tK542kO3

# Vid stripebetalning:
Sätt systemvariablerna(environment variables) med:\
source .env\
Detta för att komma åt de säkert lagrade API-nycklarna\
Använd kortuppgifter från:
https://stripe.com/docs/testing#cards
