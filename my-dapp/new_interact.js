let scenes = {};
let currentSceneId = "0"; // default start scene

async function loadScenes() {
  try {
    const response = await fetch('scenes.json');
    const data = await response.json();
    scenes = data.scenes;
    navigateScene(currentSceneId);
  } catch (error) {
    console.error("Failed to load scenes:", error);
  }
}

function navigateScene(sceneId) {
  const scene = scenes[sceneId];
  if (!scene) {
    document.getElementById("output").innerText = "⚠️ Scene not found.";
    return;
  }

  document.getElementById("output").innerText = scene.description;

  const choicesDiv = document.getElementById("choices");
  choicesDiv.innerHTML = '';

  for (const [choiceText, nextSceneId] of Object.entries(scene.choices)) {
    const button = document.createElement("button");
    button.innerText = choiceText;
    button.onclick = () => {
      currentSceneId = nextSceneId;
      navigateScene(currentSceneId);
    };
    choicesDiv.appendChild(button);
  }
}

let provider, signer, contract;

const contractAddress = "0x1F6d953ca48Fb7cB90117F63BDD80c5f5c519830";

// Load the ABI dynamically from the contract.json
async function loadABI() {
  const res = await fetch('contract.json');
  const json = await res.json();
  return json.abi;
}

// Connect to MetaMask and the smart contract
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

// Save the current scene to the smart contract
async function saveScene() {
  const sceneNumber = document.getElementById("numberInput").value;

  if (!sceneNumber || isNaN(sceneNumber)) {
    alert("Please enter a valid scene number.");
    return;
  }

  if (!contract) {
    document.getElementById("txStatus").innerText = "⛔ Not connected to contract.";
    return;
  }

  try {
    const tx = await contract.store(parseInt(sceneNumber));
    document.getElementById("txStatus").innerText = "📤 Transaction sent... waiting for confirmation.";
    await tx.wait();
    document.getElementById("txStatus").innerText = `✅ Scene saved with number ${sceneNumber} in block ${tx.blockNumber}.`;
  } catch (err) {
    console.error("Transaction failed:", err);
    document.getElementById("txStatus").innerText = "⚠️ Transaction failed. See console.";
  }
}

// Load the saved scene from the smart contract
async function loadScene() {
  if (!contract) {
    document.getElementById("txStatus").innerText = "⛔ Not connected to contract.";
    return;
  }

  try {
    const storedScene = await contract.retrieve();
    document.getElementById("output").innerText = `📦 Loaded scene number: ${storedScene.toString()}`;
  } catch (err) {
    console.error("Error loading scene:", err);
    document.getElementById("output").innerText = "⚠️ Error loading scene.";
  }
}

// Restart the game (reset to the first scene)
document.getElementById("restartButton").addEventListener("click", () => {
  // Reset to the first scene (can change to a specific starting scene ID if necessary)
  currentSceneId = "0"; // Starting scene ID
  navigateScene(currentSceneId);
});

// Navigate to a specific scene
function navigateScene(sceneId) {
  const scene = scenes[sceneId];
  if (!scene) {
    document.getElementById("output").innerText = "⚠️ Scene not found.";
    return;
  }

  document.getElementById("output").innerText = scene.description;
  const choicesDiv = document.getElementById("choices");
  choicesDiv.innerHTML = '';

  for (const [choiceText, nextSceneId] of Object.entries(scene.choices)) {
    const button = document.createElement("button");
    button.innerText = choiceText;
    button.onclick = () => {
      currentSceneId = nextSceneId;
      navigateScene(currentSceneId);
    };
    choicesDiv.appendChild(button);
  }
}

// Load scenes when the page is ready
document.getElementById("loadSceneButton").addEventListener("click", loadScenes);
