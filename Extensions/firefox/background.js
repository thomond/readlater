browser.contextMenus.create({
  id: "send-url",
  title: "Read Later...",
  contexts: ["link"]
});

browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "send-url") {
    const url = info.linkUrl;
    const data = JSON.stringify({ url: url });
    fetch("http://localhost:5000/add", {
      method: "POST",
      body: data,
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      console.log("Response:", response);
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
});

browser.browserAction.onClicked.addListener(() => {
  browser.browserAction.openPopup();
});
