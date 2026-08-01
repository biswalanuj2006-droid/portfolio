(() => {
  "use strict";

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  /* ---------- Preloader ---------- */
  const preloader = $("#preloader");
  const hidePreloader = () => preloader && preloader.classList.add("hidden");
  // Hide as soon as the DOM is ready (don't wait for slow CDN fonts/scripts).
  document.addEventListener("DOMContentLoaded", () => setTimeout(hidePreloader, 450));
  window.addEventListener("load", hidePreloader);
  setTimeout(hidePreloader, 2000); // safety net: never leave the spinner forever

  /* ---------- Navbar ---------- */
  const nav = $("#siteNav");
  const navLinks = $("#navLinks");
  const navToggler = $("#navToggler");
  if (navToggler && navLinks) {
    navToggler.addEventListener("click", () => {
      navLinks.classList.toggle("open");
      navToggler.classList.toggle("active");
    });
    navLinks.querySelectorAll("a").forEach((link) =>
      link.addEventListener("click", () => navLinks.classList.remove("open"))
    );
  }
  const onScroll = () => nav && nav.classList.toggle("scrolled", window.scrollY > 30);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Theme toggle ---------- */
  const themeToggle = $("#themeToggle");
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme") || "dark";
  root.setAttribute("data-theme", savedTheme);
  if (themeToggle) {
    const icons = { dark: "bi-moon-stars", light: "bi-sun" };
    const syncIcon = () => {
      const i = themeToggle.querySelector("i");
      if (i) i.className = "bi " + (root.getAttribute("data-theme") === "dark" ? icons.dark : icons.light);
    };
    syncIcon();
    themeToggle.addEventListener("click", () => {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);
      syncIcon();
    });
  }

  /* ---------- Hero typing animation ---------- */
  const typedEl = $("#typed");
  if (typedEl) {
    let roles = [];
    try {
      const data = document.getElementById("typingRoles");
      roles = data ? JSON.parse(data.textContent) : [];
    } catch (e) { roles = []; }
    const list = (Array.isArray(roles) && roles.length)
      ? roles
      : ["AI Engineer", "Full-Stack Developer", "ML Enthusiast"];
    let ri = 0, ci = 0, deleting = false;
    const type = () => {
      const word = list[ri];
      typedEl.textContent = word.slice(0, ci);
      if (!deleting) {
        if (ci < word.length) { ci++; setTimeout(type, 65); }
        else { deleting = true; setTimeout(type, 1700); }
      } else {
        if (ci > 0) { ci--; setTimeout(type, 32); }
        else { deleting = false; ri = (ri + 1) % list.length; setTimeout(type, 320); }
      }
    };
    type();
  }

  /* ---------- Mobile menu overlay close on outside click ---------- */
  document.addEventListener("click", (e) => {
    if (navLinks && navLinks.classList.contains("open") && !e.target.closest(".nav-inner")) {
      navLinks.classList.remove("open");
    }
  });


  /* ---------- Particles (hero canvas) ---------- */
  const canvas = $("#particles");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let particles = [], raf = null;
    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    const init = () => {
      resize();
      const count = Math.min(90, Math.floor(canvas.width / 16));
      particles = Array.from({ length: count }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2 + 0.6,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        c: Math.random() > 0.5 ? "108,92,231" : "0,212,255",
      }));
    };
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach((p, i) => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.c},0.8)`;
        ctx.fill();
        for (let j = i + 1; j < particles.length; j++) {
          const q = particles[j];
          const dx = p.x - q.x, dy = p.y - q.y;
          const dist = Math.hypot(dx, dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = `rgba(${p.c},${0.12 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      });
      raf = requestAnimationFrame(draw);
    };
    window.addEventListener("resize", () => { init(); }, { passive: true });
    init();
    raf = requestAnimationFrame(draw);
  }

  /* ---------- Reveal on scroll ---------- */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  $$(".reveal").forEach((el) => revealObserver.observe(el));

  /* ---------- Animated counters ---------- */
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.count || "0", 10);
      const duration = 1200;
      const start = performance.now();
      const step = (now) => {
        const p = Math.min((now - start) / duration, 1);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      countObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  $$(".stat-num[data-count]").forEach((el) => countObserver.observe(el));

  /* ---------- Skill bars / rings animate ---------- */
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const card = entry.target;
      const fill = card.querySelector(".skill-fill");
      if (fill) fill.classList.add("animated");
      skillObserver.unobserve(card);
    });
  }, { threshold: 0.35 });
  $$(".skill-bar-card, .skill-card").forEach((el) => skillObserver.observe(el));

  /* ---------- Back to top ---------- */
  const backToTop = $("#backToTop");
  if (backToTop) {
    backToTop.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" })
    );
  }

  /* ---------- Lightbox ---------- */
  const lightbox = $("#lightbox");
  const lightboxImg = $("#lightbox-img");
  const lightboxTitle = $("#lightbox-title");
  const openLightbox = (src, title) => {
    if (!lightbox || !src) return;
    lightboxImg.src = src;
    lightboxImg.alt = title || "Preview";
    if (lightboxTitle) lightboxTitle.textContent = title || "";
    lightbox.classList.add("open");
    document.body.style.overflow = "hidden";
  };
  document.addEventListener("click", (e) => {
    const trigger = e.target.closest("[data-lightbox]");
    if (trigger && trigger.dataset.lightbox) {
      e.preventDefault();
      openLightbox(trigger.dataset.lightbox, trigger.dataset.title);
    }
  });
  if (lightbox) {
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox || e.target.closest(".lightbox-close")) {
        lightbox.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && lightbox.classList.contains("open")) {
        lightbox.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  }

  /* ---------- AI Assistant (predefined FAQs only) ---------- */
  const fab = $("#aiFab");
  const panel = $("#aiPanel");
  const closeBtn = $("#aiClose");
  const messagesBox = $("#aiMessages");
  const chipsBox = $("#aiChips");
  const aiForm = $("#aiForm");
  const aiText = $("#aiText");
  let faqs = [];
  const FALLBACK =
    "I'm designed to answer only portfolio-related questions.";
  const GREETING =
    "Hi! I'm Anuj's portfolio assistant. Ask me about his skills, projects, certificates, education or how to contact him.";

  const addMsg = (text, who) => {
    const div = document.createElement("div");
    div.className = `ai-msg ${who}`;
    div.textContent = text;
    messagesBox.appendChild(div);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    return div;
  };

  const renderChips = () => {
    if (!chipsBox || !faqs.length) return;
    chipsBox.innerHTML = "";
    faqs.slice(0, 4).forEach((f) => {
      const chip = document.createElement("button");
      chip.className = "ai-chip";
      chip.type = "button";
      chip.textContent = f.question.length > 34 ? f.question.slice(0, 32) + "..." : f.question;
      chip.addEventListener("click", () => {
        addMsg(f.question, "user");
        setTimeout(() => addMsg(f.answer, "bot"), 350);
      });
      chipsBox.appendChild(chip);
    });
  };

  const bestMatch = (query) => {
    const qTokens = query.toLowerCase().replace(/[^a-z0-9 ]/g, "").split(/\s+/).filter(Boolean);
    let best = null, bestScore = 0;
    faqs.forEach((f) => {
      const haystack = `${f.question} ${f.keywords || ""}`.toLowerCase();
      const tokens = haystack.replace(/[^a-z0-9 ]/g, "").split(/\s+/).filter(Boolean);
      const hits = qTokens.filter((t) => tokens.includes(t)).length;
      const score = qTokens.length ? hits / qTokens.length : 0;
      if (score > bestScore) { bestScore = score; best = f; }
    });
    return bestScore >= 0.45 ? best : null;
  };

  const answer = (query) => {
    const match = bestMatch(query);
    if (match) return match.answer;
    return FALLBACK;
  };

  if (fab && panel) {
    const toggle = (open) => {
      panel.classList.toggle("open", open);
      panel.setAttribute("aria-hidden", String(!open));
      if (open && !messagesBox.children.length) {
        addMsg(GREETING, "bot");
        renderChips();
      }
    };
    fab.addEventListener("click", () => toggle(!panel.classList.contains("open")));
    if (closeBtn) closeBtn.addEventListener("click", () => toggle(false));
    if (aiForm) {
      aiForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const query = aiText.value.trim();
        if (!query) return;
        addMsg(query, "user");
        aiText.value = "";
        const typing = document.createElement("div");
        typing.className = "ai-msg bot ai-typing";
        typing.innerHTML = "<i>•</i> <i>•</i> <i>•</i>";
        messagesBox.appendChild(typing);
        messagesBox.scrollTop = messagesBox.scrollHeight;
        setTimeout(() => {
          typing.remove();
          addMsg(answer(query), "bot");
        }, 650);
      });
    }
  }

  /* ---------- Load FAQs ---------- */
  fetch("/api/faq/")
    .then((res) => res.json())
    .then((data) => { faqs = data.faqs || []; renderChips(); })
    .catch(() => { /* assistant works with empty state */ });
})();
