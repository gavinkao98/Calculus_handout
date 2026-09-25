# §3.1 核心內容大綱（Derivatives of the Sine and Cosine Functions）

> 2026-09-25 由主對話從講義 `handout/latex/src/ch03/chapter3.tex` §3.1 提煉，給「無指引生成」實驗使用。
> **本檔只列要教的內容與數學事實，不規定講法、順序、畫面或篇幅。** 下列編號只是清單編號，不代表出場順序；「依賴」欄只標邏輯上的先後（證明 B 需要先有 A）。

## 1. 學完要會的

- 知道並會用 $\dfrac{d}{dx}\sin x=\cos x$、$\dfrac{d}{dx}\cos x=-\sin x$（$x$ 以弧度計）。
- 理解為什麼需要一個新的極限 $\lim_{\theta\to0}\dfrac{\sin\theta}{\theta}=1$，以及它怎麼證出來。
- 能用這兩個導數，加上第 2 章的規則，求出其餘四個三角函數的導數。

## 2. 內容清單

| # | 內容 | 數學事實 | 依賴 |
|---|---|---|---|
| C1 | 為什麼三角函數不一樣 | 多項式、$e^x$ 的差商都能用代數消掉分母的 $h$；$\dfrac{\sin(x+h)-\sin x}{h}$ 不行。整個計算最後歸結到單一極限 $\lim_{\theta\to0}\dfrac{\sin\theta}{\theta}$，屬 $0/0$ 型，代數解決不了，需要新工具：單位圓上的面積比較，再夾擠。全節角度一律用弧度。 | — |
| C2 | 和差化積改寫差商 | $\sin A-\sin B=2\cos\frac{A+B}{2}\sin\frac{A-B}{2}$（由和角公式展開 $\sin(u+v)-\sin(u-v)$ 得到）。取 $A=x+h$、$B=x$：$\dfrac{\sin(x+h)-\sin x}{h}=\cos\!\left(x+\tfrac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}$。$h\to0$ 時，第一個因子若 cos 連續則趨於 $\cos x$，第二個因子正是 $\frac{\sin\theta}{\theta}$、$\theta=h/2\to0$。所以導數取決於兩件事：sin、cos 的連續性，以及 $\lim\frac{\sin\theta}{\theta}$。 | C1 |
| C3 | 單位圓上的面積不等式 | 取 $0<\theta<\frac\pi2$，$A=(1,0)$、$B=(\cos\theta,\sin\theta)$、$C=(1,\tan\theta)$。內接三角形 $OAB$ 面積 $\frac12\sin\theta$ ≤ 扇形 $OAB$ 面積 $\frac12\theta$ ≤ 三角形 $OAC$ 面積 $\frac12\tan\theta$。所以 $\sin\theta\le\theta\le\tan\theta$，改寫得 $\cos\theta\le\dfrac{\sin\theta}{\theta}\le1$。$\frac{\sin\theta}{\theta}$ 是偶函數，只需看 $\theta>0$。副產品：$\lvert\sin\theta\rvert\le\lvert\theta\rvert$。 | C1 |
| C4 | sin、cos 的連續性 | 由 $\lvert\sin\theta\rvert\le\lvert\theta\rvert$ 與夾擠得 $\lim_{\theta\to0}\sin\theta=0$；再用和差化積得 $\lvert\sin x-\sin x_0\rvert\le2\lvert\sin\frac{x-x_0}{2}\rvert$、$\lvert\cos x-\cos x_0\rvert\le2\lvert\sin\frac{x-x_0}{2}\rvert$，右邊趨於 0，所以 sin、cos 處處連續。 | C3 |
| C5 | 基本極限 | $\lim_{\theta\to0}\dfrac{\sin\theta}{\theta}=1$：上界是常數 1，下界 $\cos\theta\to1$（cos 連續），夾擠；偶函數讓左右極限相同。 | C3、C4 |
| C6 | 兩個提醒 | (a) 這是極限，不是恆等式：$\theta=\frac\pi2$ 時比值是 $\frac2\pi\approx0.64$，$\theta=\pi$ 時是 0。(b) 必須用弧度：扇形面積 $\frac12\theta$ 靠弧度成立；若用度，$\lim_{x\to0}\frac{\sin(x^\circ)}{x}=\frac{\pi}{180}$，且 $\frac{d}{dx}\sin(x^\circ)=\frac{\pi}{180}\cos(x^\circ)$。 | C5 |
| C7 | 定理：sin 的導數 | $\dfrac{d}{dx}\sin x=\cos x$。證明：C2 的式子取極限，第一因子 $\to\cos x$（連續），第二因子 $\to1$（基本極限）。 | C2、C4、C5 |
| C8 | 定理：cos 的導數 | $\dfrac{d}{dx}\cos x=-\sin x$。用 $\cos A-\cos B=-2\sin\frac{A+B}{2}\sin\frac{A-B}{2}$：差商 $=-\sin\!\left(x+\tfrac h2\right)\cdot\dfrac{\sin(h/2)}{h/2}\to-\sin x$。 | C4、C5 |
| C9 | 圖形解讀 | 在同一個 $x$，$y=\sin x$ 的切線斜率等於 $y=\cos x$ 的高度。 | C7 |
| C10 | 例：伴隨極限 | $\lim_{\theta\to0}\dfrac{1-\cos\theta}{\theta}=0$：上下同乘 $1+\cos\theta$，得 $\dfrac{\sin\theta}{\theta}\cdot\dfrac{\sin\theta}{1+\cos\theta}\to1\cdot0=0$。 | C4、C5 |
| C11 | 例：其餘四個三角函數 | 商法則：$(\tan x)'=\sec^2x$、$(\sec x)'=\sec x\tan x$、$(\cot x)'=-\csc^2x$、$(\csc x)'=-\csc x\cot x$（在分母不為 0 處）。$\tan$ 的計算用到 $\cos^2x+\sin^2x=1$。 | C7、C8 |
| C12 | 例：彈簧上的重物 | 高度 $s(t)=\sin t$，速度 $s'(t)=\cos t$，加速度 $s''(t)=-\sin t=-s(t)$。$s''=-s$ 是簡諧運動的特徵：加速度永遠指回平衡位置，大小與離平衡的距離成正比。sin、cos 都滿足它。 | C7、C8 |
| C13 | 導數循環 | $\sin x\to\cos x\to-\sin x\to-\cos x\to\sin x$，四次回到原點，$\frac{d^4}{dx^4}\sin x=\sin x$。對照：$e^x$ 一步就回到自己；sin、cos 兩步變成自己的負值，也就是 C12 的 $s''=-s$。 | C7、C8 |
| C14 | 往下一節 | 目前只能微分「裸的」$\sin x$，還處理不了 $\sin(x^2)$、$\sin(3x+1)$ 這種函數套函數；下一節的連鎖律負責這件事。 | — |
