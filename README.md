# onetimepad
A simple onetimepad script

# encrypt

    echo "Hello, World" > ./in
    python3 onetimepad.py -m encrypt -i ./in -o ./out

# decrypt

    cat ./out > ./in
    python3 onetimepad.py -m decrypt -i ./in -o ./out
    cat ./out
    Hello, World

# key file

A new key is generated for every encryption.

    ./key
