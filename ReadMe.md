# Documentation for deploying this smart contract onto Algorand Testnet

All the command belows are to be given as an input through the sandbox environment provided by algorand.

For more about the sandbox, please visit:   https://github.com/algorand/sandbox
## 1. Deploy smart contract into Algorand (Developers):

`goal app create --creator $account --approval-prog approval.teal --clear-prog clear.teal --global-ints 2 --global-byteslices 0 --local-ints 0 --local-byteslices 0`

## 2. Fund the smart contract account (Developers):
`goal clerk send --amount 500000 --from $account --to <app address>`

## 2. Setting Up smart contracts and create Fungible Token (Developers):
`goal app call --app-id <app id> --from $account --app-arg "str:Set Up"`

## 3. Opt-in into the asset created by smart contract (Users):
`goal asset optin --assetid <asset id> --account $account`

Note: You can obtain the asset id throught checking the smart contract details (Global State: Asset ID)

## 4. Developers can broadcast message to all (Developers):
`goal app call --app-id <app id> --from $account --app-arg "str:Notify" --app-arg "str:Hello" --app-account <account public key> --foreign-asset <asset id>`
