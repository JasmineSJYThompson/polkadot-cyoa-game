import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Storage Contract UI", page_icon="📦", layout="centered")
st.title("🧠 Ethereum Storage Contract")

# Inject ethers.js + contract interaction UI
components.html("""
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.umd.min.js"></script>
  </head>
  <body>
    <h3>Connect Wallet & Interact</h3>
    <button onclick="connect()">🔌 Connect Wallet</button>
    <p id="wallet"></p>
    
    <h4>📥 Retrieve Stored Value</h4>
    <button onclick="getValue()">🔍 Get Value</button>
    <p id="value"></p>

    <h4>📤 Store a New Value</h4>
    <input type="number" id="inputValue" placeholder="Enter new value"/>
    <button onclick="setValue()">💾 Store Value</button>
    <p id="storeStatus"></p>

    <script>
      let signer;
      const contractAddress = "0x46b77bcf67b6ceb25dc786efee998e69fae60d2a";
      const abi = [
        {
          "inputs": [{"internalType": "uint256","name": "num","type": "uint256"}],
          "name": "store",
          "outputs": [],
          "stateMutability": "nonpayable",
          "type": "function"
        },
        {
          "inputs": [],
          "name": "retrieve",
          "outputs": [{"internalType": "uint256","name": "","type": "uint256"}],
          "stateMutability": "view",
          "type": "function"
        }
      ];

      async function connect() {
        if (window.ethereum) {
          try {
            await ethereum.request({ method: 'eth_requestAccounts' });
            const provider = new ethers.providers.Web3Provider(window.ethereum);
            signer = provider.getSigner();
            const address = await signer.getAddress();
            document.getElementById("wallet").innerText = "✅ Connected: " + address;
          } catch (err) {
            document.getElementById("wallet").innerText = "❌ Wallet connection failed.";
            console.error(err);
          }
        } else {
          alert("🦊 Please install MetaMask!");
        }
      }

      async function getValue() {
        try {
          const provider = new ethers.providers.Web3Provider(window.ethereum);
          const contract = new ethers.Contract(contractAddress, abi, provider);
          const value = await contract.retrieve();
          document.getElementById("value").innerText = "Stored Value: " + value;
        } catch (err) {
          document.getElementById("value").innerText = "❌ Error reading value.";
          console.error(err);
        }
      }

      async function setValue() {
        try {
          const contract = new ethers.Contract(contractAddress, abi, signer);
          const input = document.getElementById("inputValue").value;
          const tx = await contract.store(input);
          document.getElementById("storeStatus").innerText = "⏳ Transaction sent. Waiting...";
          await tx.wait();
          document.getElementById("storeStatus").innerText = "✅ Stored successfully!";
        } catch (err) {
          document.getElementById("storeStatus").innerText = "❌ Transaction failed.";
          console.error(err);
        }
      }
    </script>
  </body>
</html>
""", height=600)

