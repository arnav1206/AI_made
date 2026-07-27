// background.js — Formitra Extension Service Worker

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "formitra_dictate_field",
    title: "🎙️ Dictate with Formitra for this field",
    contexts: ["editable"]
  });
  console.log("Formitra Extension installed successfully.");
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "formitra_dictate_field" && tab && tab.id) {
    chrome.tabs.sendMessage(tab.id, { action: "TRIGGER_FIELD_DICTATION" });
  }
});
