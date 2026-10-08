from PIL import Image

p = 'android/app/src/main/AndroidManifest.xml'
s = open(p, encoding='utf-8').read()
if 'sensorLandscape' not in s:
    s = s.replace('android:launchMode="singleTask"',
                  'android:launchMode="singleTask"\n            android:screenOrientation="sensorLandscape"', 1)
open(p, 'w', encoding='utf-8').write(s)

open('android/app/src/main/java/com/stickman/kombat/MainActivity.java', 'w', encoding='utf-8').write('''package com.stickman.kombat;

import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        ocultarBarras();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) ocultarBarras();
    }

    private void ocultarBarras() {
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        View decor = getWindow().getDecorView();
        WindowInsetsControllerCompat c = new WindowInsetsControllerCompat(getWindow(), decor);
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }
}
''')

src = Image.open('www/icon-512.png').convert('RGB')
for d, sz in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
    base = f'android/app/src/main/res/mipmap-{d}/'
    src.resize((sz, sz), Image.LANCZOS).save(base + 'ic_launcher.png')
    src.resize((sz, sz), Image.LANCZOS).save(base + 'ic_launcher_round.png')
    fg = int(sz * 108 / 48)
    f = Image.new('RGBA', (fg, fg), (0, 0, 0, 0))
    inner = src.resize((int(fg * 0.6), int(fg * 0.6)), Image.LANCZOS).convert('RGBA')
    f.paste(inner, ((fg - inner.width) // 2, (fg - inner.height) // 2))
    f.save(base + 'ic_launcher_foreground.png')

b = 'android/app/src/main/res/values/ic_launcher_background.xml'
t = open(b, encoding='utf-8').read().replace('#FFFFFF', '#040710')
open(b, 'w', encoding='utf-8').write(t)
