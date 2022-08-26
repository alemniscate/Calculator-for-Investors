import re
import os
import sqlite3

def main_menu():
    while True:
        print("MAIN MENU")
        print("0 Exit")
        print("1 CRUD operations")
        print("2 Show top ten companies by criteria")
        print()
        print("Enter an option:")
        num = input()
        if  len(num) == 1 and re.match("[0-2]", num):
            return int(num)
        print("Invalid option!")
        print()

def crud_menu(crud):
    while True:
        print("CRUD MENU")
        print("0 Back")
        print("1 Create a company")
        print("2 Read a company")
        print("3 Update a company")
        print("4 Delete a company")
        print("5 List all companies")
        print()
        print("Enter an option:")
        num = input()
        if len(num) == 1 and re.match("[0-5]", num):
            crud.exec(int(num))
            print()
            return int(num)
        print("Invalid option!")
        print()

def top_menu():
    while True:
        print("TOP TEN MENU")
        print("0 Back")
        print("1 List by ND/EBITDA")
        print("2 List by ROE")
        print("3 List by ROA")
        print()
        print("Enter an option:")
        num = input()
        if len(num) == 1 and re.match("[0-3]", num):
            crud.topten(int(num))
            print()
            return int(num)
        print("Invalid option!")
        print()
        return int(num)

class Crud:
    def __init__(self):
        dbfile = 'investor.db'
        dbexist_flag = os.path.exists(dbfile)
        
        self.con = sqlite3.connect(dbfile)
        self.cursor = self.con.cursor()

        if not dbexist_flag:
            self.create_companies_table()
            self.con.commit()
            self.create_financial_table()
            self.con.commit()

    def create_companies_table(self):

        with open("C:/private/src/python/idea/calculatorforinvestor/test/companies.csv", encoding="utf-8") as f:
            lines = f.readlines()

        companies = []
        for line in lines:
            companies.append(line.strip())

        self.cursor.execute("""create table if not exists companies(
            ticker text,
            name text,
            sector text,
            primary key (ticker)
            );""")

        self.cursor.execute("delete from companies") 
        for company in companies[1:]:
            match = re.match('(.+?),"(.+?)",(.+)', company)
            if match:
                ticker = match.group(1)
                name = match.group(2)
                sector = match.group(3)
            else:
                ticker, name, sector = company.split(",")

            self.cursor.execute(f"insert into companies values('{ticker}', '{name}', '{sector}');")
        self.con.commit()

    def create_financial_table(self):

        with open("C:/private/src/python/idea/calculatorforinvestor/test/financial.csv", encoding="utf-8") as f:
            lines = f.readlines()

        financial = []
        for line in lines:
            financial.append(line.strip())

        self.cursor.execute("""create table if not exists financial(
            ticker text,
            ebitda integer,
            sales integer,
            net_profit integer,
            market_price integer,
            net_debt integer,
            assets integer,
            equity integer,
            cash_equivalents integer,
            liabilities integer,
            primary key (ticker)
            );""")

        self.cursor.execute("delete from financial") 
        for stock in financial[1:]:
            cells = stock.split(",")
            cells = [x if x != "" else "null" for x in cells]
            ticker = cells[0]
            details = ",".join(cells[1:])

            self.cursor.execute(f"insert into financial values('{ticker}', {details});")
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()

    def exec(self, num):
        if num == 1:
            self.create()
        elif num == 2:
            self.read()
        elif num == 3:
            self.update()
        elif num == 4:
            self.delete()
        elif num == 5:
            self.listall()
        else:
            return

    def topten(self, num):
        if num == 1:
            self.nd_ebitda()
        elif num == 2:
            self.roe()
        elif num == 3:
            self.roa()
        else:
            return
            
    def nd_ebitda(self):
        print("TICKER ND/EBITDA")
        result = self.cursor.execute(f"select ticker, round(cast(net_debt as float) / cast(ebitda as float), 2) as ratio from financial order by 2 desc;")
        ratios = result.fetchall()
        for ticker, ratio in ratios[:10]:
            print(f"{ticker} {round(ratio, 2)}")

    def roe(self):
        print("TICKER ROE")
        result = self.cursor.execute(f"select ticker, round(cast(net_profit as float) / cast(equity as float), 2) as ratio from financial order by 2 desc;")
        ratios = result.fetchall()
        for ticker, ratio in ratios[:10]:
            print(f"{ticker} {round(ratio, 2)}")

    def roa(self):
        print("TICKER ROA")
        result = self.cursor.execute(f"select ticker, round(cast(net_profit as float) / cast(assets as float), 2) as ratio from financial order by 2 desc;")
        ratios = result.fetchall()
        for ticker, ratio in ratios[:10]:
            print(f"{ticker} {round(ratio, 2)}")

    def input_company(self):
        print("Enter ticker (in the format 'MOON'):")
        ticker = input()
        print("Enter company (in the format 'Moon Corp'):")
        name = input()
        print("Enter industries (in the format 'Technology'):")
        sector = input()
        return ticker, name, sector
    
    def input_financial(self):
        print("Enter ebitda (in the format '987654321'):")
        ebitda = input()
        print("Enter sales (in the format '987654321'):")
        sales = input()
        print("Enter net profit (in the format '987654321'):")
        net_profit = input()
        print("Enter market price (in the format '987654321'):")
        market_price = input()
        print("Enter net dept (in the format '987654321'):")
        net_debt = input()
        print("Enter assets (in the format '987654321'):")
        assets = input()
        print("Enter equity (in the format '987654321'):")
        equity = input()
        print("Enter cash equivalents (in the format '987654321'):")
        cash_equivalents = input()
        print("Enter liabilities (in the format '987654321'):")
        liabilities = input()

        return ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities

    def create(self):

        ticker, name, sector = self.input_company()
        financial = self.input_financial()
        details = ",".join(financial)

        self.cursor.execute(f"insert into companies values('{ticker}', '{name}', '{sector}');")
        self.cursor.execute(f"insert into financial values('{ticker}', {details});")
        self.con.commit()

        print("Company created successfully!")

    def input_company_name(self):
        print("Enter company name:")
        name = input()
        result = self.cursor.execute(f"select name from companies where name like'%{name}%';")
        companies = result.fetchall()
        if len(companies) == 0:
            print("Company not found!")
            return None, None
        for i, company in enumerate(companies):
            print(f"{i} {company[0]}")
        print("Enter company number:")
        num = int(input())
        name = companies[num][0]
        result = self.cursor.execute(f"select ticker from companies where name = '{name}';")
        ticker = result.fetchone()[0]    
        return name, ticker           

    def read(self):
        name, ticker = self.input_company_name()    
        if name == None:
            return     
        result = self.cursor.execute(f"select * from financial where ticker = '{ticker}';")

        financial = result.fetchone()
        ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities = financial[1:]
        print(f"{ticker} {name}")
        try:
            print(f"P/E = {round(market_price / net_profit, 2)}")
        except:
            print(f"P/E = None")

        try:
            print(f"P/S = {round(market_price / sales, 2)}")
        except:
            print(f"P/S = None")

        try:
            print(f"P/B = {round(market_price / assets, 2)}")
        except:
            print(f"P/B = None")

        try:
            print(f"ND/EBITDA = {round(net_debt / ebitda, 2)}")
        except:
            print(f"ND/EBITDA = None")

        try:
            print(f"ROE = {round(net_profit / equity, 2)}")
        except:
            print(f"ROE = None")

        try:
            print(f"ROA = {round(net_profit / assets, 2)}")
        except:
            print(f"ROA = None")

        try:
            print(f"L/A = {round(liabilities / assets, 2)}")
        except:
            print(f"L/A = None")

        pass

    def update(self):
        name, ticker = self.input_company_name()    
        if name == None:
            return     

        financial = self.input_financial()
        ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalents, liabilities = financial

        self.cursor.execute(f"update financial set ebitda = {ebitda} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set ebitda = {ebitda} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set sales = {sales} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set net_profit = {net_profit} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set market_price = {market_price} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set net_debt = {net_debt} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set assets = {assets} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set equity = {equity} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set cash_equivalents = {cash_equivalents} where ticker = '{ticker}';")
        self.cursor.execute(f"update financial set liabilities = {liabilities} where ticker = '{ticker}';")
        self.con.commit()

        print("Company updated successfully!")

    def delete(self):
        name, ticker = self.input_company_name()    
        if name == None:
            return     

        self.cursor.execute(f"delete from companies where ticker = '{ticker}';")
        self.cursor.execute(f"delete from financial where ticker = '{ticker}';")
        self.con.commit()

        print("Company deleted successfully!")

    def listall(self):
        print("COMPANY LIST")
        result = self.cursor.execute(f"select * from companies order by 1;")
        companies = result.fetchall()
        for company in companies:
            ticker, name, sector = company
            print(f"{ticker} {name} {sector}")

if __name__ == "__main__":

    print("Welcome to the Investor Program!")
    print()

    crud = Crud()

    num = -1
    while num != 0:
        num = main_menu()
        if num == 0:
            print("Have a nice day!")
        elif num == 1:
            print()
            crud_menu(crud)
        elif num == 2:
            print()
            top_menu()

    crud.close()
