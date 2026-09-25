// 字型全部來自 bundle 內的 @fontsource（開放授權），render 時不連網。
// 載入完成前以 delayRender 擋住截圖。
import {continueRender, delayRender} from 'remotion';
import '@fontsource/cormorant-garamond/400.css';
import '@fontsource/cormorant-garamond/500.css';
import '@fontsource/cormorant-garamond/400-italic.css';
import '@fontsource/cormorant-garamond/500-italic.css';
import '@fontsource/dm-mono/300.css';
import '@fontsource/dm-mono/400.css';
// 以下僅供品牌 lockup 內建的 <text>（lockup-white.svg 指定 Noto Sans TC／Inter）
import '@fontsource/noto-sans-tc/500.css';
import '@fontsource/noto-sans-tc/700.css';
import '@fontsource/noto-sans-tc/900.css';
import '@fontsource/inter/700.css';

const LOCKUP_TEXT = '國立臺灣大學｜北區高中學生科學研究人才培育計畫數學組';
const SAMPLE = 'AaBbSsCcDdHhow fast does sine change? §3.1 0123456789 −+=.';

const handle = delayRender('Loading fonts');
Promise.all([
  document.fonts.load('400 64px "Cormorant Garamond"', SAMPLE),
  document.fonts.load('500 64px "Cormorant Garamond"', SAMPLE),
  document.fonts.load('italic 400 64px "Cormorant Garamond"', SAMPLE),
  document.fonts.load('italic 500 64px "Cormorant Garamond"', SAMPLE),
  document.fonts.load('300 32px "DM Mono"', SAMPLE),
  document.fonts.load('400 32px "DM Mono"', SAMPLE),
  document.fonts.load('500 22px "Noto Sans TC"', LOCKUP_TEXT),
  document.fonts.load('700 24px "Noto Sans TC"', LOCKUP_TEXT),
  document.fonts.load('900 40px "Noto Sans TC"', LOCKUP_TEXT),
  document.fonts.load('700 22px "Inter"', 'NTU'),
])
  .then(() => continueRender(handle))
  .catch((err) => {
    console.error(err);
    continueRender(handle);
  });
