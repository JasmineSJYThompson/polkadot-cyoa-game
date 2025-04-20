let provider, signer, contract;

const contractAddress = "0x1F6d953ca48Fb7cB90117F63BDD80c5f5c519830";

async function loadABI() {
  const res = await fetch('contract.json');
  const json = await res.json();
  return json.abi;
}

async function connect() {
  if (!window.ethereum) {
    alert("MetaMask not found. Install it first.");
    return;
  }

  const abi = await loadABI();

  provider = new ethers.providers.Web3Provider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  signer = provider.getSigner();

  contract = new ethers.Contract(contractAddress, abi, signer);
  document.getElementById("output").innerText = "✅ Connected to MetaMask and contract loaded.";
}

async function sendNumber() {
  const input = document.getElementById("numberInput");
  const value = input.value;

  if (!contract) {
    document.getElementById("txStatus").innerText = "⛔ Not connected to contract.";
    return;
  }

  if (!value || isNaN(value)) {
    alert("Please enter a valid number");
    return;
  }

  try {
    const tx = await contract.store(parseInt(value));
    document.getElementById("txStatus").innerText = "📤 Transaction sent... waiting for confirmation.";

    await tx.wait();
    document.getElementById("txStatus").innerText = `✅ Confirmed in block ${tx.blockNumber}`;
    await getValue(); // 🔄 Automatically refresh the displayed value
  } catch (err) {
    console.error("Transaction failed:", err);
    document.getElementById("txStatus").innerText = "⚠️ Transaction failed. See console.";
  }
}

async function getValue() {
  if (!contract) {
    document.getElementById("output").innerText = "⛔ Connect to contract first.";
    return;
  }

  try {
    const value = await contract.retrieve();
    document.getElementById("output").innerText = `📦 Stored value: ${value.toString()}`;
  } catch (err) {
    console.error("Error reading value:", err);
    document.getElementById("output").innerText = "⚠️ Error reading value.";
  }
}

