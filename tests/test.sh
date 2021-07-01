#! /usr/bin/env bash

assert ()                 # exit if string not found in text
{
  text=$1
  string=$2

  if [[ $text == *"$string"* ]];
  then
    echo "'$string': passed"
  else
    echo "'$string' not found in text:"
    echo "$text"
    exit 99
  fi  
}

username=$(shuf -n1  /usr/share/dict/words)
password=$(shuf -n1  /usr/share/dict/words)
wrongpassword="hlerb"

register () { curl -d "username=$1&password=$2" -X POST http://localhost:5000/auth/register; }
login () { curl -d "username=$1&password=$2" -X POST http://localhost:5000/auth/login; }

assert "$(register "" "$password")" "Username is required"
assert "$(register "$username" "")" "Password is required"
assert "$(register "$username" "$password")" "Redirecting"
assert "$(register "$username" "$password")" "already registered"
assert "$(login "" "$password")" "Incorrect username"
assert "$(login "$username" "")" "Incorrect password"
assert "$(login "$username" "$wrongpassword")" "Incorrect password"
assert "$(login "$username" "$password")" "Redirecting"

