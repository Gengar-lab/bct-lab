curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

\. "$HOME/.nvm/nvm.sh"

nvm install 20

cd web3-app

npm install

cd ~

curl -L https://foundry.paradigm.xyz | bash

source ~/.bashrc

foundryup