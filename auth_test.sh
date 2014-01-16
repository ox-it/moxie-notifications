#!/bin/bash
# Script used for testing the HMAC authentication.
# Usage: ./auth_test.sh method url apikey sharedsecret [additional options for curl]
# Example: ./auth_test.sh POST http://localhost:5000/notifications/ myapikey mysharedsecret -d '{"message": "urgent message!"}'

# Builds a "canonical form" of the request, then uses openssl to create a HMAC which we
# capture the hex digest and build a curl request with all the correct headers.
method=$1
url=$2
apikey=$3
secret=$4
shift
shift
shift
shift

date=$(date)
nonce=$((RANDOM))

canonical_form="$method
$url
date:$date
x-hmac-nonce:$nonce"

echo "Canonical form:"
echo "$canonical_form"

authorize=$(echo -n "$canonical_form" | openssl sha1 -hmac "$secret" | sed 's/^.* //')

echo "Authorize header:"
echo $authorize
echo
echo
echo "$@"

curl -i -H "X-Moxie-Key: $apikey" -H "Date: $date" -H "X-HMAC-Nonce: $nonce" -H "Authorization: $authorize" -X $method "$@" $url
