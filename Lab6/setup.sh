cd ~

sudo apt update
sudo apt-get install build-essential jq curl git

curl -sSL https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/bootstrap.sh| bash -s

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

\. "$HOME/.nvm/nvm.sh"

nvm install 20

npm install -g yarn

export PATH=$PATH:~/fabric-samples/bin

cd ~/fabric-samples/test-network

./network.sh down

./network.sh up createChannel

./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-javascript -ccl javascript