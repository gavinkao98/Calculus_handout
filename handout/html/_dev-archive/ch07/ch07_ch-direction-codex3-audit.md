# Ch7 章層方向閘（③）— Codex 對抗審裁決紀錄（raw JSON gitignored；本檔為版控轉錄）

2026-07-18。canon 變體 ③ 對 Codex 跑（gpt-5.6-terra／xhigh、read-only、output-schema）。
單輪收斂：**D1–D7 全數 agree／agree-with-modifications、0 prefer-alternative**；另 8 blocking＋5 advisory
獨立風險。Claude 逐條核驗後**全數採納**（含 D4 以 Codex 的顯式誤差估計取代原提案的 named fence——
數學上已由 Claude 獨立驗證）。收斂即定案（本對話使用者授權 Claude⇄Codex 收斂＝拍板）。

## D1–D7 裁決摘要（詳 PLAN-ch07「Chapter-level direction decisions」定案版）

| ID | verdict | 落地 |
|---|---|---|
| D1 roster | agree-w-mods | 七節全保留；**全章 worked-example 硬上限 23**；§7.4 恰 3 例、**§7.7 至多 2 例**（about-y-axis 與 u-sub 合一例）；Schwarz-lantern 不寫。依據=課程範圍（NTU 甲＝Stewart 1–10），非 sec-6-5 的承諾（那句只提 areas/volumes/arc lengths） |
| D2 積分 MVT | agree-w-mods | Def＋Thm 均明定 \(a<b\)；結論 \(c\in[a,b]\)；證明分 \(m=M\)（常數，任取 c）／\(m<M\)（令 \(\alpha=\min\{x_m,x_M\}\)、\(\beta=\max\{x_m,x_M\}\)，對 \([\alpha,\beta]\) 用 IVT 4.9(b)）；不把 Ch6 反向積分慣例套進平均值；FTC 路線至多一句（點名 Thm 6.3＋4.12） |
| D3 弧長 | agree-w-mods | Thm 寫 \(a<b\) 且 \(f\in C^1([a,b])\)，**就地定義該記號**（閉區間連續、內部可微、f′ 連續延伸至端點；端點單側）；Def=regular-partition 多邊形和的有限極限、\(a=b\) 時 \(L=0\)、不設反向慣例；術語=**graph arc length**，Ch10 參數式只 forward-ref |
| D4 表面積 | agree-w-mods | **棄 named uniform-continuity fence**（App D 無對應 entry＝無地址證明債）；改 **C¹ 顯式誤差估計當場證完**：\(K=\max\lvert f'\rvert\)、\(B=\max\sqrt{1+f'^2}\)（EVT），MVT 給 \(\lvert\frac{f(x_{i-1})+f(x_i)}{2}-f(\xi_i)\rvert\le K\Delta x\)，總替換誤差 \(\le 2\pi BK(b-a)\Delta x\to 0\)。統一 \(S=\int 2\pi\rho\,ds\)（繞 x 軸 \(\rho=f\ge0\)；繞 y 軸 \(0\le a<b\)、\(\rho=x\)）。frustum 幾何補 \(r_1=r_2\) cylinder 退化。frustum 先備=108 課綱 S-9 相似形/扇形/圓錐展開（A-class 短橋，展示不裸引） |
| D5 殼法 | agree-w-mods | Thm 陳述補 f continuous、f≥0、\(0\le a<b\)；「exact」只修飾**取高 \(f(\bar x_i)\) 的 approximating annular cylinder**，不得暗示原 solid 徑向帶等高；先明說 shell-stack model 再給 algebra；shifted-axis 例限區域全在軸一側、半徑寫 \(\lvert x-c\rvert\) |
| D6 選材 | **agree**（無 mod） | §7.4 三例（spring/cable/pump）SI 主、ft-lb 一提；no RMS；dropped 8.3–8.5 不回鍋 |
| D7 opener | agree-w-mods | schema＋Stewart 序保留；**學習成果 6 條→5 條**（SPEC §4 上限 3–5；弧長＋表面積合併一條） |

## 獨立風險（blocking 8——全數落地）

1. §7.5 未限 \(a<b\) 會除以零／反向積分混入；IVT 直接套「端點 x_m,x_M 的區間」漏次序與常數退化 → D2 修正案。
2. §7.6 弧長非有向量；b<a 慣例會給負值；C¹([a,b]) 與端點導數須精確 → D3 修正案。
3. §7.7 named fence 無 App D 實體 entry＝無地址證明債 → D4 直接證，fence 取消。
4. 完整球面 \([-r,r]\) 在兩極 \(f'\) 無界、不滿足 C¹ → 改 **spherical zone**（Claude 於 ③ 回覆前已自行同款修正——兩邊獨立收斂）；\(4\pi r^2\) 只作明確標示的 limiting preview。
5. frustum 相似錐相減推導除以 \(r_2-r_1\) 漏 \(r_1=r_2\)；而常數函數使每帶皆 cylinder＝核心退化 → 由 sector 得 \(\pi r\ell\) 再推 \(\pi(r_1+r_2)\ell\)；\(r_1=r_2\) 以展開矩形 \(2\pi r\ell\) 另驗。
6. 裸寫 \(S=\int 2\pi x\,ds\) 在 x<0 給負值；跨軸曲線兩側生成同面重疊計數 → 本章限曲線在軸一側（\(0\le a<b\)）；一律先寫 radius=distance to axis。
7. §7.3 midpoint 等式對原 solid 的徑向帶**不**精確（只對 approximating shell 精確）→ 措辭紀律（D5）。
8. 學習成果 6 條違反 SPEC 3–5 → 合併為 5。

## 獨立風險（advisory 5——全數採納）

9. perfect-square 弧長例 \(\sqrt{q^2}=\lvert q\rvert\) 判號紀律：鎖正區間、解中明寫絕對值展開；§7.7 例定案=\(y=x^2\)、\(x\in[0,1]\) 繞 y 軸（y-axis＋u-sub 一例兩用，恰合 D1 的 §7.7 併例）。
10. Hooke：\(F=kx\) 是 **applied force**（restoring=−kx）；Def 把 F 說成沿位移方向的 signed component；spring 例明講 work against the spring。cable 直接給 weight density N/m（勿混 kg/m）。
11. 「split at intersections」僅在交點有限時是有限步驟：一般公式=\(\int\lvert f-g\rvert\)；策略框措辭限定「本書例題交點皆有限」。
12. §7.5→Ch15 export 措辭改「average-value normalization＋一維 attainment template」（attainment 暗用區間連通性；Ch15 disconnected region 可能取不到）。
13. 術語限定 **graph** arc length／surface of **revolution**，不預先承諾 reparameterization invariance 或一般 surface theory（Ch10/Ch16 建）。

## overall

方向可採；七節 roster 與三個核心證明均有現成 machinery 支撐；不需退到 integral-definition 的表面積。
撰稿前修正上列 blockers（§7.5/§7.6 退化假設、§7.7 無地址 fence、y 軸半徑、球面 C¹）。
已具名例題（球面端點除外）皆不需 Ch8 技巧。

**落地動作（同日）：** PLAN-ch07 D1–D7 改定案版＋export 措辭修＋ledger 例數上限；sec-7-1.html
學習成果 6→5、crossing 措辭；briefs 7-3/7-4/7-5/7-6/7-7 對應更新。§7.1–§7.2 先行稿經對照：
除 opener bullets 外無違反收斂裁決處（§7.1 crossing 段補一子句）。
