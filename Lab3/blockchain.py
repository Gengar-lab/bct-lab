import hashlib
import json
import time
import random
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
from rich import box

console = Console()

# Ethereum units
WEI_PER_ETHER = 10**18
GWEI_PER_ETHER = 10**9

class Account:
    def __init__(self, address: str):
        self.address = address
        self.balance = 100
        self.transaction_count = 0
        self.created_at = time.time()
        self.last_active = time.time()
        
    def update_activity(self):
        self.last_active = time.time()
        
    def add_transaction(self):
        self.transaction_count += 1
        self.update_activity()

class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
        self.miner = ""
        self.difficulty = 0
        self.size = len(str(transactions))

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    def __str__(self) -> str:
        return f"Block #{self.index} | Hash: {self.hash} | TXs: {len(self.transactions)}"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.accounts = {}
        self.difficulty = 4
        self.mining_reward = 100
        self.total_coins = 0
        self.blocks_mined = 0
        self.current_account = None
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = Block(0, [], time.time(), "0" * 64)
        genesis.hash = genesis.calculate_hash()
        genesis.miner = "0x0000000000000000000000000000000000000000"
        self.chain.append(genesis)
    
    def create_account(self) -> str:
        address = f"0x{hashlib.sha256(str(time.time()).encode()).hexdigest()}"
        self.accounts[address] = Account(address)
        self.total_coins += 100
        return address
    
    def switch_account(self, address: str) -> bool:
        if address in self.accounts:
            self.current_account = address
            self.accounts[address].update_activity()
            return True
        return False
    
    def get_current_account(self) -> str:
        return self.current_account
    
    def get_balance(self, address: str) -> int:
        return self.accounts[address].balance if address in self.accounts else 0
    
    def get_account_info(self, address: str) -> Dict:
        if address not in self.accounts:
            return None
        account = self.accounts[address]
        return {
            "address": account.address,
            "balance": account.balance,
            "transactions": account.transaction_count,
            "created": time.ctime(account.created_at),
            "last_active": time.ctime(account.last_active)
        }
    
    def create_transaction(self, sender: str, recipient: str, amount: int) -> bool:
        if sender not in self.accounts or recipient not in self.accounts:
            return False
            
        if self.get_balance(sender) < amount:
            return False
            
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": time.time()
        })
        
        self.accounts[sender].add_transaction()
        return True
    
    def mine_pending_transactions(self, miner_address: str):
        if miner_address not in self.accounts:
            return None
            
        self.pending_transactions.append({
            "sender": "0x0000000000000000000000000000000000000000",
            "recipient": miner_address,
            "amount": self.mining_reward,
            "timestamp": time.time()
        })
        
        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.chain[-1].hash
        )
        
        block.miner = miner_address
        block.difficulty = self.difficulty
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Mining block...", total=None)
            while block.hash[:self.difficulty] != "0" * self.difficulty:
                block.nonce += 1
                block.hash = block.calculate_hash()
                progress.update(task, advance=1)
        
        self.chain.append(block)
        self.blocks_mined += 1
        
        for tx in self.pending_transactions:
            if tx["sender"] != "0x0000000000000000000000000000000000000000":
                self.accounts[tx["sender"]].balance -= tx["amount"]
            self.accounts[tx["recipient"]].balance += tx["amount"]
            self.accounts[tx["recipient"]].add_transaction()
        
        self.pending_transactions = []
        return block
    
    def get_blockchain_stats(self) -> Dict:
        return {
            "total_blocks": len(self.chain),
            "total_transactions": sum(len(block.transactions) for block in self.chain),
            "total_coins": self.total_coins,
            "difficulty": self.difficulty,
            "pending_transactions": len(self.pending_transactions),
            "accounts": len(self.accounts)
        }
    
    def get_block_info(self, block_index: int) -> Dict:
        if 0 <= block_index < len(self.chain):
            block = self.chain[block_index]
            return {
                "index": block.index,
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "timestamp": time.ctime(block.timestamp),
                "miner": block.miner,
                "transactions": len(block.transactions),
                "size": block.size,
                "difficulty": block.difficulty
            }
        return None

def display_menu():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]BlockchainPy 1.0[/bold cyan]\n"
        "[yellow]Current Account:[/yellow] " + 
        (f"[green]{blockchain.get_current_account()}[/green]" if blockchain.get_current_account() else "[red]None[/red]"),
        title="Main Menu",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    table.add_column("Description", style="green")
    
    menu_items = [
        ("1", "Create account"),
        ("2", "Switch account"),
        ("3", "Check balance"),
        ("4", "Send coins"),
        ("5", "Mine block"),
        ("6", "View blockchain"),
        ("7", "View account details"),
        ("8", "View block details"),
        ("9", "View blockchain stats"),
        ("10", "List all accounts"),
        ("11", "Exit")
    ]
    
    for option, desc in menu_items:
        table.add_row(option, desc)
    
    console.print(table)
    return Prompt.ask("Select option", choices=[str(i) for i in range(1, 12)])

def display_account_selection():
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    table.add_column("Address", style="yellow")
    table.add_column("Balance", style="green")
    
    accounts = list(blockchain.accounts.items())
    for idx, (address, account) in enumerate(accounts, 1):
        table.add_row(
            str(idx),
            address,
            str(account.balance)
        )
    
    console.print(Panel(table, title="Available Accounts", border_style="cyan"))
    return Prompt.ask("Select account number", choices=[str(i) for i in range(1, len(accounts) + 1)])

def main():
    global blockchain
    blockchain = Blockchain()
    
    accounts = [blockchain.create_account() for _ in range(3)]
    console.print(f"[green]Created {len(accounts)} accounts[/green]")
    
    blockchain.switch_account(accounts[0])
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            address = blockchain.create_account()
            console.print(f"[green]Created account: {address}[/green]")
            
        elif choice == "2":
            console.print("\n[yellow]Available accounts:[/yellow]")
            account_num = display_account_selection()
            selected_address = list(blockchain.accounts.keys())[int(account_num) - 1]
            if blockchain.switch_account(selected_address):
                console.print(f"[green]Switched to account: {selected_address}[/green]")
            else:
                console.print("[red]Account not found[/red]")
            
        elif choice == "3":
            if blockchain.get_current_account():
                balance = blockchain.get_balance(blockchain.get_current_account())
                console.print(f"[green]Current account balance: {balance} coins[/green]")
            else:
                console.print("[red]No account selected[/red]")
            
        elif choice == "4":
            if not blockchain.get_current_account():
                console.print("[red]No account selected[/red]")
                continue
                
            recipient = Prompt.ask("To")
            try:
                amount = int(Prompt.ask("Amount"))
                if blockchain.create_transaction(blockchain.get_current_account(), recipient, amount):
                    console.print("[green]Transaction created[/green]")
                else:
                    console.print("[red]Transaction failed[/red]")
            except ValueError:
                console.print("[red]Invalid amount[/red]")
                
        elif choice == "5":
            if not blockchain.get_current_account():
                console.print("[red]No account selected[/red]")
                continue
                
            block = blockchain.mine_pending_transactions(blockchain.get_current_account())
            if block:
                console.print(f"[green]Block mined: {block.hash}[/green]")
            else:
                console.print("[red]Mining failed[/red]")
                
        elif choice == "6":
            table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
            table.add_column("Block #", style="cyan")
            table.add_column("Hash", style="yellow")
            table.add_column("Transactions", style="green")
            
            for block in blockchain.chain:
                table.add_row(
                    str(block.index),
                    block.hash,
                    str(len(block.transactions))
                )
            
            console.print(Panel(table, title="Blockchain", border_style="cyan"))
                
        elif choice == "7":
            if blockchain.get_current_account():
                info = blockchain.get_account_info(blockchain.get_current_account())
                table = Table(show_header=False, box=box.ROUNDED)
                table.add_column("Field", style="cyan")
                table.add_column("Value", style="green")
                
                for key, value in info.items():
                    table.add_row(key.capitalize(), str(value))
                
                console.print(Panel(table, title="Account Details", border_style="cyan"))
            else:
                console.print("[red]No account selected[/red]")
                
        elif choice == "8":
            try:
                index = int(Prompt.ask("Enter block number"))
                info = blockchain.get_block_info(index)
                if info:
                    table = Table(show_header=False, box=box.ROUNDED)
                    table.add_column("Field", style="cyan")
                    table.add_column("Value", style="green")
                    
                    for key, value in info.items():
                        table.add_row(key.capitalize(), str(value))
                    
                    console.print(Panel(table, title="Block Details", border_style="cyan"))
                else:
                    console.print("[red]Block not found[/red]")
            except ValueError:
                console.print("[red]Invalid block number[/red]")
                
        elif choice == "9":
            stats = blockchain.get_blockchain_stats()
            table = Table(show_header=False, box=box.ROUNDED)
            table.add_column("Stat", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in stats.items():
                table.add_row(key.replace("_", " ").title(), str(value))
            
            console.print(Panel(table, title="Blockchain Stats", border_style="cyan"))
            
        elif choice == "10":
            table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
            table.add_column("Address", style="cyan")
            table.add_column("Balance", style="green")
            table.add_column("Transactions", style="yellow")
            table.add_column("Last Active", style="blue")
            
            for address, account in blockchain.accounts.items():
                table.add_row(
                    address,
                    str(account.balance),
                    str(account.transaction_count),
                    time.ctime(account.last_active)
                )
            
            console.print(Panel(table, title="All Accounts", border_style="cyan"))
                
        elif choice == "11":
            if Confirm.ask("Are you sure you want to exit?"):
                console.print("[green]Goodbye![/green]")
                break
            
        console.print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    main() 