/* ============================================================
   figures.js — 圖表登錄表（每章一份）。
   每個 <figure data-fig="id"> 會被 hydrateFigures(root) 自動填入
   對應的繪圖。圖中的座標軸、曲線、虛線、點都會繼承 skin-hs.css
   的圖形樣式（.axis / .curve / .refline / .dot），標籤用真正的
   \( … \) TeX，跟內文公式同一套字型（Computer Modern）。

   買賣合約：每個 entry 回傳 { layout, panels: [{ svg, note }] }
     layout : "single" | "pair" | "triple" | "grid"
     svg    : 用 buildPlot(cfg) 產生的 SVG 字串
     note   : 圖下的小字說明（可含 \( \) 數學，可省略）

   buildPlot(cfg) 常用欄位（完整見 shared/plot.js）：
     w, h                畫布像素寬高
     xmin,xmax,ymin,ymax 資料範圍
     items: [
       { type:"curve", fn:x=>..., domain:[a,b], samples:240, cls:"curve" }
       { type:"hline", y:1, from:-2, to:2, cls:"refline" }
       { type:"vline", x:1, from:-2, to:2, cls:"refline" }
       { type:"dot",  x:1, y:1, r:2.6 }
       { type:"text", x:1, y:1, tex:"f", cls:"a-curve",
                      anchor:"start|middle|end", vAnchor:"top|middle|bottom", dx:0, dy:0 }
     ]
   cls 對照：a-curve（藍/主色） a-ref（紅/虛線） a-ax（軸標） a-pt（點標）
   ============================================================ */
(function () {
  const FIGS = {

    /* 範例圖：把 data-fig="demo-parabola" 的 <figure> 換成這張圖。
       刪掉它、照樣式新增你自己的條目即可。 */
    "demo-parabola": () => ({
      layout: "single",
      panels: [{
        svg: buildPlot({
          w: 320, h: 240, xmin: -2.4, xmax: 2.4, ymin: -0.6, ymax: 4.2,
          xlabel: "x", ylabel: "y",
          aria: "The parabola y = x squared.",
          items: [
            { type: "curve", fn: (x) => x * x, domain: [-2, 2], cls: "curve" },
            { type: "dot", x: 1, y: 1 },
            { type: "text", x: 1.85, y: 3.6, tex: "y=x^2", cls: "a-curve", anchor: "start" },
            { type: "text", x: 1.06, y: 0.9, tex: "(1,1)", cls: "a-pt", anchor: "start", vAnchor: "top" },
          ],
        }),
        note: "範例圖 \u2014 拋物線 \\(y=x^2\\)。把這條登錄改成你需要的圖。",
      }],
    }),

    /* 並排兩張圖的寫法：layout:"pair"、panels 放兩個物件。
    "before-after": () => ({
      layout: "pair",
      panels: [
        { svg: buildPlot({ ... }), note: "左圖說明" },
        { svg: buildPlot({ ... }), note: "右圖說明" },
      ],
    }),
    */

  };

  /* ---- 以下不用動：把 FIGS 接到頁面（和正式版完全相同的實作） ---- */
  function hydrateFigures(root) {
    (root || document).querySelectorAll("[data-fig]").forEach((el) => {
      const def = FIGS[el.dataset.fig];
      if (!def || el.dataset.figDone) return;
      const { layout, panels } = def();
      let html;
      if (layout === "single" && panels.length === 1 && !panels[0].note) {
        html = `<div class="figure-art">${panels[0].svg}</div>`;
      } else {
        const cls = { pair: "figure-art--pair", triple: "figure-art--triple", grid: "figure-art--grid" }[layout] || "";
        html = `<div class="figure-art ${cls}">` +
          panels.map((p) => `<div class="fig-panel">${p.svg}${p.note ? `<div class="fig-note">${p.note}</div>` : ""}</div>`).join("") +
          `</div>`;
      }
      el.insertAdjacentHTML("afterbegin", html);
      el.dataset.figDone = "1";
    });
  }
  window.hydrateFigures = hydrateFigures;
})();
