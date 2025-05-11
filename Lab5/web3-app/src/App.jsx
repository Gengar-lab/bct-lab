import { useState, useEffect } from 'react'
import Web3 from 'web3'
import './App.css'

function App() {
  const [web3, setWeb3] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [fromAddress, setFromAddress] = useState('');
  const [toAddress, setToAddress] = useState('');
  const [amount, setAmount] = useState('');
  const [balance, setBalance] = useState('0');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [transactionHash, setTransactionHash] = useState('');
  const [networkInfo, setNetworkInfo] = useState(null);
  const [showBlockDetails, setShowBlockDetails] = useState(false);
  const [blockDetails, setBlockDetails] = useState(null);

  useEffect(() => {
    const initWeb3 = async () => {
      try {
        // Connect to local Anvil instance
        const web3Instance = new Web3('http://127.0.0.1:8545');
        setWeb3(web3Instance);
        
        // Get network information
        try {
          const networkId = await web3Instance.eth.net.getId();
          const blockNumber = await web3Instance.eth.getBlockNumber();
          setNetworkInfo({
            id: networkId,
            name: networkId === 31337 ? 'Anvil Local Chain' : `Network ${networkId}`,
            blockNumber
          });
        } catch (err) {
          console.error('Error fetching network info:', err);
        }
        
        // Get accounts
        const accts = await web3Instance.eth.getAccounts();
        setAccounts(accts);
        
        if (accts.length > 0) {
          setFromAddress(accts[0]);
          // If we have more than one account, set the second as default recipient
          if (accts.length > 1) {
            setToAddress(accts[1]);
          }
          
          // Get balance of first account
          const bal = await web3Instance.eth.getBalance(accts[0]);
          setBalance(web3Instance.utils.fromWei(bal, 'ether'));
        }
      } catch (error) {
        console.error('Error initializing Web3:', error);
        setStatus('Failed to connect to blockchain. Is Anvil running?');
      }
    };

    initWeb3();
  }, []);

  const refreshBalance = async () => {
    if (web3 && fromAddress) {
      try {
        setIsLoading(true);
        const bal = await web3.eth.getBalance(fromAddress);
        setBalance(web3.utils.fromWei(bal, 'ether'));
        
        if (networkInfo) {
          const blockNumber = await web3.eth.getBlockNumber();
          setNetworkInfo({...networkInfo, blockNumber});
        }
        
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching balance:', error);
        setIsLoading(false);
      }
    }
  };

  const handleViewStats = async () => {
    if (!web3) return;
    
    try {
      setIsLoading(true);
      // Get latest block number
      const blockNumber = await web3.eth.getBlockNumber();
      
      // Get block details
      const block = await web3.eth.getBlock(blockNumber);
      
      // Get gas price
      const gasPrice = await web3.eth.getGasPrice();
      
      // Format data
      const blockInfo = {
        number: blockNumber,
        hash: block.hash,
        timestamp: new Date(parseInt(block.timestamp) * 1000).toLocaleString(),
        gasPrice: web3.utils.fromWei(gasPrice, 'gwei') + ' Gwei',
        transactions: block.transactions.length
      };
      
      console.log("Block details fetched:", blockInfo);
      
      // Set state
      setBlockDetails(blockInfo);
      setShowBlockDetails(true);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching block details:', error);
      setStatus('Failed to fetch blockchain stats: ' + error.message);
      setIsLoading(false);
    }
  };

  const handleFromAddressChange = async (e) => {
    const addr = e.target.value;
    setFromAddress(addr);
    if (web3 && addr) {
      try {
        setIsLoading(true);
        const bal = await web3.eth.getBalance(addr);
        setBalance(web3.utils.fromWei(bal, 'ether'));
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching balance:', error);
        setIsLoading(false);
      }
    }
  };

  const handleTransfer = async (e) => {
    e.preventDefault();
    
    if (!web3) {
      setStatus('Web3 not initialized');
      return;
    }
    
    if (!fromAddress || !toAddress || !amount) {
      setStatus('Please fill in all fields');
      return;
    }
    
    try {
      setIsLoading(true);
      setStatus('Transaction in progress...');
      setTransactionHash('');
      
      const weiAmount = web3.utils.toWei(amount, 'ether');
      
      // Send transaction
      const result = await web3.eth.sendTransaction({
        from: fromAddress,
        to: toAddress,
        value: weiAmount,
        gas: 21000
      });
      
      setTransactionHash(result.transactionHash);
      setStatus('Transaction successful!');
      setAmount('');
      
      // Refresh balance
      await refreshBalance();
    } catch (error) {
      console.error('Transaction error:', error);
      setStatus(`Transaction failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Decorative glowing elements */}
      <div className="glow glow-1"></div>
      <div className="glow glow-2"></div>
      <div className="glow glow-3"></div>
      
      <h1>Ethereum Transfer App</h1>
      
      {networkInfo && (
        <div className="network-badge">
          {networkInfo.name} • Block #{networkInfo.blockNumber}
          <button 
            onClick={handleViewStats} 
            className="block-info-button" 
            disabled={isLoading}
          >
            {isLoading ? '...' : 'View Stats'}
          </button>
        </div>
      )}
      
      <div className="card">
        {showBlockDetails && blockDetails && (
          <div className="block-details">
            <div className="block-details-header">
              <h3>Blockchain Statistics</h3>
              <button onClick={() => setShowBlockDetails(false)} className="close-button">×</button>
            </div>
            <div className="block-details-content">
              <div className="block-detail">
                <span>Block Number:</span>
                <span>{blockDetails.number}</span>
              </div>
              <div className="block-detail">
                <span>Block Hash:</span>
                <span className="mono">{blockDetails.hash}</span>
              </div>
              <div className="block-detail">
                <span>Timestamp:</span>
                <span>{blockDetails.timestamp}</span>
              </div>
              <div className="block-detail">
                <span>Gas Price:</span>
                <span>{blockDetails.gasPrice}</span>
              </div>
              <div className="block-detail">
                <span>Transactions:</span>
                <span>{blockDetails.transactions}</span>
              </div>
            </div>
          </div>
        )}
        
        {!web3 ? (
          <div className="error-message">
            Connecting to blockchain...
            <p>Make sure Anvil is running on http://127.0.0.1:8545</p>
          </div>
        ) : (
          <>
            <div className="balance-container">
              <h3>Account Balance</h3>
              <p className="balance">{balance}</p>
              <button 
                onClick={refreshBalance} 
                className="refresh-button"
                disabled={isLoading}
              >
                {isLoading ? 'Refreshing...' : 'Refresh'}
              </button>
            </div>
            
            <form onSubmit={handleTransfer} className="transfer-form">
              <div className="form-group">
                <label htmlFor="fromAddress" className="from-label">From Account:</label>
                <select
                  id="fromAddress"
                  value={fromAddress}
                  onChange={handleFromAddressChange}
                  required
                  disabled={isLoading}
                >
                  <option value="">Select account</option>
                  {accounts.map((account) => (
                    <option key={account} value={account}>
                      {account}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="toAddress" className="to-label">To Account:</label>
                <select
                  id="toAddress"
                  value={toAddress}
                  onChange={(e) => setToAddress(e.target.value)}
                  required
                  disabled={isLoading}
                >
                  <option value="">Select account</option>
                  {accounts.map((account) => (
                    <option key={account} value={account}>
                      {account}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="amount" className="amount-label">Amount (ETH):</label>
                <input
                  id="amount"
                  type="number"
                  step="0.000001"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  placeholder="0.0"
                  required
                  disabled={isLoading}
                />
              </div>
              
              <button 
                type="submit" 
                className="transfer-button"
                disabled={isLoading}
              >
                {isLoading ? 'Processing...' : 'Transfer ETH'}
              </button>
            </form>
            
            {status && (
              <div className={`status-message ${status.includes('failed') || status.includes('Failed') ? 'error' : ''}`}>
                {status}
                {transactionHash && (
                  <div className="transaction-hash">
                    TX: {transactionHash}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App 