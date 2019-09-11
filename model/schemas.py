import asyncio
from gino import Gino

db = Gino()

class AccountGroup(db.Model):
    __tablename__ = 'account_group'

    account_group_number = db.Column(db.String, primary_key=True)
    first_number = db.Column(db.String)
    last_number = db.Column(db.String)

    #_pk = db.PrimaryKeyConstraint('account_group_number', name='accountgroup_pkey')
    #idx1 = db.Index('first_idx_last', 'first_number', 'last_number', unique=True)

class TransactionTypes(db.Model):
    __tablename__ = 'transaction_types'

    transaction_type_code = db.Column(db.String, primary_key=True)
    transaction_type_description = db.Column(db.String)

class RefPartyTypes(db.Model):
    __tablename__ = 'ref_party_types'

    party_type_code = db.Column(db.String, primary_key=True)
    perty_type_description = db.Column(db.String)


class ChartOfAccount(db.Model):
    __tablename__ = 'chart_of_account'

    account_number = db.Column(db.String, primary_key=True)
    account_group_number = db.Column(db.String, db.ForeignKey('account_group.account_group_number'))

class GeneralLedger(db.Model):
    __tablename__ = 'general_ledger'

    gl_entry_id = db.Column(db.String, primary_key=True)
    account_number = db.Column(db.String, db.ForeignKey('chart_of_account.account_number'))  
    transaction_id = db.Column(db.String, db.ForeignKey('account_in_transaction.transaction_id'))
    entry_ammount = db.Column(db.Numeric)
    entry_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class AccountInTransaction(db.Model):
    __tablename__ = 'account_in_transaction'

    transaction_id = db.Column(db.String, db.ForeignKey('financial_transaction.transaction_id'))
    account_number = db.Column(db.String, db.ForeignKey('general_ledger.account_number'))
    ammount = db.Column(db.Numeric)

    _pk = db.PrimaryKeyConstraint('transaction_id', 'account_number', name='account_transaction_pkey')

class FinancialTransactions(db.Model):
    __tablename__ = 'financial_transactions'

    transaction_id = db.Column(db.String, primary_key=True)
    transaction_type_code = db.Column(db.String, db.ForeignKey('ref_transaction_types.transaction_type_code'))
    transaction_date = db.Column(db.Date)
    transaction_amount = db.Column(db.Numeric)
    transaction_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class Parties(db.Model):
    __tablename__ = 'parties'

    party_id = db.Column(db.String, primary_key=True)
    party_type_code = db.Column(db.String, db.ForeignKey('perty_types.party_id'))
    party_name = db.Column(db.String)
    party_address = db.Column(db.String)
    party_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class PartiesInTransaction(db.Model):
    __tablename__ = 'parties_in_transaction'    

    transaction_id = db.Column(db.String, db.ForeignKey('financial_transaction.transaction_id'))
    party_id = db.Column(db.String, db.ForeignKey('parties.party_id'))


async def main():
    await db.set_bind('postgres://miftah:fonez@localhost/accounting')
    await db.gino.create_all()

asyncio.get_event_loop().run_until_complete(main())
