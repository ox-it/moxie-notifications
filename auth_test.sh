#!/bin/bash
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
echo $canonical_form

authorize=$(echo -n "$canonical_form" | openssl sha1 -hmac "$secret" | sed 's/^.* //')

echo "Authorize header:"
echo $authorize
echo
echo
echo "$@"

curl -i -H "X-Moxie-Key: $apikey" -H "Date: $date" -H "X-HMAC-Nonce: $nonce" -H "Authorization: $authorize" -X $method "$@" $url
