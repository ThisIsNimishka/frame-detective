"""app/templates/base.py — HTML shell for Frame Detective."""

from .styles  import CSS
from .scripts import SHARED_JS


def base(title: str, body: str, extra_js: str = "") -> str:
    """Return a full HTML page. SHARED_JS loads BEFORE extra_js or inline scripts."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Frame Detective — Intel PresentMon learning game">
<title>{title} | Frame Detective</title>
<style>
{CSS}
/* streak bump */
#hud-streak.bump {{
  animation: bump .35s cubic-bezier(.16,1,.3,1);
}}
@keyframes bump {{
  0%   {{ transform:scale(1); }}
  35%  {{ transform:scale(1.8); color:var(--yellow); }}
  100% {{ transform:scale(1); }}
}}
</style>
</head>
<body>
<canvas id="bgcanvas"></canvas>
<div id="page-veil"></div>
{body}
<script>
/* ── SHARED GAME ENGINE ── (loaded first, before any page script) */
{SHARED_JS}

/* ── AMBIENT BACKGROUND GLOW ── */
(function() {{
  var cv  = document.getElementById('bgcanvas');
  if (!cv) return;
  var ctx = cv.getContext('2d');
  var pulse = 0;
  function draw() {{
    cv.width  = window.innerWidth;
    cv.height = window.innerHeight;
    ctx.clearRect(0, 0, cv.width, cv.height);
    
    pulse += 0.01;
    var opacity = 0.05 + Math.sin(pulse) * 0.02;
    
    // Draw a subtle radial gradient
    var grad = ctx.createRadialGradient(
      cv.width/2, cv.height/2, 0,
      cv.width/2, cv.height/2, cv.width * 0.8
    );
    grad.addColorStop(0, 'rgba(0, 229, 255, ' + opacity + ')');
    grad.addColorStop(1, 'transparent');
    
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, cv.width, cv.height);
    requestAnimationFrame(draw);
  }}
  draw();
}})();

/* ── INIT HUD + TYPEWRITER ── */
renderHUD();
initTypewriters();

/* ── PAGE JS ── */
{extra_js}
</script>
</body>
</html>"""
