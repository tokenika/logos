#!/usr/bin/env python3
"""Pretty print json received from a PushAction object."""

#  HOST <= HOST::create         {"challenger":"ALICE","host":"CAROL"}
# executed transaction: 869173095f5ac4df477166eb285713e087eacac70395c7670148df3efaf043a4  112 bytes  1029 us
# warning: transaction executed locally, but may not be confirmed by the network yet    


example =\
{
    "actions": [
        {
            "account_action_seq": 0,
            "action_trace": {
                "account_ram_deltas": [],
                "act": {
                    "account": "HOST",
                    "authorization": [
                        {
                            "actor": "ALICE",
                            "permission": "active"
                        }
                    ],
                    "data": {
                        "by": "ALICE",
                        "challenger": "ALICE",
                        "column": 1,
                        "host": "CAROL",
                        "row": 1
                    },
                    "hex_data": "e047f11367e25426d057cbceae70ffabe047f11367e2542601000100",
                    "name": "move"
                },
                "action_ordinal": 1,
                "block_num": 80,
                "block_time": "2019-08-30T05:10:45.500",
                "closest_unnotified_ancestor_action_ordinal": 0,
                "console": "",
                "context_free": False,
                "creator_action_ordinal": 0,
                "elapsed": 1875,
                "error_code": None,
                "except": None,
                "producer_block_id": None,
                "receipt": {
                    "abi_sequence": 1,
                    "act_digest": "44e331aabcf32e90e6fe8bf64402736fd4dbb331755554beda4b1518581c36db",
                    "auth_sequence": [
                        [
                            "ALICE",
                            1
                        ]
                    ],
                    "code_sequence": 1,
                    "global_sequence": 87,
                    "receiver": "HOST",
                    "recv_sequence": 3
                },
                "receiver": "HOST",
                "trx_id": "b173077978f4c6df8d845f45dc62b4fd2b69ea6a9de57d4c324ee74460632103"
            },
            "block_num": 80,
            "block_time": "2019-08-30T05:10:45.500",
            "global_action_seq": 87
        },
        {
            "account_action_seq": 10,
            "action_trace": {
                "account_ram_deltas": [],
                "act": {
                    "account": "HOST",
                    "authorization": [
                        {
                            "actor": "CAROL",
                            "permission": "active"
                        }
                    ],
                    "data": {
                        "by": "ALICE",
                        "challenger": "ALICE",
                        "column": 1,
                        "host": "CAROL",
                        "row": 1
                    },
                    "hex_data": "e047f11367e25426d057cbceae70ffabe047f11367e2542601000100",
                    "name": "move"
                },
                "action_ordinal": 1,
                "block_num": 80,
                "block_time": "2019-08-30T05:20:45.500",
                "closest_unnotified_ancestor_action_ordinal": 0,
                "console": "",
                "context_free": False,
                "creator_action_ordinal": 0,
                "elapsed": 1875,
                "error_code": None,
                "except": None,
                "producer_block_id": None,
                "receipt": {
                    "abi_sequence": 1,
                    "act_digest": "44e331aabcf32e90e6fe8bf64402736fd4dbb331755554beda4b1518581c36db",
                    "auth_sequence": [
                        [
                            "ALICE",
                            1
                        ]
                    ],
                    "code_sequence": 1,
                    "global_sequence": 87,
                    "receiver": "HOST1",
                    "recv_sequence": 3
                },
                "receiver": "HOST1",
                "trx_id": "b173077978f4c6df8d845f45dc62b4fd2b69ea6a9de57d4c324ee74460632103"
            },
            "block_num": 80,
            "block_time": "2019-08-30T05:20:45.500",
            "global_action_seq": 87
        }
    ],
    "last_irreversible_block": 205
}


class GetActions():
    """
    Args:
        received_json (str): Data from nodeos.
        console (bool): print console output generated by action. Default is ``False``.
    """

    def __init__(self, received_json, console=False):

        if "actions" in received_json and received_json["actions"]:
            self.info = ""
            first = True

            for action in received_json["actions"]:
                if not first:
                    self.info = self.info + "\n"
                first = False

                act = action["action_trace"]["act"]
                self.info = self.info \
                    + ('block_time: %s\naction-receiver: "%s"\n'\
                    + 'trx_id: %s\nargs: %s\n') % (
                    action["block_time"],
                    "%s::%s => %s" % (
                        act["account"], 
                        act["name"], action["action_trace"]["receiver"]
                    ),
                    action["action_trace"]["trx_id"],
                    str(act["data"]).replace("'", '"')
                )
                if console:
                    self.info = self.info \
                        + 'console: %s' % (action["action_trace"]["console"])

                self.info = self.info + "\n"
        else:
            self.info = "The list of actions is empty."

    def __str__(self):
        return self.info
  
if __name__ == '__main__':
    print(GetActions(example, console=True))