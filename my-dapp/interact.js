let provider, signer, contract;

const contractAddress = "0x1F6d953ca48Fb7cB90117F63BDD80c5f5c519830";

async function loadABI() {
  const res = await fetch('contract.json');
  const json = await res.json();
  return json.abi; // 👈 this fixes it!
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
  document.getElementById("output").innerText = "Connected to MetaMask and contract loaded.";
}

async function getValue() {
  if (!contract) {
    document.getElementById("output").innerText = "Please connect first.";
    return;
  }

  try {
    const value = await contract.retrieve();
    document.getElementById("output").innerText = `Stored value: ${value.toString()}`;
  } catch (err) {
    console.error(err);
    document.getElementById("output").innerText = "Error reading value.";
  }
}

