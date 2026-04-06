/* ============================================================
   TWILIGHT BIATHLON — Shared JS
   ============================================================ */

// Mobile menu toggle
function initMobileMenu() {
  var btn = document.getElementById('nav-hamburger');
  var menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', function() {
    var isOpen = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on link click
  menu.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });
}

// FAQ accordion
function initFaqAccordion() {
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var answer = this.nextElementSibling;
      var isOpen = answer.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-answer.open').forEach(function(a) { a.classList.remove('open'); });
      document.querySelectorAll('.faq-question[aria-expanded="true"]').forEach(function(b) {
        b.setAttribute('aria-expanded', 'false');
      });

      if (!isOpen) {
        answer.classList.add('open');
        this.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

// Mark active nav link
function initActiveNav() {
  var path = window.location.pathname;
  var filename = path.split('/').pop() || 'index.html';

  document.querySelectorAll('.nav__link, .mobile-menu__link').forEach(function(link) {
    var href = link.getAttribute('href');
    if (!href) return;
    var linkFile = href.split('/').pop() || 'index.html';

    if (linkFile === filename) {
      link.classList.add('nav__link--active');
      if (link.classList.contains('mobile-menu__link')) {
        link.classList.add('mobile-menu__link--active');
      }
    }
  });
}

// Scroll reveal animation
function initScrollReveal() {
  var els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  els.forEach(function(el) { observer.observe(el); });
}

// Hero laser animation (home page only)
function initHeroLasers() {
  var canvas = document.getElementById('hero-lasers');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var W, H;

  function resize() {
    var hero = canvas.parentElement;
    W = canvas.width = hero.offsetWidth;
    H = canvas.height = hero.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  var beams = [
    { ox: -0.03, oy: 0.18, tx: 1.05, ty: 0.52, w: 1.5, int: 0.32, drift: 0.002, phase: 0 },
    { ox: -0.02, oy: 0.42, tx: 1.08, ty: 0.68, w: 1.2, int: 0.25, drift: 0.003, phase: 1.4 },
    { ox: -0.03, oy: 0.58, tx: 1.04, ty: 0.38, w: 1.6, int: 0.35, drift: 0.0025, phase: 2.8 },
    { ox: -0.02, oy: 0.76, tx: 1.06, ty: 0.55, w: 1.0, int: 0.20, drift: 0.004, phase: 0.7 },
    { ox: -0.03, oy: 0.33, tx: 1.07, ty: 0.80, w: 1.3, int: 0.28, drift: 0.003, phase: 3.5 },
  ];

  var t = 0;
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  function drawBeam(b) {
    var ox = b.ox * W, oy = b.oy * H;
    var jx = Math.sin(t * b.drift * 900 + b.phase) * 25 + Math.sin(t * b.drift * 350 + b.phase * 2.3) * 15;
    var jy = Math.cos(t * b.drift * 750 + b.phase * 1.7) * 20 + Math.cos(t * b.drift * 450 + b.phase * 0.7) * 10;
    var tx = b.tx * W + jx, ty = b.ty * H + jy;
    var flicker = 0.85 + 0.15 * Math.sin(t * 8 + b.phase * 3);
    var a = b.int * flicker;

    var lc = window.__LASER_COLOR || '100,200,60';
    var lc2 = window.__LASER_COLOR2 || '80,170,40';
    var lc3 = window.__LASER_COLOR3 || '60,150,30';
    ctx.save();
    ctx.filter = 'blur(1.5px)';

    ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + lc + ',' + (a * 0.7) + ')'; ctx.lineWidth = b.w * 0.8; ctx.stroke();

    ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + lc + ',' + (a * 0.25) + ')'; ctx.lineWidth = b.w * 3; ctx.stroke();

    ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + lc2 + ',' + (a * 0.07) + ')'; ctx.lineWidth = b.w * 8; ctx.stroke();

    ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + lc3 + ',' + (a * 0.02) + ')'; ctx.lineWidth = b.w * 20; ctx.stroke();

    ctx.restore();
  }

  function render() {
    t += 0.024;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < beams.length; i++) drawBeam(beams[i]);
    requestAnimationFrame(render);
  }
  render();
}

// Init all
document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initFaqAccordion();
  initActiveNav();
  initScrollReveal();
  initHeroLasers();
});
