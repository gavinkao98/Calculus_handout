/**
 * Page turn: the outgoing scene is a leaf hinged at the spine (left edge).
 * It lifts toward the lens and swings over (rotateY with perspective),
 * catching lamp light as it rises and darkening as it passes edge-on; the
 * incoming page below receives a soft moving shadow from the leaf.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { ease } from "../theme";
import { TURN } from "./timing";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Wraps the outgoing scene; `dur` is the scene length (the turn fills its last TURN frames). */
export const PageTurnOut: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [dur - TURN, dur], [0, 1], { ...clamp, easing: ease.camera });
  if (p <= 0) return <>{children}</>;
  const ang = -p * 96; // past 90°: the leaf is gone (backface hidden)
  const lift = Math.sin(Math.PI * Math.min(1, p * 1.1)); // 0 → 1 → 0
  return (
    <AbsoluteFill>
      {/* the leaf's shadow on the next page: a band that sweeps toward the spine */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(90deg, rgba(50,32,8,${0.28 * lift}) 0%, rgba(50,32,8,${0.12 * lift}) ${Math.max(4, 100 * (1 - p) * 0.9)}%, rgba(50,32,8,0) ${Math.max(8, 100 * (1 - p))}%)`,
        }}
      />
      <AbsoluteFill
        style={{
          transformOrigin: "0% 50%",
          transform: `perspective(4800px) rotateY(${ang}deg)`,
          backfaceVisibility: "hidden",
          boxShadow: `0 0 ${80 * lift}px rgba(40,25,5,${0.35 * lift})`,
        }}
      >
        {children}
        {/* light on the rising leaf, then shade as it goes edge-on */}
        <AbsoluteFill
          style={{
            background: `linear-gradient(90deg, rgba(255,250,235,${0.18 * lift}) 0%, rgba(40,25,5,${0.35 * p * p}) 100%)`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
