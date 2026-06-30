# _fixture_pedagogy — pedagogy-firstlearner calibration content script (test-only)

> **階段：** LOCKED（fixture，calibration baseline；`CONTENT_APPROVED=yes`）。本檔是 `pedagogy-firstlearner` 閘的校準源（approved deck），純供 `pedagogy_audit.yml` 的 `md:<unit>` ref 解析與 gate-1 agent 判 OF1 之用，不進任何真實渲染。各單元的 `narration:`／`learning_goal:` 刻意造成「忠實 / 過窄 / 過寬」三種角色，給 agent 真實可判的源文字。

### unit: unit_squeeze
```
id: unit_squeeze
source: fixture (squeeze bound for sin θ / θ)
learning_goal: 用幾何不等式夾出 lim_{θ→0} (sin θ)/θ = 1（first-learner 主力源）
kind: content
narration: |
  對 0 < θ < π/2，比較三塊面積——內接三角形、扇形、外切三角形——
  得到 sin θ < θ < tan θ。三邊同除以 sin θ（θ 為正，不等號方向不變）得
  1 < θ/(sin θ) < 1/(cos θ)，取倒數翻向得到夾擠不等式
  cos θ ≤ (sin θ)/θ ≤ 1。當 θ → 0 時 cos θ → 1，由夾擠定理 (sin θ)/θ → 1。
  這個推導的每一步都是承重的：面積比較給出原始不等式，同除 sin θ 與取倒數
  是兩個各自獨立的代數動作，最後才是取極限。
visual_need: 三塊面積（三角形/扇形/三角形）疊在單位圓上，逐塊上色比較
animation_cue: 先畫單位圓與角 θ，再依序填三塊面積，最後並排三條不等式
```

### unit: unit_narrow
```
id: unit_narrow
source: fixture (narrow claim — single-point statement only)
learning_goal: 只陳述 lim_{θ→0} (sin θ)/θ = 1 這一個結果，不延伸
kind: content
narration: |
  (sin θ)/θ 在 θ → 0 的極限等於 1。本單元只給這一個極限值本身，
  不討論 (1 − cos θ)/θ，也不對任何 θ ≠ 0 的點下結論，更不主張
  (sin θ)/θ 在整個區間上單調或有界。這裡就只有 θ → 0 這一個點的極限。
visual_need: 單一極限式置中
animation_cue: 淡入極限式
```

### unit: unit_broad
```
id: unit_broad
source: fixture (broad cross-unit synthesis — covers loosely, states nothing specific)
learning_goal: 綜述「三角函數的小角行為」這一大主題，不落到任一條具體子斷言
kind: content
narration: |
  本單元是一段跨單元的總覽：三角函數在小角度附近有許多有用的近似與極限，
  它們合起來支撐了正弦、餘弦導數的推導，也連到後面的泰勒展開與物理上的
  小角近似。這裡談的是「整體圖像為何重要、彼此如何串接」，刻意停在主題層，
  不寫出任何一條特定的等式或不等式——例如不在此給 (1 − cos θ)/θ → 0 的值，
  也不給 cos θ ≤ (sin θ)/θ ≤ 1 的具體界，那些具體子斷言各有其專屬單元。
visual_need: 小角主題的概念地圖（節點＋連線，無公式）
animation_cue: 節點逐一亮起並連線，全程不出現具體公式
```

### unit: unit_two
```
id: unit_two
source: fixture (two distinct concepts, both faithfully stated)
learning_goal: 同時陳述兩個各自獨立的結果，供 L2-territory 邊界場引用
kind: content
narration: |
  本單元明確陳述兩個彼此獨立的結果。其一：lim_{θ→0} (sin θ)/θ = 1。
  其二：lim_{θ→0} (1 − cos θ)/θ = 0。兩者都由前面的夾擠論證與
  半角恆等式各自得到，是兩個分開的教學概念，但本單元把兩者都完整講清楚。
visual_need: 兩條極限式上下並列
animation_cue: 兩式先後淡入
```

### unit: unit_recap
```
id: unit_recap
source: fixture (innocuous recap takeaways)
learning_goal: 收束本段的兩三條重點，供 recap_cards 場引用
kind: content
narration: |
  回顧本段：我們用面積比較夾出了 (sin θ)/θ → 1，並把推導拆成
  面積比較、同除 sin θ、取倒數、取極限四個承重步驟。記得 θ 必須以
  弧度量，否則弧長 = θ 這一步不成立。這些都是後面算正弦、餘弦導數的基石。
visual_need: 三張重點卡
animation_cue: 重點卡逐張翻出
```
