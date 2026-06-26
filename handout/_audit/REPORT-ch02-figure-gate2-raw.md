**Gate 2 圖稽核報告**

母體核對：Chapter 2 `<figure>` 共 10 張，與使用者列出的 8 張 FIGS + 2 張 inline-SVG 一致。

1. `secant-to-tangent`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 以 \(f(x)=0.1x^2+0.5\)、\(c=1\)、\(f'(c)=0.2\)、\(Q_1,Q_2,Q_3=(7,5,3)\) 繪製；割線斜率 \(0.8,0.6,0.4\) 收斂到切線，caption 一致。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:1813>)。

2. `difference-quotient-anatomy`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 設 \(a=1.5,h=2.5,b=a+h=4\)，水平腿標 \(h\)，垂直腿標 \(f(a+h)-f(a)\)，與 §2.1 h-form prose 一致。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:2097>)。

3. `tangent-approx`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：圖示 \(y=1/x\) 在 \((2,\tfrac12)\) 的切線 \(y=-0.25x+1\)，tick 與 Example 2.5 相符；無標籤遮擋或裁切。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:1881>)。

4. `f-and-fprime`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：上圖 \(f=x^2+4x-2\) 最小點 \((-2,-6)\)，下圖 \(f'=2x+4\) 於 \(x=-2\) 為 0；共同垂直線、正負號標示與 caption 一致。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:1958>)。

5. `fig-diff-cont`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：inline-SVG 外層 dashed ellipse 為 `Continuous`，內層 ellipse 為 `Differentiable`，`|x| at x = 0` 放在內層外、外層內，符合 Theorem 2.1 與後續 caution。來源：[sec-2-3.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/fragments/ch02/sec-2-3.html:120>)。

6. `abs-corner`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 繪 \(y=|x|\)，右側 secant 斜率 \(+1\)、左側 \(-1\)，caption 與 Example 2.11 prose 一致；線型與標籤足以灰階辨識。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:1912>)。

7. `cbrt-vertical-tangent`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 繪 \(y=\sqrt[3]{x}\)，割線點 \(x=2.6,1.0,0.35\) 的斜率依 \(x^{-2/3}\) 增大，正確表達 slope \(\to\infty\)。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:2068>)。

8. `exp-self-derivative`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 繪 \(y=e^x\)，切線 \(x=0\) 為 \(y=x+1\)、\(x=1\) 為 \(y=ex\)，標示 slope \(=1=e^0\)、slope \(=e=e^1\) 正確。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:1998>)。

9. `fig-product-area`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：inline-SVG 以 base \(fg\)、右 strip、上 strip、corner 分區；邊長標 \(f,\Delta f,g,\Delta g\)，與 Figure 2.4 caption/prose 一致。來源：[sec-2-5.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/fragments/ch02/sec-2-5.html:55>)。

10. `quotient-example-graph`  
`VERDICT: 0 blocking, 0 advisory`  
Findings: 無。  
D1–D8 乾淨：FIGS 繪 \(f(x)=x/(x^2+1)\) 與 \(f'(x)=(1-x^2)/(x^2+1)^2\)，頂點/谷點 \((\pm1,\pm\tfrac12)\)、\(f'(\pm1)=0\)、\(f'(0)=1\) 均與 Example 2.20 一致。來源：[chapter2-print-standalone.html](<C:/Users/Kao/Downloads/Calculus_handout/handout/chapter2-print-standalone.html:2027>)。

**全章彙總**

總 blocking 數：0。  
總 advisory 數：0。  
Figure gate 2：通過（blocking = 0）。