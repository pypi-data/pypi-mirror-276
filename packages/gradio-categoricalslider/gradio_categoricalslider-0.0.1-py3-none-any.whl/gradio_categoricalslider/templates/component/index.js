const {
  SvelteComponent: xt,
  assign: $t,
  create_slot: el,
  detach: tl,
  element: ll,
  get_all_dirty_from_scope: nl,
  get_slot_changes: il,
  get_spread_update: fl,
  init: sl,
  insert: ol,
  safe_not_equal: al,
  set_dynamic_element_data: Je,
  set_style: j,
  toggle_class: O,
  transition_in: St,
  transition_out: Lt,
  update_slot_base: rl
} = window.__gradio__svelte__internal;
function _l(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), f = el(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let s = 0; s < o.length; s += 1)
    r = $t(r, o[s]);
  return {
    c() {
      e = ll(
        /*tag*/
        l[14]
      ), f && f.c(), Je(
        /*tag*/
        l[14]
      )(e, r), O(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        l[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), O(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), O(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), j(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), j(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), j(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), j(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), j(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), j(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), j(e, "border-width", "var(--block-border-width)");
    },
    m(s, a) {
      ol(s, e, a), f && f.m(e, null), n = !0;
    },
    p(s, a) {
      f && f.p && (!n || a & /*$$scope*/
      131072) && rl(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? il(
          i,
          /*$$scope*/
          s[17],
          a,
          null
        ) : nl(
          /*$$scope*/
          s[17]
        ),
        null
      ), Je(
        /*tag*/
        s[14]
      )(e, r = fl(o, [
        (!n || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), O(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        s[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), O(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), O(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), a & /*height*/
      1 && j(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), a & /*width*/
      2 && j(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), a & /*variant*/
      16 && j(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), a & /*allow_overflow*/
      2048 && j(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && j(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), a & /*min_width*/
      8192 && j(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (St(f, s), n = !0);
    },
    o(s) {
      Lt(f, s), n = !1;
    },
    d(s) {
      s && tl(e), f && f.d(s);
    }
  };
}
function ul(l) {
  let e, t = (
    /*tag*/
    l[14] && _l(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (St(t, n), e = !0);
    },
    o(n) {
      Lt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function cl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: o = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: p = "normal" } = e, { test_id: b = void 0 } = e, { explicit_call: k = !1 } = e, { container: M = !0 } = e, { visible: C = !0 } = e, { allow_overflow: S = !0 } = e, { scale: d = null } = e, { min_width: c = 0 } = e, h = p === "fieldset" ? "fieldset" : "div";
  const g = (m) => {
    if (m !== void 0) {
      if (typeof m == "number")
        return m + "px";
      if (typeof m == "string")
        return m;
    }
  };
  return l.$$set = (m) => {
    "height" in m && t(0, f = m.height), "width" in m && t(1, o = m.width), "elem_id" in m && t(2, r = m.elem_id), "elem_classes" in m && t(3, s = m.elem_classes), "variant" in m && t(4, a = m.variant), "border_mode" in m && t(5, _ = m.border_mode), "padding" in m && t(6, u = m.padding), "type" in m && t(16, p = m.type), "test_id" in m && t(7, b = m.test_id), "explicit_call" in m && t(8, k = m.explicit_call), "container" in m && t(9, M = m.container), "visible" in m && t(10, C = m.visible), "allow_overflow" in m && t(11, S = m.allow_overflow), "scale" in m && t(12, d = m.scale), "min_width" in m && t(13, c = m.min_width), "$$scope" in m && t(17, i = m.$$scope);
  }, [
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    b,
    k,
    M,
    C,
    S,
    d,
    c,
    h,
    g,
    p,
    i,
    n
  ];
}
class dl extends xt {
  constructor(e) {
    super(), sl(this, e, cl, ul, al, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: ml,
  attr: bl,
  create_slot: gl,
  detach: hl,
  element: wl,
  get_all_dirty_from_scope: pl,
  get_slot_changes: kl,
  init: vl,
  insert: yl,
  safe_not_equal: ql,
  transition_in: Cl,
  transition_out: Fl,
  update_slot_base: Ml
} = window.__gradio__svelte__internal;
function Sl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = gl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = wl("div"), i && i.c(), bl(e, "class", "svelte-1hnfib2");
    },
    m(f, o) {
      yl(f, e, o), i && i.m(e, null), t = !0;
    },
    p(f, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && Ml(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        t ? kl(
          n,
          /*$$scope*/
          f[0],
          o,
          null
        ) : pl(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (Cl(i, f), t = !0);
    },
    o(f) {
      Fl(i, f), t = !1;
    },
    d(f) {
      f && hl(e), i && i.d(f);
    }
  };
}
function Ll(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, n];
}
class zl extends ml {
  constructor(e) {
    super(), vl(this, e, Ll, Sl, ql, {});
  }
}
const {
  SvelteComponent: Vl,
  attr: Ke,
  check_outros: Nl,
  create_component: Il,
  create_slot: Zl,
  destroy_component: jl,
  detach: ve,
  element: Pl,
  empty: Bl,
  get_all_dirty_from_scope: Al,
  get_slot_changes: Dl,
  group_outros: El,
  init: Tl,
  insert: ye,
  mount_component: Rl,
  safe_not_equal: Xl,
  set_data: Yl,
  space: Gl,
  text: Ol,
  toggle_class: ie,
  transition_in: ce,
  transition_out: qe,
  update_slot_base: Ul
} = window.__gradio__svelte__internal;
function Qe(l) {
  let e, t;
  return e = new zl({
    props: {
      $$slots: { default: [Hl] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Il(e.$$.fragment);
    },
    m(n, i) {
      Rl(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (ce(e.$$.fragment, n), t = !0);
    },
    o(n) {
      qe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      jl(e, n);
    }
  };
}
function Hl(l) {
  let e;
  return {
    c() {
      e = Ol(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      ye(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Yl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && ve(e);
    }
  };
}
function Jl(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[2].default
  ), o = Zl(
    f,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let r = (
    /*info*/
    l[1] && Qe(l)
  );
  return {
    c() {
      e = Pl("span"), o && o.c(), t = Gl(), r && r.c(), n = Bl(), Ke(e, "data-testid", "block-info"), Ke(e, "class", "svelte-22c38v"), ie(e, "sr-only", !/*show_label*/
      l[0]), ie(e, "hide", !/*show_label*/
      l[0]), ie(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(s, a) {
      ye(s, e, a), o && o.m(e, null), ye(s, t, a), r && r.m(s, a), ye(s, n, a), i = !0;
    },
    p(s, [a]) {
      o && o.p && (!i || a & /*$$scope*/
      8) && Ul(
        o,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? Dl(
          f,
          /*$$scope*/
          s[3],
          a,
          null
        ) : Al(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && ie(e, "sr-only", !/*show_label*/
      s[0]), (!i || a & /*show_label*/
      1) && ie(e, "hide", !/*show_label*/
      s[0]), (!i || a & /*info*/
      2) && ie(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, a), a & /*info*/
      2 && ce(r, 1)) : (r = Qe(s), r.c(), ce(r, 1), r.m(n.parentNode, n)) : r && (El(), qe(r, 1, 1, () => {
        r = null;
      }), Nl());
    },
    i(s) {
      i || (ce(o, s), ce(r), i = !0);
    },
    o(s) {
      qe(o, s), qe(r), i = !1;
    },
    d(s) {
      s && (ve(e), ve(t), ve(n)), o && o.d(s), r && r.d(s);
    }
  };
}
function Kl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: o = void 0 } = e;
  return l.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, o = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, o, n, i];
}
class Ql extends Vl {
  constructor(e) {
    super(), Tl(this, e, Kl, Jl, Xl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Wl,
  append: Pe,
  attr: Q,
  bubble: xl,
  create_component: $l,
  destroy_component: en,
  detach: zt,
  element: Be,
  init: tn,
  insert: Vt,
  listen: ln,
  mount_component: nn,
  safe_not_equal: fn,
  set_data: sn,
  set_style: fe,
  space: on,
  text: an,
  toggle_class: Z,
  transition_in: rn,
  transition_out: _n
} = window.__gradio__svelte__internal;
function We(l) {
  let e, t;
  return {
    c() {
      e = Be("span"), t = an(
        /*label*/
        l[1]
      ), Q(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Vt(n, e, i), Pe(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && sn(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && zt(e);
    }
  };
}
function un(l) {
  let e, t, n, i, f, o, r, s = (
    /*show_label*/
    l[2] && We(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = Be("button"), s && s.c(), t = on(), n = Be("div"), $l(i.$$.fragment), Q(n, "class", "svelte-1lrphxw"), Z(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), Z(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), Z(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Q(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Q(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Q(
        e,
        "title",
        /*label*/
        l[1]
      ), Q(e, "class", "svelte-1lrphxw"), Z(
        e,
        "pending",
        /*pending*/
        l[3]
      ), Z(
        e,
        "padded",
        /*padded*/
        l[5]
      ), Z(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), Z(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), fe(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), fe(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), fe(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(a, _) {
      Vt(a, e, _), s && s.m(e, null), Pe(e, t), Pe(e, n), nn(i, n, null), f = !0, o || (r = ln(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), o = !0);
    },
    p(a, [_]) {
      /*show_label*/
      a[2] ? s ? s.p(a, _) : (s = We(a), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!f || _ & /*size*/
      16) && Z(
        n,
        "small",
        /*size*/
        a[4] === "small"
      ), (!f || _ & /*size*/
      16) && Z(
        n,
        "large",
        /*size*/
        a[4] === "large"
      ), (!f || _ & /*size*/
      16) && Z(
        n,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!f || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!f || _ & /*label*/
      2) && Q(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || _ & /*hasPopup*/
      256) && Q(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || _ & /*label*/
      2) && Q(
        e,
        "title",
        /*label*/
        a[1]
      ), (!f || _ & /*pending*/
      8) && Z(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!f || _ & /*padded*/
      32) && Z(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!f || _ & /*highlight*/
      64) && Z(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!f || _ & /*transparent*/
      512) && Z(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), _ & /*disabled, _color*/
      4224 && fe(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && fe(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), _ & /*offset*/
      2048 && fe(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (rn(i.$$.fragment, a), f = !0);
    },
    o(a) {
      _n(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && zt(e), s && s.d(), en(i), o = !1, r();
    }
  };
}
function cn(l, e, t) {
  let n, { Icon: i } = e, { label: f = "" } = e, { show_label: o = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: a = !0 } = e, { highlight: _ = !1 } = e, { disabled: u = !1 } = e, { hasPopup: p = !1 } = e, { color: b = "var(--block-label-text-color)" } = e, { transparent: k = !1 } = e, { background: M = "var(--background-fill-primary)" } = e, { offset: C = 0 } = e;
  function S(d) {
    xl.call(this, l, d);
  }
  return l.$$set = (d) => {
    "Icon" in d && t(0, i = d.Icon), "label" in d && t(1, f = d.label), "show_label" in d && t(2, o = d.show_label), "pending" in d && t(3, r = d.pending), "size" in d && t(4, s = d.size), "padded" in d && t(5, a = d.padded), "highlight" in d && t(6, _ = d.highlight), "disabled" in d && t(7, u = d.disabled), "hasPopup" in d && t(8, p = d.hasPopup), "color" in d && t(13, b = d.color), "transparent" in d && t(9, k = d.transparent), "background" in d && t(10, M = d.background), "offset" in d && t(11, C = d.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = _ ? "var(--color-accent)" : b);
  }, [
    i,
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    p,
    k,
    M,
    C,
    n,
    b,
    S
  ];
}
class dn extends Wl {
  constructor(e) {
    super(), tn(this, e, cn, un, fn, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: mn,
  append: Ve,
  attr: E,
  detach: bn,
  init: gn,
  insert: hn,
  noop: Ne,
  safe_not_equal: wn,
  set_style: U,
  svg_element: we
} = window.__gradio__svelte__internal;
function pn(l) {
  let e, t, n, i;
  return {
    c() {
      e = we("svg"), t = we("g"), n = we("path"), i = we("path"), E(n, "d", "M18,6L6.087,17.913"), U(n, "fill", "none"), U(n, "fill-rule", "nonzero"), U(n, "stroke-width", "2px"), E(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), E(i, "d", "M4.364,4.364L19.636,19.636"), U(i, "fill", "none"), U(i, "fill-rule", "nonzero"), U(i, "stroke-width", "2px"), E(e, "width", "100%"), E(e, "height", "100%"), E(e, "viewBox", "0 0 24 24"), E(e, "version", "1.1"), E(e, "xmlns", "http://www.w3.org/2000/svg"), E(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), E(e, "xml:space", "preserve"), E(e, "stroke", "currentColor"), U(e, "fill-rule", "evenodd"), U(e, "clip-rule", "evenodd"), U(e, "stroke-linecap", "round"), U(e, "stroke-linejoin", "round");
    },
    m(f, o) {
      hn(f, e, o), Ve(e, t), Ve(t, n), Ve(e, i);
    },
    p: Ne,
    i: Ne,
    o: Ne,
    d(f) {
      f && bn(e);
    }
  };
}
class kn extends mn {
  constructor(e) {
    super(), gn(this, e, null, pn, wn, {});
  }
}
const vn = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], xe = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
vn.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: xe[e][t],
      secondary: xe[e][n]
    }
  }),
  {}
);
function ae(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ce() {
}
function yn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Nt = typeof window < "u";
let $e = Nt ? () => window.performance.now() : () => Date.now(), It = Nt ? (l) => requestAnimationFrame(l) : Ce;
const re = /* @__PURE__ */ new Set();
function Zt(l) {
  re.forEach((e) => {
    e.c(l) || (re.delete(e), e.f());
  }), re.size !== 0 && It(Zt);
}
function qn(l) {
  let e;
  return re.size === 0 && It(Zt), {
    promise: new Promise((t) => {
      re.add(e = { c: l, f: t });
    }),
    abort() {
      re.delete(e);
    }
  };
}
const se = [];
function Cn(l, e = Ce) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (yn(l, r) && (l = r, t)) {
      const s = !se.length;
      for (const a of n)
        a[1](), se.push(a, l);
      if (s) {
        for (let a = 0; a < se.length; a += 2)
          se[a][0](se[a + 1]);
        se.length = 0;
      }
    }
  }
  function f(r) {
    i(r(l));
  }
  function o(r, s = Ce) {
    const a = [r, s];
    return n.add(a), n.size === 1 && (t = e(i, f) || Ce), r(l), () => {
      n.delete(a), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: o };
}
function et(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ae(l, e, t, n) {
  if (typeof t == "number" || et(t)) {
    const i = n - t, f = (t - e) / (l.dt || 1 / 60), o = l.opts.stiffness * i, r = l.opts.damping * f, s = (o - r) * l.inv_mass, a = (f + s) * l.dt;
    return Math.abs(a) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, et(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Ae(l, e[f], t[f], n[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Ae(l, e[f], t[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function tt(l, e = {}) {
  const t = Cn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let o, r, s, a = l, _ = l, u = 1, p = 0, b = !1;
  function k(C, S = {}) {
    _ = C;
    const d = s = {};
    return l == null || S.hard || M.stiffness >= 1 && M.damping >= 1 ? (b = !0, o = $e(), a = C, t.set(l = _), Promise.resolve()) : (S.soft && (p = 1 / ((S.soft === !0 ? 0.5 : +S.soft) * 60), u = 0), r || (o = $e(), b = !1, r = qn((c) => {
      if (b)
        return b = !1, r = null, !1;
      u = Math.min(u + p, 1);
      const h = {
        inv_mass: u,
        opts: M,
        settled: !0,
        dt: (c - o) * 60 / 1e3
      }, g = Ae(h, a, l, _);
      return o = c, a = l, t.set(l = g), h.settled && (r = null), !h.settled;
    })), new Promise((c) => {
      r.promise.then(() => {
        d === s && c();
      });
    }));
  }
  const M = {
    set: k,
    update: (C, S) => k(C(_, l), S),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return M;
}
const {
  SvelteComponent: Fn,
  append: T,
  attr: F,
  component_subscribe: lt,
  detach: Mn,
  element: Sn,
  init: Ln,
  insert: zn,
  noop: nt,
  safe_not_equal: Vn,
  set_style: pe,
  svg_element: R,
  toggle_class: it
} = window.__gradio__svelte__internal, { onMount: Nn } = window.__gradio__svelte__internal;
function In(l) {
  let e, t, n, i, f, o, r, s, a, _, u, p;
  return {
    c() {
      e = Sn("div"), t = R("svg"), n = R("g"), i = R("path"), f = R("path"), o = R("path"), r = R("path"), s = R("g"), a = R("path"), _ = R("path"), u = R("path"), p = R("path"), F(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), F(i, "fill", "#FF7C00"), F(i, "fill-opacity", "0.4"), F(i, "class", "svelte-43sxxs"), F(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), F(f, "fill", "#FF7C00"), F(f, "class", "svelte-43sxxs"), F(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), F(o, "fill", "#FF7C00"), F(o, "fill-opacity", "0.4"), F(o, "class", "svelte-43sxxs"), F(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), F(r, "fill", "#FF7C00"), F(r, "class", "svelte-43sxxs"), pe(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), F(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), F(a, "fill", "#FF7C00"), F(a, "fill-opacity", "0.4"), F(a, "class", "svelte-43sxxs"), F(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), F(_, "fill", "#FF7C00"), F(_, "class", "svelte-43sxxs"), F(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), F(u, "fill", "#FF7C00"), F(u, "fill-opacity", "0.4"), F(u, "class", "svelte-43sxxs"), F(p, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), F(p, "fill", "#FF7C00"), F(p, "class", "svelte-43sxxs"), pe(s, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), F(t, "viewBox", "-1200 -1200 3000 3000"), F(t, "fill", "none"), F(t, "xmlns", "http://www.w3.org/2000/svg"), F(t, "class", "svelte-43sxxs"), F(e, "class", "svelte-43sxxs"), it(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(b, k) {
      zn(b, e, k), T(e, t), T(t, n), T(n, i), T(n, f), T(n, o), T(n, r), T(t, s), T(s, a), T(s, _), T(s, u), T(s, p);
    },
    p(b, [k]) {
      k & /*$top*/
      2 && pe(n, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), k & /*$bottom*/
      4 && pe(s, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), k & /*margin*/
      1 && it(
        e,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: nt,
    o: nt,
    d(b) {
      b && Mn(e);
    }
  };
}
function Zn(l, e, t) {
  let n, i;
  var f = this && this.__awaiter || function(b, k, M, C) {
    function S(d) {
      return d instanceof M ? d : new M(function(c) {
        c(d);
      });
    }
    return new (M || (M = Promise))(function(d, c) {
      function h(z) {
        try {
          m(C.next(z));
        } catch (N) {
          c(N);
        }
      }
      function g(z) {
        try {
          m(C.throw(z));
        } catch (N) {
          c(N);
        }
      }
      function m(z) {
        z.done ? d(z.value) : S(z.value).then(h, g);
      }
      m((C = C.apply(b, k || [])).next());
    });
  };
  let { margin: o = !0 } = e;
  const r = tt([0, 0]);
  lt(l, r, (b) => t(1, n = b));
  const s = tt([0, 0]);
  lt(l, s, (b) => t(2, i = b));
  let a;
  function _() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function u() {
    return f(this, void 0, void 0, function* () {
      yield _(), a || u();
    });
  }
  function p() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), u();
    });
  }
  return Nn(() => (p(), () => a = !0)), l.$$set = (b) => {
    "margin" in b && t(0, o = b.margin);
  }, [o, n, i, r, s];
}
class jn extends Fn {
  constructor(e) {
    super(), Ln(this, e, Zn, In, Vn, { margin: 0 });
  }
}
const {
  SvelteComponent: Pn,
  append: le,
  attr: Y,
  binding_callbacks: ft,
  check_outros: De,
  create_component: jt,
  create_slot: Pt,
  destroy_component: Bt,
  destroy_each: At,
  detach: y,
  element: H,
  empty: _e,
  ensure_array_like: Fe,
  get_all_dirty_from_scope: Dt,
  get_slot_changes: Et,
  group_outros: Ee,
  init: Bn,
  insert: q,
  mount_component: Tt,
  noop: Te,
  safe_not_equal: An,
  set_data: D,
  set_style: $,
  space: A,
  text: L,
  toggle_class: B,
  transition_in: X,
  transition_out: J,
  update_slot_base: Rt
} = window.__gradio__svelte__internal, { tick: Dn } = window.__gradio__svelte__internal, { onDestroy: En } = window.__gradio__svelte__internal, { createEventDispatcher: Tn } = window.__gradio__svelte__internal, Rn = (l) => ({}), st = (l) => ({}), Xn = (l) => ({}), ot = (l) => ({});
function at(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function rt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Yn(l) {
  let e, t, n, i, f = (
    /*i18n*/
    l[1]("common.error") + ""
  ), o, r, s;
  t = new dn({
    props: {
      Icon: kn,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const a = (
    /*#slots*/
    l[30].error
  ), _ = Pt(
    a,
    l,
    /*$$scope*/
    l[29],
    st
  );
  return {
    c() {
      e = H("div"), jt(t.$$.fragment), n = A(), i = H("span"), o = L(f), r = A(), _ && _.c(), Y(e, "class", "clear-status svelte-vopvsi"), Y(i, "class", "error svelte-vopvsi");
    },
    m(u, p) {
      q(u, e, p), Tt(t, e, null), q(u, n, p), q(u, i, p), le(i, o), q(u, r, p), _ && _.m(u, p), s = !0;
    },
    p(u, p) {
      const b = {};
      p[0] & /*i18n*/
      2 && (b.label = /*i18n*/
      u[1]("common.clear")), t.$set(b), (!s || p[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      u[1]("common.error") + "") && D(o, f), _ && _.p && (!s || p[0] & /*$$scope*/
      536870912) && Rt(
        _,
        a,
        u,
        /*$$scope*/
        u[29],
        s ? Et(
          a,
          /*$$scope*/
          u[29],
          p,
          Rn
        ) : Dt(
          /*$$scope*/
          u[29]
        ),
        st
      );
    },
    i(u) {
      s || (X(t.$$.fragment, u), X(_, u), s = !0);
    },
    o(u) {
      J(t.$$.fragment, u), J(_, u), s = !1;
    },
    d(u) {
      u && (y(e), y(n), y(i), y(r)), Bt(t), _ && _.d(u);
    }
  };
}
function Gn(l) {
  let e, t, n, i, f, o, r, s, a, _ = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && _t(l)
  );
  function u(c, h) {
    if (
      /*progress*/
      c[7]
    )
      return Hn;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    )
      return Un;
    if (
      /*queue_position*/
      c[2] === 0
    )
      return On;
  }
  let p = u(l), b = p && p(l), k = (
    /*timer*/
    l[5] && dt(l)
  );
  const M = [Wn, Qn], C = [];
  function S(c, h) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = S(l)) && (o = C[f] = M[f](l));
  let d = !/*timer*/
  l[5] && kt(l);
  return {
    c() {
      _ && _.c(), e = A(), t = H("div"), b && b.c(), n = A(), k && k.c(), i = A(), o && o.c(), r = A(), d && d.c(), s = _e(), Y(t, "class", "progress-text svelte-vopvsi"), B(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), B(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(c, h) {
      _ && _.m(c, h), q(c, e, h), q(c, t, h), b && b.m(t, null), le(t, n), k && k.m(t, null), q(c, i, h), ~f && C[f].m(c, h), q(c, r, h), d && d.m(c, h), q(c, s, h), a = !0;
    },
    p(c, h) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? _ ? _.p(c, h) : (_ = _t(c), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), p === (p = u(c)) && b ? b.p(c, h) : (b && b.d(1), b = p && p(c), b && (b.c(), b.m(t, n))), /*timer*/
      c[5] ? k ? k.p(c, h) : (k = dt(c), k.c(), k.m(t, null)) : k && (k.d(1), k = null), (!a || h[0] & /*variant*/
      256) && B(
        t,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!a || h[0] & /*variant*/
      256) && B(
        t,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let g = f;
      f = S(c), f === g ? ~f && C[f].p(c, h) : (o && (Ee(), J(C[g], 1, 1, () => {
        C[g] = null;
      }), De()), ~f ? (o = C[f], o ? o.p(c, h) : (o = C[f] = M[f](c), o.c()), X(o, 1), o.m(r.parentNode, r)) : o = null), /*timer*/
      c[5] ? d && (Ee(), J(d, 1, 1, () => {
        d = null;
      }), De()) : d ? (d.p(c, h), h[0] & /*timer*/
      32 && X(d, 1)) : (d = kt(c), d.c(), X(d, 1), d.m(s.parentNode, s));
    },
    i(c) {
      a || (X(o), X(d), a = !0);
    },
    o(c) {
      J(o), J(d), a = !1;
    },
    d(c) {
      c && (y(e), y(t), y(i), y(r), y(s)), _ && _.d(c), b && b.d(), k && k.d(), ~f && C[f].d(c), d && d.d(c);
    }
  };
}
function _t(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = H("div"), Y(e, "class", "eta-bar svelte-vopvsi"), $(e, "transform", t);
    },
    m(n, i) {
      q(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && $(e, "transform", t);
    },
    d(n) {
      n && y(e);
    }
  };
}
function On(l) {
  let e;
  return {
    c() {
      e = L("processing |");
    },
    m(t, n) {
      q(t, e, n);
    },
    p: Te,
    d(t) {
      t && y(e);
    }
  };
}
function Un(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, f, o;
  return {
    c() {
      e = L("queue: "), n = L(t), i = L("/"), f = L(
        /*queue_size*/
        l[3]
      ), o = L(" |");
    },
    m(r, s) {
      q(r, e, s), q(r, n, s), q(r, i, s), q(r, f, s), q(r, o, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && D(n, t), s[0] & /*queue_size*/
      8 && D(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (y(e), y(n), y(i), y(f), y(o));
    }
  };
}
function Hn(l) {
  let e, t = Fe(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = ct(rt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = _e();
    },
    m(i, f) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, f);
      q(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Fe(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = rt(i, t, o);
          n[o] ? n[o].p(r, f) : (n[o] = ct(r), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && y(e), At(n, i);
    }
  };
}
function ut(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, f = " ", o;
  function r(_, u) {
    return (
      /*p*/
      _[41].length != null ? Kn : Jn
    );
  }
  let s = r(l), a = s(l);
  return {
    c() {
      a.c(), e = A(), n = L(t), i = L(" | "), o = L(f);
    },
    m(_, u) {
      a.m(_, u), q(_, e, u), q(_, n, u), q(_, i, u), q(_, o, u);
    },
    p(_, u) {
      s === (s = r(_)) && a ? a.p(_, u) : (a.d(1), a = s(_), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && D(n, t);
    },
    d(_) {
      _ && (y(e), y(n), y(i), y(o)), a.d(_);
    }
  };
}
function Jn(l) {
  let e = ae(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = L(e);
    },
    m(n, i) {
      q(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = ae(
        /*p*/
        n[41].index || 0
      ) + "") && D(t, e);
    },
    d(n) {
      n && y(t);
    }
  };
}
function Kn(l) {
  let e = ae(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = ae(
    /*p*/
    l[41].length
  ) + "", f;
  return {
    c() {
      t = L(e), n = L("/"), f = L(i);
    },
    m(o, r) {
      q(o, t, r), q(o, n, r), q(o, f, r);
    },
    p(o, r) {
      r[0] & /*progress*/
      128 && e !== (e = ae(
        /*p*/
        o[41].index || 0
      ) + "") && D(t, e), r[0] & /*progress*/
      128 && i !== (i = ae(
        /*p*/
        o[41].length
      ) + "") && D(f, i);
    },
    d(o) {
      o && (y(t), y(n), y(f));
    }
  };
}
function ct(l) {
  let e, t = (
    /*p*/
    l[41].index != null && ut(l)
  );
  return {
    c() {
      t && t.c(), e = _e();
    },
    m(n, i) {
      t && t.m(n, i), q(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = ut(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && y(e), t && t.d(n);
    }
  };
}
function dt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = L(
        /*formatted_timer*/
        l[20]
      ), n = L(t), i = L("s");
    },
    m(f, o) {
      q(f, e, o), q(f, n, o), q(f, i, o);
    },
    p(f, o) {
      o[0] & /*formatted_timer*/
      1048576 && D(
        e,
        /*formatted_timer*/
        f[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && D(n, t);
    },
    d(f) {
      f && (y(e), y(n), y(i));
    }
  };
}
function Qn(l) {
  let e, t;
  return e = new jn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      jt(e.$$.fragment);
    },
    m(n, i) {
      Tt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), e.$set(f);
    },
    i(n) {
      t || (X(e.$$.fragment, n), t = !0);
    },
    o(n) {
      J(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Bt(e, n);
    }
  };
}
function Wn(l) {
  let e, t, n, i, f, o = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && mt(l)
  );
  return {
    c() {
      e = H("div"), t = H("div"), r && r.c(), n = A(), i = H("div"), f = H("div"), Y(t, "class", "progress-level-inner svelte-vopvsi"), Y(f, "class", "progress-bar svelte-vopvsi"), $(f, "width", o), Y(i, "class", "progress-bar-wrap svelte-vopvsi"), Y(e, "class", "progress-level svelte-vopvsi");
    },
    m(s, a) {
      q(s, e, a), le(e, t), r && r.m(t, null), le(e, n), le(e, i), le(i, f), l[31](f);
    },
    p(s, a) {
      /*progress*/
      s[7] != null ? r ? r.p(s, a) : (r = mt(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      s[15] * 100}%`) && $(f, "width", o);
    },
    i: Te,
    o: Te,
    d(s) {
      s && y(e), r && r.d(), l[31](null);
    }
  };
}
function mt(l) {
  let e, t = Fe(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pt(at(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = _e();
    },
    m(i, f) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, f);
      q(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Fe(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = at(i, t, o);
          n[o] ? n[o].p(r, f) : (n[o] = pt(r), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && y(e), At(n, i);
    }
  };
}
function bt(l) {
  let e, t, n, i, f = (
    /*i*/
    l[43] !== 0 && xn()
  ), o = (
    /*p*/
    l[41].desc != null && gt(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && ht()
  ), s = (
    /*progress_level*/
    l[14] != null && wt(l)
  );
  return {
    c() {
      f && f.c(), e = A(), o && o.c(), t = A(), r && r.c(), n = A(), s && s.c(), i = _e();
    },
    m(a, _) {
      f && f.m(a, _), q(a, e, _), o && o.m(a, _), q(a, t, _), r && r.m(a, _), q(a, n, _), s && s.m(a, _), q(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[41].desc != null ? o ? o.p(a, _) : (o = gt(a), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = ht(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? s ? s.p(a, _) : (s = wt(a), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(a) {
      a && (y(e), y(t), y(n), y(i)), f && f.d(a), o && o.d(a), r && r.d(a), s && s.d(a);
    }
  };
}
function xn(l) {
  let e;
  return {
    c() {
      e = L(" /");
    },
    m(t, n) {
      q(t, e, n);
    },
    d(t) {
      t && y(e);
    }
  };
}
function gt(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = L(e);
    },
    m(n, i) {
      q(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && D(t, e);
    },
    d(n) {
      n && y(t);
    }
  };
}
function ht(l) {
  let e;
  return {
    c() {
      e = L("-");
    },
    m(t, n) {
      q(t, e, n);
    },
    d(t) {
      t && y(e);
    }
  };
}
function wt(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = L(e), n = L("%");
    },
    m(i, f) {
      q(i, t, f), q(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && D(t, e);
    },
    d(i) {
      i && (y(t), y(n));
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && bt(l)
  );
  return {
    c() {
      t && t.c(), e = _e();
    },
    m(n, i) {
      t && t.m(n, i), q(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = bt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && y(e), t && t.d(n);
    }
  };
}
function kt(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), o = Pt(
    f,
    l,
    /*$$scope*/
    l[29],
    ot
  );
  return {
    c() {
      e = H("p"), t = L(
        /*loading_text*/
        l[9]
      ), n = A(), o && o.c(), Y(e, "class", "loading svelte-vopvsi");
    },
    m(r, s) {
      q(r, e, s), le(e, t), q(r, n, s), o && o.m(r, s), i = !0;
    },
    p(r, s) {
      (!i || s[0] & /*loading_text*/
      512) && D(
        t,
        /*loading_text*/
        r[9]
      ), o && o.p && (!i || s[0] & /*$$scope*/
      536870912) && Rt(
        o,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Et(
          f,
          /*$$scope*/
          r[29],
          s,
          Xn
        ) : Dt(
          /*$$scope*/
          r[29]
        ),
        ot
      );
    },
    i(r) {
      i || (X(o, r), i = !0);
    },
    o(r) {
      J(o, r), i = !1;
    },
    d(r) {
      r && (y(e), y(n)), o && o.d(r);
    }
  };
}
function $n(l) {
  let e, t, n, i, f;
  const o = [Gn, Yn], r = [];
  function s(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(l)) && (n = r[t] = o[t](l)), {
    c() {
      e = H("div"), n && n.c(), Y(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-vopvsi"), B(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), B(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), B(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), B(
        e,
        "border",
        /*border*/
        l[12]
      ), $(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), $(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      q(a, e, _), ~t && r[t].m(e, null), l[33](e), f = !0;
    },
    p(a, _) {
      let u = t;
      t = s(a), t === u ? ~t && r[t].p(a, _) : (n && (Ee(), J(r[u], 1, 1, () => {
        r[u] = null;
      }), De()), ~t ? (n = r[t], n ? n.p(a, _) : (n = r[t] = o[t](a), n.c()), X(n, 1), n.m(e, null)) : n = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-vopvsi")) && Y(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && B(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && B(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && B(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && B(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && $(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && $(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (X(n), f = !0);
    },
    o(a) {
      J(n), f = !1;
    },
    d(a) {
      a && y(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var ei = function(l, e, t, n) {
  function i(f) {
    return f instanceof t ? f : new t(function(o) {
      o(f);
    });
  }
  return new (t || (t = Promise))(function(f, o) {
    function r(_) {
      try {
        a(n.next(_));
      } catch (u) {
        o(u);
      }
    }
    function s(_) {
      try {
        a(n.throw(_));
      } catch (u) {
        o(u);
      }
    }
    function a(_) {
      _.done ? f(_.value) : i(_.value).then(r, s);
    }
    a((n = n.apply(l, e || [])).next());
  });
};
let ke = [], Ie = !1;
function ti(l) {
  return ei(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (ke.push(e), !Ie)
        Ie = !0;
      else
        return;
      yield Dn(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < ke.length; i++) {
          const o = ke[i].getBoundingClientRect();
          (i === 0 || o.top + window.scrollY <= n[0]) && (n[0] = o.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Ie = !1, ke = [];
      });
    }
  });
}
function li(l, e, t) {
  let n, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const o = Tn();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: p = !1 } = e, { timer: b = !0 } = e, { show_progress: k = "full" } = e, { message: M = null } = e, { progress: C = null } = e, { variant: S = "default" } = e, { loading_text: d = "Loading..." } = e, { absolute: c = !0 } = e, { translucent: h = !1 } = e, { border: g = !1 } = e, { autoscroll: m } = e, z, N = !1, V = 0, P = 0, W = null, v = null, de = 0, K = null, x, G = null, ne = !0;
  const Gt = () => {
    t(0, s = t(27, W = t(19, me = null))), t(25, V = performance.now()), t(26, P = 0), N = !0, Ue();
  };
  function Ue() {
    requestAnimationFrame(() => {
      t(26, P = (performance.now() - V) / 1e3), N && Ue();
    });
  }
  function He() {
    t(26, P = 0), t(0, s = t(27, W = t(19, me = null))), N && (N = !1);
  }
  En(() => {
    N && He();
  });
  let me = null;
  function Ot(w) {
    ft[w ? "unshift" : "push"](() => {
      G = w, t(16, G), t(7, C), t(14, K), t(15, x);
    });
  }
  const Ut = () => {
    o("clear_status");
  };
  function Ht(w) {
    ft[w ? "unshift" : "push"](() => {
      z = w, t(13, z);
    });
  }
  return l.$$set = (w) => {
    "i18n" in w && t(1, r = w.i18n), "eta" in w && t(0, s = w.eta), "queue_position" in w && t(2, a = w.queue_position), "queue_size" in w && t(3, _ = w.queue_size), "status" in w && t(4, u = w.status), "scroll_to_output" in w && t(22, p = w.scroll_to_output), "timer" in w && t(5, b = w.timer), "show_progress" in w && t(6, k = w.show_progress), "message" in w && t(23, M = w.message), "progress" in w && t(7, C = w.progress), "variant" in w && t(8, S = w.variant), "loading_text" in w && t(9, d = w.loading_text), "absolute" in w && t(10, c = w.absolute), "translucent" in w && t(11, h = w.translucent), "border" in w && t(12, g = w.border), "autoscroll" in w && t(24, m = w.autoscroll), "$$scope" in w && t(29, f = w.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = W), s != null && W !== s && (t(28, v = (performance.now() - V) / 1e3 + s), t(19, me = v.toFixed(1)), t(27, W = s))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, de = v === null || v <= 0 || !P ? null : Math.min(P / v, 1)), l.$$.dirty[0] & /*progress*/
    128 && C != null && t(18, ne = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? t(14, K = C.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, K = null), K ? (t(15, x = K[K.length - 1]), G && (x === 0 ? t(16, G.style.transition = "0", G) : t(16, G.style.transition = "150ms", G))) : t(15, x = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? Gt() : He()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && z && p && (u === "pending" || u === "complete") && ti(z, m), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = P.toFixed(1));
  }, [
    s,
    r,
    a,
    _,
    u,
    b,
    k,
    C,
    S,
    d,
    c,
    h,
    g,
    z,
    K,
    x,
    G,
    de,
    ne,
    me,
    n,
    o,
    p,
    M,
    m,
    V,
    P,
    W,
    v,
    f,
    i,
    Ot,
    Ut,
    Ht
  ];
}
class ni extends Pn {
  constructor(e) {
    super(), Bn(
      this,
      e,
      li,
      $n,
      An,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: ii,
  append: te,
  assign: fi,
  attr: I,
  binding_callbacks: si,
  create_component: Re,
  destroy_component: Xe,
  destroy_each: oi,
  detach: Me,
  element: oe,
  ensure_array_like: vt,
  get_spread_object: ai,
  get_spread_update: ri,
  init: _i,
  insert: Se,
  listen: Ze,
  mount_component: Ye,
  run_all: ui,
  safe_not_equal: ci,
  set_data: Xt,
  set_input_value: yt,
  space: je,
  text: Yt,
  to_number: di,
  transition_in: Ge,
  transition_out: Oe
} = window.__gradio__svelte__internal, { afterUpdate: mi } = window.__gradio__svelte__internal;
function qt(l, e, t) {
  const n = l.slice();
  return n[12] = e[t][0], n[25] = e[t][1], n;
}
function bi(l) {
  let e;
  return {
    c() {
      e = Yt(
        /*label*/
        l[12]
      );
    },
    m(t, n) {
      Se(t, e, n);
    },
    p(t, n) {
      n & /*label*/
      4096 && Xt(
        e,
        /*label*/
        t[12]
      );
    },
    d(t) {
      t && Me(e);
    }
  };
}
function Ct(l) {
  let e, t = (
    /*label*/
    l[12] + ""
  ), n;
  return {
    c() {
      e = oe("span"), n = Yt(t);
    },
    m(i, f) {
      Se(i, e, f), te(e, n);
    },
    p(i, f) {
      f & /*categories*/
      2048 && t !== (t = /*label*/
      i[12] + "") && Xt(n, t);
    },
    d(i) {
      i && Me(e);
    }
  };
}
function gi(l) {
  let e, t, n, i, f, o, r, s, a, _, u, p, b, k, M, C;
  const S = [
    { autoscroll: (
      /*gradio*/
      l[1].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[1].i18n
    ) },
    /*loading_status*/
    l[10]
  ];
  let d = {};
  for (let g = 0; g < S.length; g += 1)
    d = fi(d, S[g]);
  e = new ni({ props: d }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[19]
  ), o = new Ql({
    props: {
      show_label: (
        /*show_label*/
        l[9]
      ),
      info: (
        /*info*/
        l[5]
      ),
      $$slots: { default: [bi] },
      $$scope: { ctx: l }
    }
  });
  let c = vt(
    /*categories*/
    l[11]
  ), h = [];
  for (let g = 0; g < c.length; g += 1)
    h[g] = Ct(qt(l, c, g));
  return {
    c() {
      Re(e.$$.fragment), t = je(), n = oe("div"), i = oe("div"), f = oe("label"), Re(o.$$.fragment), r = je(), s = oe("div");
      for (let g = 0; g < h.length; g += 1)
        h[g].c();
      a = je(), _ = oe("input"), I(
        f,
        "for",
        /*id*/
        l[15]
      ), I(i, "class", "head svelte-46715e"), I(s, "class", "labels svelte-46715e"), I(_, "type", "range"), I(
        _,
        "id",
        /*id*/
        l[15]
      ), I(_, "name", "cowbell"), I(_, "min", u = Math.min(.../*categories*/
      l[11].map(Ft))), I(_, "max", p = Math.max(.../*categories*/
      l[11].map(Mt))), I(_, "step", 1), _.disabled = /*disabled*/
      l[14], I(_, "aria-label", b = `range slider for ${/*label*/
      l[12]}`), I(_, "class", "slider svelte-46715e"), I(n, "class", "wrap svelte-46715e");
    },
    m(g, m) {
      Ye(e, g, m), Se(g, t, m), Se(g, n, m), te(n, i), te(i, f), Ye(o, f, null), te(n, r), te(n, s);
      for (let z = 0; z < h.length; z += 1)
        h[z] && h[z].m(s, null);
      te(n, a), te(n, _), yt(
        _,
        /*value*/
        l[0]
      ), l[21](_), k = !0, M || (C = [
        Ze(
          _,
          "change",
          /*input_change_input_handler*/
          l[20]
        ),
        Ze(
          _,
          "input",
          /*input_change_input_handler*/
          l[20]
        ),
        Ze(
          _,
          "pointerup",
          /*handle_release*/
          l[16]
        )
      ], M = !0);
    },
    p(g, m) {
      const z = m & /*gradio, loading_status*/
      1026 ? ri(S, [
        m & /*gradio*/
        2 && { autoscroll: (
          /*gradio*/
          g[1].autoscroll
        ) },
        m & /*gradio*/
        2 && { i18n: (
          /*gradio*/
          g[1].i18n
        ) },
        m & /*loading_status*/
        1024 && ai(
          /*loading_status*/
          g[10]
        )
      ]) : {};
      e.$set(z);
      const N = {};
      if (m & /*show_label*/
      512 && (N.show_label = /*show_label*/
      g[9]), m & /*info*/
      32 && (N.info = /*info*/
      g[5]), m & /*$$scope, label*/
      268439552 && (N.$$scope = { dirty: m, ctx: g }), o.$set(N), m & /*categories*/
      2048) {
        c = vt(
          /*categories*/
          g[11]
        );
        let V;
        for (V = 0; V < c.length; V += 1) {
          const P = qt(g, c, V);
          h[V] ? h[V].p(P, m) : (h[V] = Ct(P), h[V].c(), h[V].m(s, null));
        }
        for (; V < h.length; V += 1)
          h[V].d(1);
        h.length = c.length;
      }
      (!k || m & /*categories*/
      2048 && u !== (u = Math.min(.../*categories*/
      g[11].map(Ft)))) && I(_, "min", u), (!k || m & /*categories*/
      2048 && p !== (p = Math.max(.../*categories*/
      g[11].map(Mt)))) && I(_, "max", p), (!k || m & /*disabled*/
      16384) && (_.disabled = /*disabled*/
      g[14]), (!k || m & /*label*/
      4096 && b !== (b = `range slider for ${/*label*/
      g[12]}`)) && I(_, "aria-label", b), m & /*value*/
      1 && yt(
        _,
        /*value*/
        g[0]
      );
    },
    i(g) {
      k || (Ge(e.$$.fragment, g), Ge(o.$$.fragment, g), k = !0);
    },
    o(g) {
      Oe(e.$$.fragment, g), Oe(o.$$.fragment, g), k = !1;
    },
    d(g) {
      g && (Me(t), Me(n)), Xe(e, g), Xe(o), oi(h, g), l[21](null), M = !1, ui(C);
    }
  };
}
function hi(l) {
  let e, t;
  return e = new dl({
    props: {
      visible: (
        /*visible*/
        l[4]
      ),
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      container: (
        /*container*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[7]
      ),
      min_width: (
        /*min_width*/
        l[8]
      ),
      $$slots: { default: [gi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Re(e.$$.fragment);
    },
    m(n, i) {
      Ye(e, n, i), t = !0;
    },
    p(n, [i]) {
      const f = {};
      i & /*visible*/
      16 && (f.visible = /*visible*/
      n[4]), i & /*elem_id*/
      4 && (f.elem_id = /*elem_id*/
      n[2]), i & /*elem_classes*/
      8 && (f.elem_classes = /*elem_classes*/
      n[3]), i & /*container*/
      64 && (f.container = /*container*/
      n[6]), i & /*scale*/
      128 && (f.scale = /*scale*/
      n[7]), i & /*min_width*/
      256 && (f.min_width = /*min_width*/
      n[8]), i & /*$$scope, categories, disabled, label, value, rangeInput, show_label, info, gradio, loading_status*/
      268467747 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Oe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Xe(e, n);
    }
  };
}
let wi = 0;
const Ft = (l) => l[1], Mt = (l) => l[1];
function pi(l, e, t) {
  let n, { gradio: i } = e, { elem_id: f = "" } = e, { elem_classes: o = [] } = e, { visible: r = !0 } = e, { value: s = 0 } = e, { label: a = i.i18n("slider.slider") } = e, { info: _ = void 0 } = e, { container: u = !0 } = e, { scale: p = null } = e, { min_width: b = void 0 } = e, { show_label: k } = e, { interactive: M } = e, { loading_status: C } = e, { value_is_output: S = !1 } = e, { categories: d = [] } = e, c;
  const h = `range_id_${wi++}`;
  function g() {
    i.dispatch("change"), S || i.dispatch("input");
  }
  mi(() => {
    t(17, S = !1), z();
  });
  function m(v) {
    i.dispatch("release", s);
  }
  function z() {
    N(), c.addEventListener("input", N);
  }
  function N() {
    const v = Math.min(...d.map((ne) => ne[1])), de = Math.max(...d.map((ne) => ne[1])), K = Number(c.value) - v, x = de - v, G = x === 0 ? 0 : K / x;
    t(13, c.style.backgroundSize = G * 100 + "% 100%", c);
  }
  const V = () => i.dispatch("clear_status", C);
  function P() {
    s = di(this.value), t(0, s);
  }
  function W(v) {
    si[v ? "unshift" : "push"](() => {
      c = v, t(13, c);
    });
  }
  return l.$$set = (v) => {
    "gradio" in v && t(1, i = v.gradio), "elem_id" in v && t(2, f = v.elem_id), "elem_classes" in v && t(3, o = v.elem_classes), "visible" in v && t(4, r = v.visible), "value" in v && t(0, s = v.value), "label" in v && t(12, a = v.label), "info" in v && t(5, _ = v.info), "container" in v && t(6, u = v.container), "scale" in v && t(7, p = v.scale), "min_width" in v && t(8, b = v.min_width), "show_label" in v && t(9, k = v.show_label), "interactive" in v && t(18, M = v.interactive), "loading_status" in v && t(10, C = v.loading_status), "value_is_output" in v && t(17, S = v.value_is_output), "categories" in v && t(11, d = v.categories);
  }, l.$$.update = () => {
    l.$$.dirty & /*interactive*/
    262144 && t(14, n = !M), l.$$.dirty & /*value*/
    1 && g();
  }, [
    s,
    i,
    f,
    o,
    r,
    _,
    u,
    p,
    b,
    k,
    C,
    d,
    a,
    c,
    n,
    h,
    m,
    S,
    M,
    V,
    P,
    W
  ];
}
class ki extends ii {
  constructor(e) {
    super(), _i(this, e, pi, hi, ci, {
      gradio: 1,
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      value: 0,
      label: 12,
      info: 5,
      container: 6,
      scale: 7,
      min_width: 8,
      show_label: 9,
      interactive: 18,
      loading_status: 10,
      value_is_output: 17,
      categories: 11
    });
  }
}
export {
  ki as default
};
