from django.db import transaction


class atomic_if_using_transaction:

    def __init__(self, using_transactions):
        self.using_transactions = using_transactions
        if using_transactions:
            self.context_manager = transaction.atomic()

    def __enter__(self):
        if self.using_transactions:
            self.context_manager.__enter__()

    def __exit__(self, *args):
        if self.using_transactions:
            self.context_manager.__exit__(*args)
