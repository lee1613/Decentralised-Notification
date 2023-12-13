from pyteal import *


def approval_program():
    on_creation = Seq(
        [
            App.globalPut(Bytes("Asset ID"), Int(0)),
            App.globalPut(Bytes("Asset Left"), Int(0)),
            Return(Int(1))
        ]
    )


    asset_creation = Seq(
        [
            Assert(Txn.application_args.length() == Int(1)),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetConfig, 
                    TxnField.config_asset_total: Int(100000),
                    TxnField.config_asset_decimals: Int(0),
                    TxnField.config_asset_name: Bytes("Note Value"),
                    TxnField.config_asset_unit_name: Bytes("Alert"),
                    TxnField.config_asset_url: Bytes("https://algorand.com/"),
                    TxnField.config_asset_manager: Global.current_application_address(),
                    TxnField.config_asset_freeze: Global.current_application_address(),
                    TxnField.config_asset_clawback: Global.current_application_address(),
                    TxnField.config_asset_reserve: Global.current_application_address(),
                }
            ),
            InnerTxnBuilder.Submit(),
            App.globalPut(Bytes("Asset ID"), InnerTxn.created_asset_id()),
            App.globalPut(Bytes("Asset Left"), Int(100000)),
            Return(Int(1))
        ]
    )

    notify = Seq(
        [
            Assert(Txn.application_args.length() == Int(2)),
            Assert(Txn.accounts.length() == Int(1)),
            Assert(Txn.assets.length() == Int(1)),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.asset_amount: Int(1),
                    TxnField.asset_receiver: Txn.accounts[0],
                    TxnField.xfer_asset: Txn.assets[0],
                    TxnField.note: Bytes(Txn.application_args[0]),

                }
            ),
            InnerTxnBuilder.Submit(),
            asset_left := AssetHolding.balance(Global.current_application_address(),InnerTxn.created_asset_id()),
            App.globalPut(Bytes("Asset Left"), asset_left.value()),
            Return(Int(1))
        ]
    )




    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.application_args[0] == Bytes("Set Up"), asset_creation],
        [Txn.application_args[0] == Bytes("Notify"), notify],
    )

    return program


def clear_state_program():
    program = Seq(
        [
            Return(Int(1)),
        ]
    )
    return program


if __name__ == "__main__":
    with open("approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=8)
        f.write(compiled)

    with open("clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=8)
        f.write(compiled)


