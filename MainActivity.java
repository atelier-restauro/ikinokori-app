package jp.ikinokori.app;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.WebView;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

// ・通知バー・ナビゲーションバーを隠す（上からスワイプすると一時的に出る）
// ・カメラの切り欠き（ノッチ・パンチホール）の分だけ、ゲーム画面を下げる（Android 15 以降は画面が切り欠きの裏まで広がるため）
// ・端末の「文字の大きさ」設定で画面が崩れないよう、文字の拡大は 100% に固定
public class MainActivity extends BridgeActivity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    if (Build.VERSION.SDK_INT >= 28) {
      getWindow().getAttributes().layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
    }
    getWindow().getDecorView().setBackgroundColor(0xFF0B0704);
    try {
      WebView wv = getBridge().getWebView();
      wv.getSettings().setTextZoom(100);
      ViewCompat.setOnApplyWindowInsetsListener(wv, (v, insets) -> {
        Insets cut = insets.getInsets(WindowInsetsCompat.Type.displayCutout());
        ViewGroup.LayoutParams p = v.getLayoutParams();
        if (p instanceof ViewGroup.MarginLayoutParams) {
          ViewGroup.MarginLayoutParams m = (ViewGroup.MarginLayoutParams) p;
          if (m.topMargin != cut.top || m.bottomMargin != cut.bottom || m.leftMargin != cut.left || m.rightMargin != cut.right) {
            m.setMargins(cut.left, cut.top, cut.right, cut.bottom);
            v.setLayoutParams(m);
          }
        }
        return WindowInsetsCompat.CONSUMED;
      });
    } catch (Exception e) { }
    hideBars();
  }

  @Override
  public void onResume() {
    super.onResume();
    hideBars();
  }

  @Override
  public void onWindowFocusChanged(boolean hasFocus) {
    super.onWindowFocusChanged(hasFocus);
    if (hasFocus) hideBars();
  }

  private void hideBars() {
    WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
    WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
    c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    c.hide(WindowInsetsCompat.Type.systemBars());
  }
}
