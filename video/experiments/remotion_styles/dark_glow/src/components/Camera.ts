// Camera：不是 CSS scale，而是「世界座標 → 畫面 px」的映射。
// 推拉平移時線寬、光暈、字級維持恆定（像真的鏡頭移動，而不是把圖片放大）。
import {interpolate} from 'remotion';
import {ease, FRAME} from '../theme';

export type Cam = {cx: number; cy: number; zoom: number};
export type View = Cam & {
  unit: number; // zoom = 1 時 1 個世界單位的 px（等比例 x/y）
  ax: number; // 畫面錨點（相機中心在畫面上的位置）
  ay: number;
  X: (x: number) => number;
  Y: (y: number) => number;
  /** 世界長度 → px */
  L: (len: number) => number;
};

export const makeView = (cam: Cam, unit: number, ax = FRAME.width / 2, ay = FRAME.height / 2): View => {
  const k = unit * cam.zoom;
  return {
    ...cam,
    unit,
    ax,
    ay,
    X: (x) => ax + (x - cam.cx) * k,
    Y: (y) => ay - (y - cam.cy) * k,
    L: (len) => len * k,
  };
};

export type CamKey = Cam & {f: number};

/** 相機關鍵幀：段與段之間用 ease.camera 內插（慢起、長尾的推拉）。 */
export const cameraAt = (frame: number, keys: CamKey[], easing = ease.camera): Cam => {
  if (frame <= keys[0].f) return keys[0];
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i];
    const b = keys[i + 1];
    if (frame <= b.f) {
      const t = interpolate(frame, [a.f, b.f], [0, 1], {easing, extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      // zoom 用對數內插：推近時的感知速度才均勻
      const zoom = Math.exp(Math.log(a.zoom) + (Math.log(b.zoom) - Math.log(a.zoom)) * t);
      return {cx: a.cx + (b.cx - a.cx) * t, cy: a.cy + (b.cy - a.cy) * t, zoom};
    }
  }
  return keys[keys.length - 1];
};
