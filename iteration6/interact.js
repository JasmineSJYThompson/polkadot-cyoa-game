let provider, signer, contract;

const contractAddress = "0x1706BEA85Fc5E197d4e40c74Dd3ae31b40872a87";

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

async function saveInteger() {
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
    const tx = await contract.save(parseInt(value));
    document.getElementById("txStatus").innerText = "📤 Transaction sent... waiting for confirmation.";

    await tx.wait();
    document.getElementById("txStatus").innerText = `✅ Confirmed in block ${tx.blockNumber}`;
    await loadInteger(); // Automatically refresh the displayed value
  } catch (err) {
    console.error("Transaction failed:", err);
    document.getElementById("txStatus").innerText = "⚠️ Transaction failed. See console.";
  }
}

async function loadInteger() {
  if (!contract) {
    document.getElementById("output").innerText = "⛔ Connect to contract first.";
    return;
  }

  try {
    const value = await contract.load();
    document.getElementById("output").innerText = `📦 Most recent saved integer: ${value.toString()}`;
  } catch (err) {
    console.error("Error reading value:", err);
    document.getElementById("output").innerText = "⚠️ Error loading value.";
  }
}

async function loadAllIntegers() {
  if (!contract) {
    document.getElementById("allIntegersStatus").innerText = "⛔ Connect to contract first.";
    return;
  }

  try {
    const values = await contract.loadAll();
    document.getElementById("allIntegersStatus").innerText = `📦 All saved integers: ${values.join(', ')}`;
  } catch (err) {
    console.error("Error loading all integers:", err);
    document.getElementById("allIntegersStatus").innerText = "⚠️ Error loading all integers.";
  }
}

