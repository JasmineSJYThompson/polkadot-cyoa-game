let provider, signer, contract;
const contractAddress = "0x1F6d953ca48Fb7cB90117F63BDD80c5f5c519830";
let currentSceneId = "0"; // Default starting scene

// Load ABI from contract.json
async function loadABI() {
  const res = await fetch('contract.json');
  const json = await res.json();
  return json.abi;
}

// Connect to MetaMask and initialize contract
async function connect() {
  if (!window.ethereum) {
    alert("MetaMask not found. Please install it.");
    return;
  }

  const abi = await loadABI();
  provider = new ethers.providers.Web3Provider(window.ethereum);
  await provider.send("eth_requestAccounts", []);
  signer = provider.getSigner();
  contract = new ethers.Contract(contractAddress, abi, signer);

  document.getElementById("output").innerText = "✅ Connected to MetaMask.";
  navigateScene(currentSceneId);
}

// Save the current scene ID to the blockchain
async function saveScene() {
  if (!contract) {
    alert("⛔ Not connected to the contract.");
    return;
  }

  try {
    const tx = await contract.store(parseInt(currentSceneId));
    document.getElementById("txStatus").innerText = "📤 Saving scene... waiting for confirmation.";
    await tx.wait();
    document.getElementById("txStatus").innerText = `✅ Scene saved in block ${tx.blockNumber}`;
  } catch (err) {
    console.error("Transaction failed:", err);
    document.getElementById("txStatus").innerText = "⚠️ Transaction failed. See console.";
  }
}

// Load the saved scene ID from the blockchain
async function loadScene() {
  if (!contract) {
    alert("⛔ Not connected to the contract.");
    return;
  }

  try {
    const sceneId = await contract.retrieve();
    currentSceneId = sceneId.toString();
    navigateScene(currentSceneId);
  } catch (err) {
    console.error("Error reading value:", err);
    document.getElementById("output").innerText = "⚠️ Error reading value.";
  }

const scenes = {
    "0": {
      description: "🧙 You awaken in a moss-covered stone circle. Fog drips from twisted trees. A raven stares.\nYour only belongings: a rusty dagger, a torn map, and a faint headache that feels... cursed.",
      choices: {
        "Examine the map": "1",
        "Talk to the raven": "2",
        "Walk into the forest": "3"
      }
    },
    "1": {
      description: "📜 The map shows a ruin labeled 'Whispering Vault' and a trail marked with cryptic runes.",
      choices: {
        "Follow the trail": "3",
        "Return to the stone circle": "0"
      }
    },
    "2": {
      description: "🪶 The raven cocks its head. In a raspy human voice it says: 'Three paths, one truth. Don't trust the smiling god.'",
      choices: {
        "Demand more answers": "4",
        "Back away slowly": "0"
      }
    },
    "3": {
      description: "🌲 The forest path splits ahead. One way leads to light and laughter. The other, to silence and cold shadows.",
      choices: {
        "Take the bright path": "5",
        "Take the dark path": "6"
      }
    },
    "4": {
      description: "🦉 The raven screeches and bursts into black feathers. A silver key is left behind.",
      choices: {
        "Take the key and head to the forest": "3"
      }
    },
    "5": {
      description: "🌞 Warm light filters through golden leaves. You hear music, distant and cheerful. A small cottage lies ahead.\nAn old man sits outside, whittling a flute from bone. His smile doesn't reach his eyes.",
      choices: {
        "Speak to the old man": "7",
        "Ignore him and walk past": "END"
      }
    },
    "6": {
      description: "🌑 The air grows colder. Trees groan like dying things. You find a ruined shrine where an old man in rags tends a flickering blue flame.\nHis eyes are milky, but he speaks before you do: 'I saw you in the ashes.'",
      choices: {
        "Ask what he means": "8",
        "Back away into the forest": "END"
      }
    },
    "7": {
      description: "🎵 The old man chuckles. 'So you've heard the laughter too. Most think it's the fairfolk — it's not.'\n'The Whispering Vault opens soon. When it does, not even gods will sleep safe.'",
      choices: {
        "Ask about the Whispering Vault": "END"
      }
    },
    "8": {
      description: "🕯 The blind man dips his finger into the blue flame and draws a sigil in the air. It burns into your vision.\n'You were marked at birth. The Vault remembers. And it waits.'",
      choices: {
        "Stare into the flame": "END"
      }
    },
};

// Navigate to a specific scene
function navigateScene(sceneNumber) {
  currentSceneId = sceneNumber;
  const scene = scenes[sceneNumber];

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
    button.onclick = () => navigateScene(nextSceneId);
    choicesDiv.appendChild(button);
  }
}

