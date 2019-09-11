import asyncio
from gino import Gino

db = Gino()

class AccountGroup(db.Model):
    __tablename__ = 'account_group'

    account_group_number = db.Column(db.String, primary_key=True)
    first_number = db.Column(db.String)
    last_number = db.Column(db.String)
    account_group_name = db.Column(db.String)

    #_pk = db.PrimaryKeyConstraint('account_group_number', name='accountgroup_pkey')
    idx1 = db.Index('first_idx_last', 'first_number', 'last_number', unique=True)

class RefTransactionTypes(db.Model):
    __tablename__ = 'ref_transaction_types'

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
    account_name = db.Column(db.String)

class FinancialTransactions(db.Model):
    __tablename__ = 'financial_transactions'

    transaction_id = db.Column(db.String, primary_key=True)
    transaction_type_code = db.Column(db.String, db.ForeignKey('ref_transaction_types.transaction_type_code'))
    transaction_date = db.Column(db.Date)
    transaction_amount = db.Column(db.Numeric)
    transaction_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class AccountsInTransactions(db.Model):
    __tablename__ = 'accounts_in_transactions'

    transaction_id = db.Column(db.String, db.ForeignKey('financial_transactions.transaction_id'))
    account_number = db.Column(db.String)
    amount = db.Column(db.Numeric)

    _pk = db.PrimaryKeyConstraint('transaction_id', 'account_number', name='account_transaction_pkey')

class GeneralLedger(db.Model):
    __tablename__ = 'general_ledger'

    gl_entry_id = db.Column(db.String, primary_key=True)
    account_number = db.Column(db.String, db.ForeignKey('chart_of_account.account_number'))  
    transaction_id = db.Column(db.String)
    entry_ammount = db.Column(db.Numeric)
    entry_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class Parties(db.Model):
    __tablename__ = 'parties'

    party_id = db.Column(db.String, primary_key=True)
    party_type_code = db.Column(db.String, db.ForeignKey('ref_party_types.party_type_code'))
    party_name = db.Column(db.String)
    party_address = db.Column(db.String)
    party_description = db.Column(db.String)
    other_detail = db.Column(db.String)

class PartiesInTransaction(db.Model):
    __tablename__ = 'parties_in_transaction'    

    transaction_id = db.Column(db.String, db.ForeignKey('financial_transactions.transaction_id'))
    party_id = db.Column(db.String, db.ForeignKey('parties.party_id'))
    _pk = db.PrimaryKeyConstraint('transaction_id', 'party_id', name='parties_in_transaction_pkey')


async def migrate():
    await db.set_bind('postgres://miftah:fonez@localhost/accounting')
    await db.gino.create_all()

    #init Account Group
    acc1 = await AccountGroup.create(account_group_number='0001', first_number='1000', last_number='1999', account_group_name='Asset Accounts')    
    acc2 = await AccountGroup.create(account_group_number='0002', first_number='2000', last_number='2999', account_group_name='Liability Accounts')
    acc3 = await AccountGroup.create(account_group_number='0003', first_number='3000', last_number='3999', account_group_name='Equity Accounts')
    acc4 = await AccountGroup.create(account_group_number='0004', first_number='4000', last_number='4999', account_group_name='Revenue Accounts')
    acc5 = await AccountGroup.create(account_group_number='0005', first_number='5000', last_number='5999', account_group_name='COGS Accounts')
    acc6 = await AccountGroup.create(account_group_number='0006', first_number='6000', last_number='6999', account_group_name='Expenses Accounts')
    acc7 = await AccountGroup.create(account_group_number='0007', first_number='7000', last_number='7999', account_group_name='Other Revenue Accounts')
    acc8 = await AccountGroup.create(account_group_number='0008', first_number='8000', last_number='8999', account_group_name='Other Expenses Accounts')

    #init Chart of Account
    # Current Assets
    ca1 = await ChartOfAccount.create(account_number='1000', account_group_number='1000', account_name='Petty Cash')
    ca2 = await ChartOfAccount.create(account_number='1010', account_group_number='1000', account_name='Cash on Hand')
    ca3 = await ChartOfAccount.create(account_number='1020', account_group_number='1000', account_name='Regular Checking Account')
    ca4 = await ChartOfAccount.create(account_number='1030', account_group_number='1000', account_name='Payroll Checking Account')
    ca5 = await ChartOfAccount.create(account_number='1040', account_group_number='1000', account_name='Saving Account')
    ca6 = await ChartOfAccount.create(account_number='1050', account_group_number='1000', account_name='Special Account')
    ca7 = await ChartOfAccount.create(account_number='1060', account_group_number='1000', account_name='Investments - Money Market')
    ca8 = await ChartOfAccount.create(account_number='1070', account_group_number='1000', account_name='Investments - Certificate of Deposit')
    ca9 = await ChartOfAccount.create(account_number='1100', account_group_number='1000', account_name='Account Recivalble')
    ca10 = await ChartOfAccount.create(account_number='1140', account_group_number='1000', account_name='Other Receivable')
    ca11 = await ChartOfAccount.create(account_number='1150', account_group_number='1000', account_name='Allowance for Doubful Accounts')
    ca12 = await ChartOfAccount.create(account_number='1200', account_group_number='1000', account_name='Raw maaterial Inventory')
    ca13 = await ChartOfAccount.create(account_number='1205', account_group_number='1000', account_name='Supplier Inventory')
    ca14 = await ChartOfAccount.create(account_number='1210', account_group_number='1000', account_name='Work in Progress Inventory')
    ca15 = await ChartOfAccount.create(account_number='1215', account_group_number='1000', account_name='Finished Goofs Inventory - Product #1')
    ca16 = await ChartOfAccount.create(account_number='1220', account_group_number='1000', account_name='Finished Goofs Inventory - Product #2')
    ca17 = await ChartOfAccount.create(account_number='1230', account_group_number='1000', account_name='Finished Goofs Inventory - Product #3')
    ca18 = await ChartOfAccount.create(account_number='1400', account_group_number='1000', account_name='Prepaid Expenses')
    ca19 = await ChartOfAccount.create(account_number='1410', account_group_number='1000', account_name='Employee Advances')
    ca20 = await ChartOfAccount.create(account_number='1420', account_group_number='1000', account_name='Notes Receivable - Current')
    ca21 = await ChartOfAccount.create(account_number='1430', account_group_number='1000', account_name='Prepaid Interest')
    ca22 = await ChartOfAccount.create(account_number='1410', account_group_number='1000', account_name='Other Current Assets')

    # Fixed Assets
    fa1 = await ChartOfAccount.create(account_number='1500', account_group_number='1000', account_name='Furniture and Fixture')
    fa2 = await ChartOfAccount.create(account_number='1510', account_group_number='1000', account_name='Equipment')
    fa3 = await ChartOfAccount.create(account_number='1520', account_group_number='1000', account_name='Vehicles')
    fa4 = await ChartOfAccount.create(account_number='1530', account_group_number='1000', account_name='Other Depreciable Property')   
    fa5 = await ChartOfAccount.create(account_number='1540', account_group_number='1000', account_name='Leashold Improvements')
    fa6 = await ChartOfAccount.create(account_number='1550', account_group_number='1000', account_name='Buildings')
    fa7 = await ChartOfAccount.create(account_number='1560', account_group_number='1000', account_name='Building Improvements')
    fa8 = await ChartOfAccount.create(account_number='1590', account_group_number='1000', account_name='Land')
    fa9 = await ChartOfAccount.create(account_number='1700', account_group_number='1000', account_name='Accumulated Depreciation, Furniture and Fixtures')
    fa10 = await ChartOfAccount.create(account_number='1710', account_group_number='1000', account_name='Accumulated Depreciation, Equipment')
    fa11 = await ChartOfAccount.create(account_number='1720', account_group_number='1000', account_name='Accumulated Depreciation, Vehicles')
    fa12 = await ChartOfAccount.create(account_number='1730', account_group_number='1000', account_name='Accumulated Depreciation, Other')
    fa13 = await ChartOfAccount.create(account_number='1740', account_group_number='1000', account_name='Accumulated Depreciation, Leasehold')
    fa14 = await ChartOfAccount.create(account_number='1750', account_group_number='1000', account_name='Accumulated Depreciation, Buildings')
    fa15 = await ChartOfAccount.create(account_number='1760', account_group_number='1000', account_name='Accumulated Depreciation, Buildings Improvements')

    # Oher Assets
    oa1 = await ChartOfAccount.create(account_number='1900', account_group_number='1000', account_name='Deposits')
    oa2 = await ChartOfAccount.create(account_number='1910', account_group_number='1000', account_name='Organization')
    oa3 = await ChartOfAccount.create(account_number='1915', account_group_number='1000', account_name='Accumuated Amortization, Organization Costs')
    oa4 = await ChartOfAccount.create(account_number='1920', account_group_number='1000', account_name='Notes Receivable, Non-current')
    oa5 = await ChartOfAccount.create(account_number='1990', account_group_number='1000', account_name='Other Non-current Assets')

    # Liability Account
    # Current Liabilities
    lacl01 = await ChartOfAccount.create(account_number='2000', account_group_number='2000', account_name='Account Payable')
    lacl02 = await ChartOfAccount.create(account_number='2300', account_group_number='2000', account_name='Accrued Expenses')
    lacl03 = await ChartOfAccount.create(account_number='2310', account_group_number='2000', account_name='Sales Tax Payable')
    lacl04 = await ChartOfAccount.create(account_number='2320', account_group_number='2000', account_name='Wages Payable')
    lacl05 = await ChartOfAccount.create(account_number='2330', account_group_number='2000', account_name='401-K Deductions Payable')
    lacl06 = await ChartOfAccount.create(account_number='2335', account_group_number='2000', account_name='Health Insurance Payable')
    lacl07 = await ChartOfAccount.create(account_number='2340', account_group_number='2000', account_name='Federal Payroll Taxes Payable')
    lacl08 = await ChartOfAccount.create(account_number='2350', account_group_number='2000', account_name='FUTA Tax Payable')
    lacl09 = await ChartOfAccount.create(account_number='2340', account_group_number='2000', account_name='State Payroll Taxes Payable')
    lacl10 = await ChartOfAccount.create(account_number='2380', account_group_number='2000', account_name='Local Payroll Taxes Payable')
    lacl11 = await ChartOfAccount.create(account_number='2390', account_group_number='2000', account_name='Income Taxes Payable')
    lacl12 = await ChartOfAccount.create(account_number='2400', account_group_number='2000', account_name='Other Taxes Payable')
    lacl13 = await ChartOfAccount.create(account_number='2410', account_group_number='2000', account_name='Employee Benefits Payable')
    lacl14 = await ChartOfAccount.create(account_number='2420', account_group_number='2000', account_name='Current Portion of Long-Term Debt')
    lacl15 = await ChartOfAccount.create(account_number='2440', account_group_number='2000', account_name='Deposits from Customers')
    lacl16 = await ChartOfAccount.create(account_number='2480', account_group_number='2000', account_name='Other Current Liabilities')

    #Long term Liabilities
    laltl01 = await ChartOfAccount.create(account_number='2700', account_group_number='2000', account_name='Notes Payable')
    laltl02 = await ChartOfAccount.create(account_number='2702', account_group_number='2000', account_name='Land Payable')
    laltl03 = await ChartOfAccount.create(account_number='2704', account_group_number='2000', account_name='Equipment Payable')
    laltl04 = await ChartOfAccount.create(account_number='2706', account_group_number='2000', account_name='Vehicles Payable')
    laltl05 = await ChartOfAccount.create(account_number='2708', account_group_number='2000', account_name='Bank Loans Payable')
    laltl06 = await ChartOfAccount.create(account_number='2710', account_group_number='2000', account_name='Deferred Revenue')
    laltl07 = await ChartOfAccount.create(account_number='2740', account_group_number='2000', account_name='Other Long-term Liabilities')

    #Equity Accounts
    ea01 = await ChartOfAccount.create(account_number='3010', account_group_number='3000', account_name='Stated Capital')
    ea02 = await ChartOfAccount.create(account_number='3020', account_group_number='3000', account_name='Capital Surplus')
    ea03 = await ChartOfAccount.create(account_number='3030', account_group_number='3000', account_name='Retained Earnings')

    #Revenue Accounts
    ra01 = await ChartOfAccount.create(account_number='4000', account_group_number='4000', account_name='Product #1 Sales')
    ra02 = await ChartOfAccount.create(account_number='4020', account_group_number='4000', account_name='Product #2 Sales')
    ra03 = await ChartOfAccount.create(account_number='4040', account_group_number='4000', account_name='Product #3 Sales')
    ra04 = await ChartOfAccount.create(account_number='4060', account_group_number='4000', account_name='Interest Income')
    ra05 = await ChartOfAccount.create(account_number='4080', account_group_number='4000', account_name='Other Income')
    ra06 = await ChartOfAccount.create(account_number='4550', account_group_number='4000', account_name='Shipping Charges Reimbursed')
    ra07 = await ChartOfAccount.create(account_number='4800', account_group_number='4000', account_name='Sales Returns and Allowances')
    ra08 = await ChartOfAccount.create(account_number='4900', account_group_number='4000', account_name='Sales Discounts')

    # Cost of Goods Sold
    cogs01 = await ChartOfAccount.create(account_number='5000', account_group_number='5000', account_name='Product #1 Cost')
    cogs02 = await ChartOfAccount.create(account_number='5010', account_group_number='5000', account_name='Product #2 Cost')
    cogs03 = await ChartOfAccount.create(account_number='5020', account_group_number='5000', account_name='Product #3 Cost')
    cogs04 = await ChartOfAccount.create(account_number='5050', account_group_number='5000', account_name='Raw Material Purchases')
    cogs05 = await ChartOfAccount.create(account_number='5100', account_group_number='5000', account_name='Direct Labor Costs')
    cogs06 = await ChartOfAccount.create(account_number='5150', account_group_number='5000', account_name='Indirect Labor Costs')
    cogs07 = await ChartOfAccount.create(account_number='5200', account_group_number='5000', account_name='Heat and Power')
    cogs08 = await ChartOfAccount.create(account_number='5250', account_group_number='5000', account_name='Commissions')
    cogs09 = await ChartOfAccount.create(account_number='5300', account_group_number='5000', account_name='Miscellaneous Factory Costs')
    cogs10 = await ChartOfAccount.create(account_number='5700', account_group_number='5000', account_name='COGS, Salaries and Wages')
    cogs11 = await ChartOfAccount.create(account_number='5730', account_group_number='5000', account_name='COGS, Contract Labor')
    cogs12 = await ChartOfAccount.create(account_number='5750', account_group_number='5000', account_name='COGS, Freight')
    cogs13 = await ChartOfAccount.create(account_number='5800', account_group_number='5000', account_name='COGS, Other')
    cogs14 = await ChartOfAccount.create(account_number='5850', account_group_number='5000', account_name='Inventory Adjustment')
    cogs15 = await ChartOfAccount.create(account_number='5900', account_group_number='5000', account_name='Purchase Return and Allowances')
    cogs16 = await ChartOfAccount.create(account_number='5950', account_group_number='5000', account_name='Purchase Discount')

    # Expenses
    exp01 = await ChartOfAccount.create(account_number='6000', account_group_number='6000', account_name='Default Purchase Expense')
    exp02 = await ChartOfAccount.create(account_number='6010', account_group_number='6000', account_name='Advertising Expense')
    exp03 = await ChartOfAccount.create(account_number='6050', account_group_number='6000', account_name='Amortization Expense')
    exp04 = await ChartOfAccount.create(account_number='6100', account_group_number='6000', account_name='Auto Expenses')
    exp05 = await ChartOfAccount.create(account_number='6150', account_group_number='6000', account_name='Bad Debt Expense')
    exp06 = await ChartOfAccount.create(account_number='6200', account_group_number='6000', account_name='Bank Fees')
    exp07 = await ChartOfAccount.create(account_number='6250', account_group_number='6000', account_name='Cash Over and Short')
    exp08 = await ChartOfAccount.create(account_number='6300', account_group_number='6000', account_name='Charitable Contibutions Expense')
    exp09 = await ChartOfAccount.create(account_number='6350', account_group_number='6000', account_name='Commissions and Fees Expense')
    exp10 = await ChartOfAccount.create(account_number='6400', account_group_number='6000', account_name='Depreciation Expense')
    exp11 = await ChartOfAccount.create(account_number='6450', account_group_number='6000', account_name='Dues and Subscriptions Expense')
    exp12 = await ChartOfAccount.create(account_number='6500', account_group_number='6000', account_name='Employee Benefit Expense, Health Insurance')
    exp13 = await ChartOfAccount.create(account_number='6510', account_group_number='6000', account_name='Employee Benefit Expense, Pension Plan')
    exp14 = await ChartOfAccount.create(account_number='6520', account_group_number='6000', account_name='Employee Benefit Expense, Profit Sharing Plan')
    exp15 = await ChartOfAccount.create(account_number='6530', account_group_number='6000', account_name='Employee Benefit Expense, Other')
    exp16 = await ChartOfAccount.create(account_number='6550', account_group_number='6000', account_name='Freight Expense')
    exp17 = await ChartOfAccount.create(account_number='6600', account_group_number='6000', account_name='Gifts Expense')
    exp18 = await ChartOfAccount.create(account_number='6650', account_group_number='6000', account_name='Income Tax Expense, Federal')
    exp19 = await ChartOfAccount.create(account_number='6660', account_group_number='6000', account_name='Income Tax Expense, State')
    exp20 = await ChartOfAccount.create(account_number='6670', account_group_number='6000', account_name='Income Tax Expense, Local')
    




















    














    


















     








asyncio.get_event_loop().run_until_complete(init())
