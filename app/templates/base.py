"""
app/templates/base.py
---------------------
Base HTML shell. Every page calls base(title, body, extra_js="")
to get a complete self-contained HTML string.

FIX: renderHUD() and initTypewriters() now called at the END of the
     closing <script> block after ALL JS is defined — fixing the
     "XP doesn't work" bug where inline script ran before functions existed.
"""

from .styles  import CSS
from .scripts import SHARED_JS


def base(title: str, body: str, extra_js: str = "") -> str:
    """Return a full HTML page string."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <title>{title} — Frame Detective</title>
  <style>{CSS}</style>
</head>
<body>
  <canvas id="bgcanvas"></canvas>
  <div id="page-veil"></div>
  <div id="scan-sweep"></div>
  {body}
  <script>
    /* ── SHARED JS (state, utils, sound) ── */
    {SHARED_JS}

    /* ── PAGE JS ── */
    {extra_js}

    /* ── CANVAS STARFIELD (runs after all JS defined) ── */
    (function() {{
      var canvas = document.getElementById('bgcanvas');
      if (!canvas) return;
      var ctx = canvas.getContext('2d');
      var W, H;
      var stars = [], comets = [];

      function resize() {{
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
      }}
      window.addEventListener('resize', resize);
      resize();

      // Create stars
      for (var i = 0; i < 200; i++) {{
        stars.push({{
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 1.8 + 0.2,
          speed: Math.random() * 0.3 + 0.05,
          twinkle: Math.random() * Math.PI * 2,
          twinkleSpeed: 0.02 + Math.random() * 0.04,
          color: Math.random() > 0.3 ? '#00f5ff' : (Math.random() > 0.5 ? '#ffffff' : '#bf5fff'),
          alpha: 0.3 + Math.random() * 0.7,
        }});
      }}

      function spawnComet() {{
        comets.push({{
          x: Math.random() * W,
          y: -10,
          vx: 2 + Math.random() * 5,
          vy: 2 + Math.random() * 4,
          len: 80 + Math.random() * 120,
          alpha: 1,
          life: 1,
        }});
      }}

      // Spawn comets periodically
      setInterval(spawnComet, 3000 + Math.random() * 4000);
      setTimeout(spawnComet, 500);

      function draw() {{
        ctx.clearRect(0, 0, W, H);

        // Gradient background
        var bg = ctx.createRadialGradient(W*0.5, H*0.4, 0, W*0.5, H*0.4, Math.max(W, H)*0.8);
        bg.addColorStop(0,   'rgba(8, 14, 28, 1)');
        bg.addColorStop(0.5, 'rgba(5, 8, 18, 1)');
        bg.addColorStop(1,   'rgba(3, 5, 12, 1)');
        ctx.fillStyle = bg;
        ctx.fillRect(0, 0, W, H);

        // Nebula blobs
        [[W*0.2, H*0.3, 180, 'rgba(0,100,180,0.04)'],
         [W*0.8, H*0.6, 220, 'rgba(80,0,160,0.04)'],
         [W*0.5, H*0.8, 160, 'rgba(0,180,120,0.03)']
        ].forEach(function(n) {{
          var gr = ctx.createRadialGradient(n[0], n[1], 0, n[0], n[1], n[2]);
          gr.addColorStop(0, n[3]);
          gr.addColorStop(1, 'transparent');
          ctx.fillStyle = gr;
          ctx.beginPath();
          ctx.arc(n[0], n[1], n[2], 0, Math.PI*2);
          ctx.fill();
        }});

        // Stars
        var now = Date.now() * 0.001;
        stars.forEach(function(s) {{
          s.twinkle += s.twinkleSpeed;
          var a = s.alpha * (0.5 + 0.5 * Math.sin(s.twinkle));
          ctx.save();
          ctx.globalAlpha = a;
          var grad = ctx.createRadialGradient(s.x, s.y, 0, s.x, s.y, s.r * 2.5);
          grad.addColorStop(0, s.color);
          grad.addColorStop(1, 'transparent');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r * 2.5, 0, Math.PI*2);
          ctx.fill();
          // Star core
          ctx.globalAlpha = a * 0.9;
          ctx.fillStyle = '#ffffff';
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r * 0.5, 0, Math.PI*2);
          ctx.fill();
          ctx.restore();

          // Slow drift
          s.y += s.speed * 0.1;
          if (s.y > H) s.y = 0;
        }});

        // Comets
        comets = comets.filter(function(c) {{
          c.x += c.vx;
          c.y += c.vy;
          c.life -= 0.008;
          if (c.life <= 0 || c.x > W + 50 || c.y > H + 50) return false;
          ctx.save();
          ctx.globalAlpha = c.life;
          var tail = ctx.createLinearGradient(c.x, c.y, c.x - c.vx * (c.len/5), c.y - c.vy * (c.len/5));
          tail.addColorStop(0, 'rgba(200,240,255,0.9)');
          tail.addColorStop(0.3, 'rgba(0,200,255,0.5)');
          tail.addColorStop(1, 'transparent');
          ctx.strokeStyle = tail;
          ctx.lineWidth = 2;
          ctx.lineCap = 'round';
          ctx.beginPath();
          ctx.moveTo(c.x, c.y);
          ctx.lineTo(c.x - c.vx * (c.len/5), c.y - c.vy * (c.len/5));
          ctx.stroke();
          // Bright head
          ctx.globalAlpha = c.life;
          var hg = ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, 4);
          hg.addColorStop(0, 'rgba(255,255,255,1)');
          hg.addColorStop(1, 'transparent');
          ctx.fillStyle = hg;
          ctx.beginPath();
          ctx.arc(c.x, c.y, 4, 0, Math.PI*2);
          ctx.fill();
          ctx.restore();
          return true;
        }});

        requestAnimationFrame(draw);
      }}
      draw();
    }})();

    /* ── INIT (called AFTER all JS is defined) ── */
    renderHUD();
    initTypewriters();
  </script>
</body>
</html>"""
