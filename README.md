# onetimepad
A simple onetimepad script

# encrypt

```sh
echo "Hello, World" > ./in
python3 onetimepad.py -m encrypt -i ./in -o ./out
cat ./out  # base64 encoded secret
I0hHIghjXXwvQ18L
```

# decrypt

```sh
cat ./out > ./in
python3 onetimepad.py -m decrypt -i ./in -o ./out
cat ./out  # cleartext
Hello, World
```

# key file

A new key is generated for every encryption. An existent key is overwritten.

    ./key
