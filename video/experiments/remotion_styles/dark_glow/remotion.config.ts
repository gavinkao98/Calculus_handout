import {Config} from '@remotion/cli/config';

Config.setEntryPoint('./src/index.ts');
Config.setVideoImageFormat('png'); // 暗部漸層與光暈：PNG 中間幀避免 JPEG 二次壓縮色帶
Config.setPixelFormat('yuv420p');
Config.setOverwriteOutput(true);
