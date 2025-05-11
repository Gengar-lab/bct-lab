import hashlib
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.table import Table

def hash_data(data):
    return hashlib.sha256(data.encode()).digest()

def combine_hashes(hash1, hash2):
    return hashlib.sha256(hash1 + hash2).digest()

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.transaction_hashes = []
        self.levels = []
        self.root = None
        self.build_tree()
    
    def build_tree(self):
        # Hash all transactions
        self.transaction_hashes = [hash_data(tx) for tx in self.transactions]
        
        # Build levels bottom-up
        current_level = self.transaction_hashes.copy()
        self.levels = [current_level]
        
        # If odd number of transactions, duplicate the last one
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])
        
        # Build tree from bottom up
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = combine_hashes(current_level[i], current_level[i+1])
                next_level.append(combined)
            
            if len(next_level) % 2 == 1 and len(next_level) > 1:
                next_level.append(next_level[-1])
                
            self.levels.append(next_level)
            current_level = next_level
        
        self.root = self.levels[-1][0]
    
    def get_root(self):
        return self.root.hex()
    
    def visualize(self):
        console = Console()
        
        # Create a tree to display transactions and their hashes
        tree = Tree("Merkle Tree", style="bold green")
        
        # Add the root hash at the top
        root_node = tree.add(f"🌳 Root Hash: {self.root.hex()}", style="bold green")
        
        # Add all levels in reverse order (from top to bottom)
        for level_idx in range(len(self.levels) - 2, -1, -1):
            level = self.levels[level_idx]
            level_node = root_node.add(f"Level {level_idx}", style="cyan")
            
            for i, hash_value in enumerate(level):
                if level_idx == 0:  # Leaf level (individual transactions)
                    tx_idx = i + 1
                    if tx_idx <= len(self.transactions):
                        tx_text = f"T{tx_idx}"
                        level_node.add(f"📄 {tx_text}: {hash_value.hex()}", style="yellow")
                    else:
                        # This is a duplicated transaction
                        tx_text = f"T{len(self.transactions)} (duplicate)"
                        level_node.add(f"📄 {tx_text}: {hash_value.hex()}", style="yellow")
                else:  # Interior level (combined hashes)
                    # Find the two child hashes from the level below
                    child_idx1 = i * 2
                    child_idx2 = i * 2 + 1
                    if child_idx1 < len(self.levels[level_idx-1]) and child_idx2 < len(self.levels[level_idx-1]):
                        child1 = self.levels[level_idx-1][child_idx1].hex()
                        child2 = self.levels[level_idx-1][child_idx2].hex()
                        level_node.add(f"🔷 H{i*2+1}{i*2+2}: {hash_value.hex()}\n    From H{i*2+1}: {child1[:16]}...\n    and H{i*2+2}: {child2[:16]}...", style="blue")
        
        # Print the tree
        console.print("\n")
        console.print(Panel(tree, title="Merkle Tree Structure (Bottom-Up)", border_style="green"))
        
        # Create a table with individual transaction hashes
        tx_table = Table(title="Transaction Hashes", show_header=True, header_style="bold magenta")
        tx_table.add_column("Transaction", style="cyan")
        tx_table.add_column("Hash", style="green")
        
        for i, tx in enumerate(self.transactions):
            tx_hash = self.transaction_hashes[i].hex()
            tx_table.add_row(f"T{i+1}", tx_hash)
        
        console.print("\n")
        console.print(tx_table)
        
        # Create information table
        info_table = Table(title="Merkle Tree Information", show_header=True, header_style="bold magenta")
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Number of Transactions", str(len(self.transactions)))
        info_table.add_row("Tree Height", str(len(self.levels)))
        info_table.add_row("Root Hash", self.root.hex())
        
        console.print("\n")
        console.print(info_table)
        
        console.print("\n")
        console.print(Panel(
            """[bold]Legend:[/bold]
            🌳 : Merkle Root (top hash combining all transactions)
            🔷 : Interior Node (hash combining two child hashes)
            📄 : Leaf Node (individual transaction hash)
            
            [yellow]Yellow[/yellow] : Individual transaction hashes
            [blue]Blue[/blue] : Combined hashes of child nodes
            [green]Green[/green] : Root hash (final combined hash)""",
            title="Legend",
            border_style="blue"
        ))

def main():
    num_transactions = 11
    transactions = [f"Transaction {i}" for i in range(1, num_transactions + 1)]
    
    tree = MerkleTree(transactions)
    
    print(f"Merkle Root: {tree.get_root()}")
    print(f"Number of levels: {len(tree.levels)}")
    
    tree.visualize()

if __name__ == "__main__":
    main()