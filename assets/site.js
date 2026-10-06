// 複製按鈕 + 標示目前頁面
document.querySelectorAll("pre").forEach((pre) => {
  const b = document.createElement("button");
  b.className = "copy"; b.type = "button"; b.textContent = "複製";
  b.addEventListener("click", async () => {
    const text = pre.querySelector("code")?.innerText ?? pre.innerText;
    try { await navigator.clipboard.writeText(text.replace(/\n$/, "")); b.textContent = "已複製"; }
    catch { b.textContent = "請手動選取"; }
    setTimeout(() => (b.textContent = "複製"), 1600);
  });
  pre.appendChild(b);
});
const here = location.pathname.split("/").pop() || "index.html";
document.querySelectorAll(".nav-in a.l").forEach((a) => {
  if (a.getAttribute("href") === here) a.setAttribute("aria-current", "page");
});
