let scenes = {};
let currentSceneId = "0"; // Default starting scene

// Fetch scenes from scenes.json
async function loadScenes() {
  try {
    const response = await fetch('scenes.json');
    const data = await response.json();
    scenes = data.scenes;
    navigateScene(currentSceneId);
  } catch (error) {
    console.error("Error loading scenes:", error);
  }
}

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

// Restart the story
document.getElementById("restartButton").addEventListener("click", () => {
  currentSceneId = "0"; // Starting scene ID
  navigateScene(currentSceneId);
});

// Load scenes when the page is ready
document.getElementById("loadSceneButton").addEventListener("click", loadScenes);

