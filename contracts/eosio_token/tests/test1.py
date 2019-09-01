import sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = Account()
HOST = Account()
ALICE = Account()
BOB = Account()
CAROL = Account()

def test():
    SCENARIO("""
    Initialize the token and run a couple of transfers between different accounts.
    """)
    reset()
    create_master_account("MASTER")

    COMMENT("""
    Build & deploy the contract:
    """)
    create_account("HOST", MASTER)
    smart = Contract(HOST, CONTRACT_WORKSPACE)
    smart.build(force=False)
    smart.deploy()

    COMMENT("""
    Create test accounts:
    """)
    create_account("ALICE", MASTER)
    create_account("BOB", MASTER)
    create_account("CAROL", MASTER)

    COMMENT("""
    Initialize the token and send some tokens to one of the accounts:
    """)

    HOST.push_action(
        "create",
        {
            "issuer": MASTER,
            "maximum_supply": "1000000000.0000 EOS",
            "can_freeze": "0",
            "can_recall": "0",
            "can_whitelist": "0"
        },
        permission=[(MASTER, Permission.OWNER), (HOST, Permission.ACTIVE)])

    HOST.push_action(
        "issue",
        {
            "to": ALICE, "quantity": "100.0000 EOS", "memo": ""
        },
        permission=(MASTER, Permission.ACTIVE))

    COMMENT("""
    Execute a series of transfers between the accounts:
    """)

    HOST.push_action(
        "transfer",
        {
            "from": ALICE, "to": CAROL,
            "quantity": "25.0000 EOS", "memo":""
        },
        permission=(ALICE, Permission.ACTIVE))

    HOST.push_action(
        "transfer",
        {
            "from": CAROL, "to": BOB, 
            "quantity": "11.0000 EOS", "memo": ""
        },
        permission=(CAROL, Permission.ACTIVE))

    HOST.push_action(
        "transfer",
        {
            "from": CAROL, "to": BOB, 
            "quantity": "2.0000 EOS", "memo": ""
        },
        permission=(CAROL, Permission.ACTIVE))

    HOST.push_action(
        "transfer",
        {
            "from": BOB, "to": ALICE,
            "quantity": "2.0000 EOS", "memo":""
        },
        permission=(BOB, Permission.ACTIVE))

    COMMENT("""
    Verify the outcome:
    """)

    table_alice = HOST.table("accounts", ALICE)
    table_bob = HOST.table("accounts", BOB)
    table_carol = HOST.table("accounts", CAROL)

    assert table_alice.json["rows"][0]["balance"] == '77.0000 EOS'
    assert table_bob.json["rows"][0]["balance"] == '11.0000 EOS'
    assert table_carol.json["rows"][0]["balance"] == '12.0000 EOS'

    stop()


if __name__ == "__main__":
    test()
