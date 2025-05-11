sudo apt update && sudo apt upgrade -y

sudo apt-get install build-essential jq curl git -y

pip3 install --upgrade pip

pip3 install -r requirements.txt

curl -sSL https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/bootstrap.sh| bash -s

curl -L https://foundry.paradigm.xyz | bash

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

\. "$HOME/.nvm/nvm.sh"

nvm install 20

npm install -g yarn

foundryup

export PATH=$PATH:~/fabric-samples/bin