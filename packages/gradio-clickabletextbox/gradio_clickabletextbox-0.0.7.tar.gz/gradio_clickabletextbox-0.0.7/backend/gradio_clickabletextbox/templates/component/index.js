const {
  SvelteComponent: Zl,
  assign: Sl,
  create_slot: zl,
  detach: El,
  element: Tl,
  get_all_dirty_from_scope: Nl,
  get_slot_changes: Bl,
  get_spread_update: Al,
  init: Dl,
  insert: Il,
  safe_not_equal: jl,
  set_dynamic_element_data: Mt,
  set_style: U,
  toggle_class: fe,
  transition_in: _l,
  transition_out: cl,
  update_slot_base: Pl
} = window.__gradio__svelte__internal;
function Yl(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), s = zl(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let f = [
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
  ], a = {};
  for (let r = 0; r < f.length; r += 1)
    a = Sl(a, f[r]);
  return {
    c() {
      e = Tl(
        /*tag*/
        l[14]
      ), s && s.c(), Mt(
        /*tag*/
        l[14]
      )(e, a), fe(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), fe(
        e,
        "padded",
        /*padding*/
        l[6]
      ), fe(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), fe(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), fe(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), U(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), U(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), U(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), U(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), U(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), U(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), U(e, "border-width", "var(--block-border-width)");
    },
    m(r, o) {
      Il(r, e, o), s && s.m(e, null), n = !0;
    },
    p(r, o) {
      s && s.p && (!n || o & /*$$scope*/
      131072) && Pl(
        s,
        i,
        r,
        /*$$scope*/
        r[17],
        n ? Bl(
          i,
          /*$$scope*/
          r[17],
          o,
          null
        ) : Nl(
          /*$$scope*/
          r[17]
        ),
        null
      ), Mt(
        /*tag*/
        r[14]
      )(e, a = Al(f, [
        (!n || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!n || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!n || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), fe(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), fe(
        e,
        "padded",
        /*padding*/
        r[6]
      ), fe(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), fe(
        e,
        "border_contrast",
        /*border_mode*/
        r[5] === "contrast"
      ), fe(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), o & /*height*/
      1 && U(
        e,
        "height",
        /*get_dimension*/
        r[15](
          /*height*/
          r[0]
        )
      ), o & /*width*/
      2 && U(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : (
        /*get_dimension*/
        r[15](
          /*width*/
          r[1]
        )
      )), o & /*variant*/
      16 && U(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), o & /*allow_overflow*/
      2048 && U(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && U(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), o & /*min_width*/
      8192 && U(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      n || (_l(s, r), n = !0);
    },
    o(r) {
      cl(s, r), n = !1;
    },
    d(r) {
      r && El(e), s && s.d(r);
    }
  };
}
function Kl(l) {
  let e, t = (
    /*tag*/
    l[14] && Yl(l)
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
      e || (_l(t, n), e = !0);
    },
    o(n) {
      cl(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Ol(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: f = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: r = [] } = e, { variant: o = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: c = "normal" } = e, { test_id: m = void 0 } = e, { explicit_call: v = !1 } = e, { container: L = !0 } = e, { visible: w = !0 } = e, { allow_overflow: H = !0 } = e, { scale: b = null } = e, { min_width: h = 0 } = e, p = c === "fieldset" ? "fieldset" : "div";
  const T = (k) => {
    if (k !== void 0) {
      if (typeof k == "number")
        return k + "px";
      if (typeof k == "string")
        return k;
    }
  };
  return l.$$set = (k) => {
    "height" in k && t(0, s = k.height), "width" in k && t(1, f = k.width), "elem_id" in k && t(2, a = k.elem_id), "elem_classes" in k && t(3, r = k.elem_classes), "variant" in k && t(4, o = k.variant), "border_mode" in k && t(5, u = k.border_mode), "padding" in k && t(6, _ = k.padding), "type" in k && t(16, c = k.type), "test_id" in k && t(7, m = k.test_id), "explicit_call" in k && t(8, v = k.explicit_call), "container" in k && t(9, L = k.container), "visible" in k && t(10, w = k.visible), "allow_overflow" in k && t(11, H = k.allow_overflow), "scale" in k && t(12, b = k.scale), "min_width" in k && t(13, h = k.min_width), "$$scope" in k && t(17, i = k.$$scope);
  }, [
    s,
    f,
    a,
    r,
    o,
    u,
    _,
    m,
    v,
    L,
    w,
    H,
    b,
    h,
    p,
    T,
    c,
    i,
    n
  ];
}
class Ul extends Zl {
  constructor(e) {
    super(), Dl(this, e, Ol, Kl, jl, {
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
  SvelteComponent: Xl,
  attr: Gl,
  create_slot: Rl,
  detach: Wl,
  element: Jl,
  get_all_dirty_from_scope: Ql,
  get_slot_changes: xl,
  init: $l,
  insert: en,
  safe_not_equal: tn,
  transition_in: ln,
  transition_out: nn,
  update_slot_base: sn
} = window.__gradio__svelte__internal;
function fn(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = Rl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = Jl("div"), i && i.c(), Gl(e, "class", "svelte-1hnfib2");
    },
    m(s, f) {
      en(s, e, f), i && i.m(e, null), t = !0;
    },
    p(s, [f]) {
      i && i.p && (!t || f & /*$$scope*/
      1) && sn(
        i,
        n,
        s,
        /*$$scope*/
        s[0],
        t ? xl(
          n,
          /*$$scope*/
          s[0],
          f,
          null
        ) : Ql(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (ln(i, s), t = !0);
    },
    o(s) {
      nn(i, s), t = !1;
    },
    d(s) {
      s && Wl(e), i && i.d(s);
    }
  };
}
function on(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, n];
}
class an extends Xl {
  constructor(e) {
    super(), $l(this, e, on, fn, tn, {});
  }
}
const {
  SvelteComponent: rn,
  attr: Vt,
  check_outros: un,
  create_component: _n,
  create_slot: cn,
  destroy_component: dn,
  detach: Ue,
  element: mn,
  empty: hn,
  get_all_dirty_from_scope: bn,
  get_slot_changes: gn,
  group_outros: wn,
  init: vn,
  insert: Xe,
  mount_component: kn,
  safe_not_equal: pn,
  set_data: Cn,
  space: yn,
  text: Ln,
  toggle_class: Le,
  transition_in: De,
  transition_out: Ge,
  update_slot_base: Mn
} = window.__gradio__svelte__internal;
function Ht(l) {
  let e, t;
  return e = new an({
    props: {
      $$slots: { default: [Vn] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      _n(e.$$.fragment);
    },
    m(n, i) {
      kn(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (De(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ge(e.$$.fragment, n), t = !1;
    },
    d(n) {
      dn(e, n);
    }
  };
}
function Vn(l) {
  let e;
  return {
    c() {
      e = Ln(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Xe(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Cn(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Ue(e);
    }
  };
}
function Hn(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[2].default
  ), f = cn(
    s,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let a = (
    /*info*/
    l[1] && Ht(l)
  );
  return {
    c() {
      e = mn("span"), f && f.c(), t = yn(), a && a.c(), n = hn(), Vt(e, "data-testid", "block-info"), Vt(e, "class", "svelte-22c38v"), Le(e, "sr-only", !/*show_label*/
      l[0]), Le(e, "hide", !/*show_label*/
      l[0]), Le(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(r, o) {
      Xe(r, e, o), f && f.m(e, null), Xe(r, t, o), a && a.m(r, o), Xe(r, n, o), i = !0;
    },
    p(r, [o]) {
      f && f.p && (!i || o & /*$$scope*/
      8) && Mn(
        f,
        s,
        r,
        /*$$scope*/
        r[3],
        i ? gn(
          s,
          /*$$scope*/
          r[3],
          o,
          null
        ) : bn(
          /*$$scope*/
          r[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && Le(e, "sr-only", !/*show_label*/
      r[0]), (!i || o & /*show_label*/
      1) && Le(e, "hide", !/*show_label*/
      r[0]), (!i || o & /*info*/
      2) && Le(
        e,
        "has-info",
        /*info*/
        r[1] != null
      ), /*info*/
      r[1] ? a ? (a.p(r, o), o & /*info*/
      2 && De(a, 1)) : (a = Ht(r), a.c(), De(a, 1), a.m(n.parentNode, n)) : a && (wn(), Ge(a, 1, 1, () => {
        a = null;
      }), un());
    },
    i(r) {
      i || (De(f, r), De(a), i = !0);
    },
    o(r) {
      Ge(f, r), Ge(a), i = !1;
    },
    d(r) {
      r && (Ue(e), Ue(t), Ue(n)), f && f.d(r), a && a.d(r);
    }
  };
}
function qn(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: f = void 0 } = e;
  return l.$$set = (a) => {
    "show_label" in a && t(0, s = a.show_label), "info" in a && t(1, f = a.info), "$$scope" in a && t(3, i = a.$$scope);
  }, [s, f, n, i];
}
class Fn extends rn {
  constructor(e) {
    super(), vn(this, e, qn, Hn, pn, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Zn,
  append: _t,
  attr: _e,
  bubble: Sn,
  create_component: zn,
  destroy_component: En,
  detach: dl,
  element: ct,
  init: Tn,
  insert: ml,
  listen: Nn,
  mount_component: Bn,
  safe_not_equal: An,
  set_data: Dn,
  set_style: Me,
  space: In,
  text: jn,
  toggle_class: j,
  transition_in: Pn,
  transition_out: Yn
} = window.__gradio__svelte__internal;
function qt(l) {
  let e, t;
  return {
    c() {
      e = ct("span"), t = jn(
        /*label*/
        l[1]
      ), _e(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      ml(n, e, i), _t(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Dn(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && dl(e);
    }
  };
}
function Kn(l) {
  let e, t, n, i, s, f, a, r = (
    /*show_label*/
    l[2] && qt(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = ct("button"), r && r.c(), t = In(), n = ct("div"), zn(i.$$.fragment), _e(n, "class", "svelte-1lrphxw"), j(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), j(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), j(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], _e(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), _e(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), _e(
        e,
        "title",
        /*label*/
        l[1]
      ), _e(e, "class", "svelte-1lrphxw"), j(
        e,
        "pending",
        /*pending*/
        l[3]
      ), j(
        e,
        "padded",
        /*padded*/
        l[5]
      ), j(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), j(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), Me(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), Me(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), Me(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(o, u) {
      ml(o, e, u), r && r.m(e, null), _t(e, t), _t(e, n), Bn(i, n, null), s = !0, f || (a = Nn(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), f = !0);
    },
    p(o, [u]) {
      /*show_label*/
      o[2] ? r ? r.p(o, u) : (r = qt(o), r.c(), r.m(e, t)) : r && (r.d(1), r = null), (!s || u & /*size*/
      16) && j(
        n,
        "small",
        /*size*/
        o[4] === "small"
      ), (!s || u & /*size*/
      16) && j(
        n,
        "large",
        /*size*/
        o[4] === "large"
      ), (!s || u & /*size*/
      16) && j(
        n,
        "medium",
        /*size*/
        o[4] === "medium"
      ), (!s || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      o[7]), (!s || u & /*label*/
      2) && _e(
        e,
        "aria-label",
        /*label*/
        o[1]
      ), (!s || u & /*hasPopup*/
      256) && _e(
        e,
        "aria-haspopup",
        /*hasPopup*/
        o[8]
      ), (!s || u & /*label*/
      2) && _e(
        e,
        "title",
        /*label*/
        o[1]
      ), (!s || u & /*pending*/
      8) && j(
        e,
        "pending",
        /*pending*/
        o[3]
      ), (!s || u & /*padded*/
      32) && j(
        e,
        "padded",
        /*padded*/
        o[5]
      ), (!s || u & /*highlight*/
      64) && j(
        e,
        "highlight",
        /*highlight*/
        o[6]
      ), (!s || u & /*transparent*/
      512) && j(
        e,
        "transparent",
        /*transparent*/
        o[9]
      ), u & /*disabled, _color*/
      4224 && Me(e, "color", !/*disabled*/
      o[7] && /*_color*/
      o[12] ? (
        /*_color*/
        o[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && Me(e, "--bg-color", /*disabled*/
      o[7] ? "auto" : (
        /*background*/
        o[10]
      )), u & /*offset*/
      2048 && Me(
        e,
        "margin-left",
        /*offset*/
        o[11] + "px"
      );
    },
    i(o) {
      s || (Pn(i.$$.fragment, o), s = !0);
    },
    o(o) {
      Yn(i.$$.fragment, o), s = !1;
    },
    d(o) {
      o && dl(e), r && r.d(), En(i), f = !1, a();
    }
  };
}
function On(l, e, t) {
  let n, { Icon: i } = e, { label: s = "" } = e, { show_label: f = !1 } = e, { pending: a = !1 } = e, { size: r = "small" } = e, { padded: o = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: c = !1 } = e, { color: m = "var(--block-label-text-color)" } = e, { transparent: v = !1 } = e, { background: L = "var(--background-fill-primary)" } = e, { offset: w = 0 } = e;
  function H(b) {
    Sn.call(this, l, b);
  }
  return l.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, s = b.label), "show_label" in b && t(2, f = b.show_label), "pending" in b && t(3, a = b.pending), "size" in b && t(4, r = b.size), "padded" in b && t(5, o = b.padded), "highlight" in b && t(6, u = b.highlight), "disabled" in b && t(7, _ = b.disabled), "hasPopup" in b && t(8, c = b.hasPopup), "color" in b && t(13, m = b.color), "transparent" in b && t(9, v = b.transparent), "background" in b && t(10, L = b.background), "offset" in b && t(11, w = b.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : m);
  }, [
    i,
    s,
    f,
    a,
    r,
    o,
    u,
    _,
    c,
    v,
    L,
    w,
    n,
    m,
    H
  ];
}
class Un extends Zn {
  constructor(e) {
    super(), Tn(this, e, On, Kn, An, {
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
  SvelteComponent: Xn,
  append: ft,
  attr: J,
  detach: Gn,
  init: Rn,
  insert: Wn,
  noop: ot,
  safe_not_equal: Jn,
  set_style: oe,
  svg_element: Ye
} = window.__gradio__svelte__internal;
function Qn(l) {
  let e, t, n, i;
  return {
    c() {
      e = Ye("svg"), t = Ye("g"), n = Ye("path"), i = Ye("path"), J(n, "d", "M18,6L6.087,17.913"), oe(n, "fill", "none"), oe(n, "fill-rule", "nonzero"), oe(n, "stroke-width", "2px"), J(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), J(i, "d", "M4.364,4.364L19.636,19.636"), oe(i, "fill", "none"), oe(i, "fill-rule", "nonzero"), oe(i, "stroke-width", "2px"), J(e, "width", "100%"), J(e, "height", "100%"), J(e, "viewBox", "0 0 24 24"), J(e, "version", "1.1"), J(e, "xmlns", "http://www.w3.org/2000/svg"), J(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), J(e, "xml:space", "preserve"), J(e, "stroke", "currentColor"), oe(e, "fill-rule", "evenodd"), oe(e, "clip-rule", "evenodd"), oe(e, "stroke-linecap", "round"), oe(e, "stroke-linejoin", "round");
    },
    m(s, f) {
      Wn(s, e, f), ft(e, t), ft(t, n), ft(e, i);
    },
    p: ot,
    i: ot,
    o: ot,
    d(s) {
      s && Gn(e);
    }
  };
}
class xn extends Xn {
  constructor(e) {
    super(), Rn(this, e, null, Qn, Jn, {});
  }
}
const $n = [
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
], Ft = {
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
$n.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Ft[e][t],
      secondary: Ft[e][n]
    }
  }),
  {}
);
function Re() {
}
function ei(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const hl = typeof window < "u";
let Zt = hl ? () => window.performance.now() : () => Date.now(), bl = hl ? (l) => requestAnimationFrame(l) : Re;
const Se = /* @__PURE__ */ new Set();
function gl(l) {
  Se.forEach((e) => {
    e.c(l) || (Se.delete(e), e.f());
  }), Se.size !== 0 && bl(gl);
}
function ti(l) {
  let e;
  return Se.size === 0 && bl(gl), {
    promise: new Promise((t) => {
      Se.add(e = { c: l, f: t });
    }),
    abort() {
      Se.delete(e);
    }
  };
}
function li(l) {
  const e = l - 1;
  return e * e * e + 1;
}
const Ve = [];
function ni(l, e = Re) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(a) {
    if (ei(l, a) && (l = a, t)) {
      const r = !Ve.length;
      for (const o of n)
        o[1](), Ve.push(o, l);
      if (r) {
        for (let o = 0; o < Ve.length; o += 2)
          Ve[o][0](Ve[o + 1]);
        Ve.length = 0;
      }
    }
  }
  function s(a) {
    i(a(l));
  }
  function f(a, r = Re) {
    const o = [a, r];
    return n.add(o), n.size === 1 && (t = e(i, s) || Re), a(l), () => {
      n.delete(o), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: f };
}
function St(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function dt(l, e, t, n) {
  if (typeof t == "number" || St(t)) {
    const i = n - t, s = (t - e) / (l.dt || 1 / 60), f = l.opts.stiffness * i, a = l.opts.damping * s, r = (f - a) * l.inv_mass, o = (s + r) * l.dt;
    return Math.abs(o) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, St(t) ? new Date(t.getTime() + o) : t + o);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => dt(l, e[s], t[s], n[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = dt(l, e[s], t[s], n[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function zt(l, e = {}) {
  const t = ni(l), { stiffness: n = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let f, a, r, o = l, u = l, _ = 1, c = 0, m = !1;
  function v(w, H = {}) {
    u = w;
    const b = r = {};
    return l == null || H.hard || L.stiffness >= 1 && L.damping >= 1 ? (m = !0, f = Zt(), o = w, t.set(l = u), Promise.resolve()) : (H.soft && (c = 1 / ((H.soft === !0 ? 0.5 : +H.soft) * 60), _ = 0), a || (f = Zt(), m = !1, a = ti((h) => {
      if (m)
        return m = !1, a = null, !1;
      _ = Math.min(_ + c, 1);
      const p = {
        inv_mass: _,
        opts: L,
        settled: !0,
        dt: (h - f) * 60 / 1e3
      }, T = dt(p, o, l, u);
      return f = h, o = l, t.set(l = T), p.settled && (a = null), !p.settled;
    })), new Promise((h) => {
      a.promise.then(() => {
        b === r && h();
      });
    }));
  }
  const L = {
    set: v,
    update: (w, H) => v(w(u, l), H),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: s
  };
  return L;
}
function ii(l, { delay: e = 0, duration: t = 500, easing: n = li } = {}) {
  const i = parseFloat(getComputedStyle(l).height);
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (s) => {
      const f = s, a = `translateY(${(1 - s) * -10}px)`, r = s * i;
      return `
                opacity: ${f};
                transform: ${a};
                height: ${r}px;
            `;
    }
  };
}
const {
  SvelteComponent: si,
  action_destroyer: gt,
  add_render_callback: fi,
  append: F,
  attr: y,
  binding_callbacks: at,
  bubble: He,
  create_component: oi,
  create_in_transition: ai,
  destroy_component: ri,
  destroy_each: wl,
  detach: te,
  element: z,
  ensure_array_like: We,
  init: ui,
  insert: le,
  is_function: wt,
  listen: S,
  mount_component: _i,
  noop: je,
  run_all: vt,
  safe_not_equal: ci,
  set_data: kt,
  set_input_value: ze,
  space: ne,
  text: pt,
  toggle_class: Et,
  transition_in: rt,
  transition_out: di
} = window.__gradio__svelte__internal, { beforeUpdate: mi, afterUpdate: hi, createEventDispatcher: bi, tick: Tt } = window.__gradio__svelte__internal;
function Nt(l, e, t) {
  const n = l.slice();
  return n[51] = e[t], n;
}
function Bt(l, e, t) {
  const n = l.slice();
  return n[51] = e[t], n;
}
function gi(l) {
  let e;
  return {
    c() {
      e = pt(
        /*label*/
        l[3]
      );
    },
    m(t, n) {
      le(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      8 && kt(
        e,
        /*label*/
        t[3]
      );
    },
    d(t) {
      t && te(e);
    }
  };
}
function wi(l) {
  let e, t, n, i, s, f;
  return {
    c() {
      e = z("textarea"), y(e, "data-testid", "textbox"), y(e, "class", "scroll-hide svelte-ak29na"), y(e, "dir", t = /*rtl*/
      l[10] ? "rtl" : "ltr"), y(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), y(
        e,
        "rows",
        /*lines*/
        l[1]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[11], y(e, "style", n = /*text_align*/
      l[12] ? "text-align: " + /*text_align*/
      l[12] : "");
    },
    m(a, r) {
      le(a, e, r), ze(
        e,
        /*value*/
        l[0]
      ), l[42](e), /*autofocus*/
      l[11] && e.focus(), s || (f = [
        gt(i = /*text_area_resize*/
        l[23].call(
          null,
          e,
          /*value*/
          l[0]
        )),
        S(
          e,
          "input",
          /*textarea_input_handler_2*/
          l[41]
        ),
        S(
          e,
          "keypress",
          /*handle_keypress*/
          l[21]
        ),
        S(
          e,
          "blur",
          /*blur_handler_2*/
          l[31]
        ),
        S(
          e,
          "select",
          /*handle_select*/
          l[20]
        ),
        S(
          e,
          "focus",
          /*focus_handler_2*/
          l[32]
        ),
        S(
          e,
          "scroll",
          /*handle_scroll*/
          l[22]
        )
      ], s = !0);
    },
    p(a, r) {
      r[0] & /*rtl*/
      1024 && t !== (t = /*rtl*/
      a[10] ? "rtl" : "ltr") && y(e, "dir", t), r[0] & /*placeholder*/
      4 && y(
        e,
        "placeholder",
        /*placeholder*/
        a[2]
      ), r[0] & /*lines*/
      2 && y(
        e,
        "rows",
        /*lines*/
        a[1]
      ), r[0] & /*disabled*/
      32 && (e.disabled = /*disabled*/
      a[5]), r[0] & /*autofocus*/
      2048 && (e.autofocus = /*autofocus*/
      a[11]), r[0] & /*text_align*/
      4096 && n !== (n = /*text_align*/
      a[12] ? "text-align: " + /*text_align*/
      a[12] : "") && y(e, "style", n), i && wt(i.update) && r[0] & /*value*/
      1 && i.update.call(
        null,
        /*value*/
        a[0]
      ), r[0] & /*value*/
      1 && ze(
        e,
        /*value*/
        a[0]
      );
    },
    i: je,
    o: je,
    d(a) {
      a && te(e), l[42](null), s = !1, vt(f);
    }
  };
}
function vi(l) {
  let e, t, n, i, s, f, a, r, o;
  return {
    c() {
      e = z("div"), t = z("textarea"), f = ne(), a = z("button"), a.innerHTML = '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg" class="svelte-ak29na"><path d="M23.0978 15.6987L23.5777 15.2188L21.7538 13.3952L21.2739 13.8751L23.0978 15.6987ZM11.1253 2.74873L10.6454 3.22809L12.4035 4.98733L12.8834 4.50769L11.1253 2.74873ZM25.5996 9.23801H22.885V9.91673H25.5996V9.23801ZM10.6692 9.23801H7.95457V9.91673H10.6692V9.23801ZM21.8008 5.01533L23.5982 3.21773L23.118 2.73781L21.3206 4.53541L21.8008 5.01533ZM17.2391 7.29845L18.6858 8.74521C18.7489 8.80822 18.7989 8.88303 18.8331 8.96538C18.8672 9.04773 18.8847 9.13599 18.8847 9.22513C18.8847 9.31427 18.8672 9.40254 18.8331 9.48488C18.7989 9.56723 18.7489 9.64205 18.6858 9.70505L3.00501 25.3859C2.74013 25.6511 2.31061 25.6511 2.04517 25.3859L0.598406 23.9391C0.535351 23.8761 0.485329 23.8013 0.4512 23.719C0.417072 23.6366 0.399506 23.5483 0.399506 23.4592C0.399506 23.3701 0.417072 23.2818 0.4512 23.1995C0.485329 23.1171 0.535351 23.0423 0.598406 22.9793L16.2792 7.29845C16.3422 7.23533 16.417 7.18525 16.4994 7.15108C16.5817 7.11691 16.67 7.09932 16.7592 7.09932C16.8483 7.09932 16.9366 7.11691 17.019 7.15108C17.1013 7.18525 17.1761 7.23533 17.2391 7.29845ZM14.4231 13.2042L18.3792 9.24893L16.746 7.61541L12.7899 11.5713L14.4231 13.2042ZM17.4555 0.415771H16.7768V3.13037H17.4555V0.415771ZM17.4555 15.3462H16.7768V18.0608H17.4555V15.3462Z" fill="#CCCCCC" class="svelte-ak29na"></path></svg>', y(t, "data-testid", "textbox"), y(t, "class", "scroll-hide svelte-ak29na"), y(t, "dir", n = /*rtl*/
      l[10] ? "rtl" : "ltr"), y(
        t,
        "placeholder",
        /*placeholder*/
        l[2]
      ), y(
        t,
        "rows",
        /*lines*/
        l[1]
      ), t.disabled = /*disabled*/
      l[5], t.autofocus = /*autofocus*/
      l[11], y(t, "style", i = /*text_align*/
      l[12] ? "text-align: " + /*text_align*/
      l[12] : ""), y(a, "class", "extend_button svelte-ak29na"), y(a, "aria-label", "Extend"), y(a, "aria-roledescription", "Extend text"), y(e, "class", "magic_container svelte-ak29na");
    },
    m(u, _) {
      le(u, e, _), F(e, t), ze(
        t,
        /*value*/
        l[0]
      ), l[40](t), F(e, f), F(e, a), /*autofocus*/
      l[11] && t.focus(), r || (o = [
        gt(s = /*text_area_resize*/
        l[23].call(
          null,
          t,
          /*value*/
          l[0]
        )),
        S(
          t,
          "input",
          /*textarea_input_handler_1*/
          l[39]
        ),
        S(
          t,
          "keypress",
          /*handle_keypress*/
          l[21]
        ),
        S(
          t,
          "blur",
          /*blur_handler_1*/
          l[29]
        ),
        S(
          t,
          "select",
          /*handle_select*/
          l[20]
        ),
        S(
          t,
          "focus",
          /*focus_handler_1*/
          l[30]
        ),
        S(
          t,
          "scroll",
          /*handle_scroll*/
          l[22]
        ),
        S(
          a,
          "click",
          /*handle_extension*/
          l[17]
        )
      ], r = !0);
    },
    p(u, _) {
      _[0] & /*rtl*/
      1024 && n !== (n = /*rtl*/
      u[10] ? "rtl" : "ltr") && y(t, "dir", n), _[0] & /*placeholder*/
      4 && y(
        t,
        "placeholder",
        /*placeholder*/
        u[2]
      ), _[0] & /*lines*/
      2 && y(
        t,
        "rows",
        /*lines*/
        u[1]
      ), _[0] & /*disabled*/
      32 && (t.disabled = /*disabled*/
      u[5]), _[0] & /*autofocus*/
      2048 && (t.autofocus = /*autofocus*/
      u[11]), _[0] & /*text_align*/
      4096 && i !== (i = /*text_align*/
      u[12] ? "text-align: " + /*text_align*/
      u[12] : "") && y(t, "style", i), s && wt(s.update) && _[0] & /*value*/
      1 && s.update.call(
        null,
        /*value*/
        u[0]
      ), _[0] & /*value*/
      1 && ze(
        t,
        /*value*/
        u[0]
      );
    },
    i: je,
    o: je,
    d(u) {
      u && te(e), l[40](null), r = !1, vt(o);
    }
  };
}
function ki(l) {
  let e, t, n, i, s, f, a, r, o, u, _, c, m, v = (
    /*prompts*/
    l[8].length > 0 && At(l)
  ), L = (
    /*suffixes*/
    l[9].length > 0 && It(l)
  );
  return {
    c() {
      e = z("div"), t = z("textarea"), f = ne(), a = z("button"), a.innerHTML = '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg" class="svelte-ak29na"><path d="M23.0978 15.6987L23.5777 15.2188L21.7538 13.3952L21.2739 13.8751L23.0978 15.6987ZM11.1253 2.74873L10.6454 3.22809L12.4035 4.98733L12.8834 4.50769L11.1253 2.74873ZM25.5996 9.23801H22.885V9.91673H25.5996V9.23801ZM10.6692 9.23801H7.95457V9.91673H10.6692V9.23801ZM21.8008 5.01533L23.5982 3.21773L23.118 2.73781L21.3206 4.53541L21.8008 5.01533ZM17.2391 7.29845L18.6858 8.74521C18.7489 8.80822 18.7989 8.88303 18.8331 8.96538C18.8672 9.04773 18.8847 9.13599 18.8847 9.22513C18.8847 9.31427 18.8672 9.40254 18.8331 9.48488C18.7989 9.56723 18.7489 9.64205 18.6858 9.70505L3.00501 25.3859C2.74013 25.6511 2.31061 25.6511 2.04517 25.3859L0.598406 23.9391C0.535351 23.8761 0.485329 23.8013 0.4512 23.719C0.417072 23.6366 0.399506 23.5483 0.399506 23.4592C0.399506 23.3701 0.417072 23.2818 0.4512 23.1995C0.485329 23.1171 0.535351 23.0423 0.598406 22.9793L16.2792 7.29845C16.3422 7.23533 16.417 7.18525 16.4994 7.15108C16.5817 7.11691 16.67 7.09932 16.7592 7.09932C16.8483 7.09932 16.9366 7.11691 17.019 7.15108C17.1013 7.18525 17.1761 7.23533 17.2391 7.29845ZM14.4231 13.2042L18.3792 9.24893L16.746 7.61541L12.7899 11.5713L14.4231 13.2042ZM17.4555 0.415771H16.7768V3.13037H17.4555V0.415771ZM17.4555 15.3462H16.7768V18.0608H17.4555V15.3462Z" fill="#ff6700" class="svelte-ak29na"></path></svg>', r = ne(), o = z("div"), v && v.c(), u = ne(), L && L.c(), y(t, "data-testid", "textbox"), y(t, "class", "scroll-hide svelte-ak29na"), y(t, "dir", n = /*rtl*/
      l[10] ? "rtl" : "ltr"), y(
        t,
        "placeholder",
        /*placeholder*/
        l[2]
      ), y(
        t,
        "rows",
        /*lines*/
        l[1]
      ), t.disabled = /*disabled*/
      l[5], t.autofocus = /*autofocus*/
      l[11], y(t, "style", i = /*text_align*/
      l[12] ? "text-align: " + /*text_align*/
      l[12] : ""), y(a, "class", "extend_button svelte-ak29na"), y(a, "aria-label", "Extend"), y(a, "aria-roledescription", "Extend text"), y(e, "class", "magic_container svelte-ak29na"), y(o, "class", "menu svelte-ak29na");
    },
    m(w, H) {
      le(w, e, H), F(e, t), ze(
        t,
        /*value*/
        l[0]
      ), l[34](t), F(e, f), F(e, a), le(w, r, H), le(w, o, H), v && v.m(o, null), F(o, u), L && L.m(o, null), /*autofocus*/
      l[11] && t.focus(), c || (m = [
        gt(s = /*text_area_resize*/
        l[23].call(
          null,
          t,
          /*value*/
          l[0]
        )),
        S(
          t,
          "input",
          /*textarea_input_handler*/
          l[33]
        ),
        S(
          t,
          "keypress",
          /*handle_keypress*/
          l[21]
        ),
        S(
          t,
          "blur",
          /*blur_handler*/
          l[27]
        ),
        S(
          t,
          "select",
          /*handle_select*/
          l[20]
        ),
        S(
          t,
          "focus",
          /*focus_handler*/
          l[28]
        ),
        S(
          t,
          "scroll",
          /*handle_scroll*/
          l[22]
        ),
        S(
          a,
          "click",
          /*handle_extension*/
          l[17]
        ),
        S(
          o,
          "transitionstart",
          /*transitionstart_handler*/
          l[37]
        ),
        S(
          o,
          "transitionend",
          /*transitionend_handler*/
          l[38]
        )
      ], c = !0);
    },
    p(w, H) {
      H[0] & /*rtl*/
      1024 && n !== (n = /*rtl*/
      w[10] ? "rtl" : "ltr") && y(t, "dir", n), H[0] & /*placeholder*/
      4 && y(
        t,
        "placeholder",
        /*placeholder*/
        w[2]
      ), H[0] & /*lines*/
      2 && y(
        t,
        "rows",
        /*lines*/
        w[1]
      ), H[0] & /*disabled*/
      32 && (t.disabled = /*disabled*/
      w[5]), H[0] & /*autofocus*/
      2048 && (t.autofocus = /*autofocus*/
      w[11]), H[0] & /*text_align*/
      4096 && i !== (i = /*text_align*/
      w[12] ? "text-align: " + /*text_align*/
      w[12] : "") && y(t, "style", i), s && wt(s.update) && H[0] & /*value*/
      1 && s.update.call(
        null,
        /*value*/
        w[0]
      ), H[0] & /*value*/
      1 && ze(
        t,
        /*value*/
        w[0]
      ), /*prompts*/
      w[8].length > 0 ? v ? v.p(w, H) : (v = At(w), v.c(), v.m(o, u)) : v && (v.d(1), v = null), /*suffixes*/
      w[9].length > 0 ? L ? L.p(w, H) : (L = It(w), L.c(), L.m(o, null)) : L && (L.d(1), L = null);
    },
    i(w) {
      w && (_ || fi(() => {
        _ = ai(o, ii, { duration: 500 }), _.start();
      }));
    },
    o: je,
    d(w) {
      w && (te(e), te(r), te(o)), l[34](null), v && v.d(), L && L.d(), c = !1, vt(m);
    }
  };
}
function At(l) {
  let e, t, n, i, s = We(
    /*prompts*/
    l[8]
  ), f = [];
  for (let a = 0; a < s.length; a += 1)
    f[a] = Dt(Bt(l, s, a));
  return {
    c() {
      e = z("div"), t = z("span"), t.textContent = "A few prompt inspirations", n = ne(), i = z("ul");
      for (let a = 0; a < f.length; a += 1)
        f[a].c();
      y(i, "class", "svelte-ak29na"), y(e, "class", "menu_section_prompt svelte-ak29na");
    },
    m(a, r) {
      le(a, e, r), F(e, t), F(e, n), F(e, i);
      for (let o = 0; o < f.length; o += 1)
        f[o] && f[o].m(i, null);
    },
    p(a, r) {
      if (r[0] & /*loadPrompt, prompts*/
      524544) {
        s = We(
          /*prompts*/
          a[8]
        );
        let o;
        for (o = 0; o < s.length; o += 1) {
          const u = Bt(a, s, o);
          f[o] ? f[o].p(u, r) : (f[o] = Dt(u), f[o].c(), f[o].m(i, null));
        }
        for (; o < f.length; o += 1)
          f[o].d(1);
        f.length = s.length;
      }
    },
    d(a) {
      a && te(e), wl(f, a);
    }
  };
}
function Dt(l) {
  let e, t, n, i = (
    /*word*/
    l[51] + ""
  ), s, f, a, r, o, u;
  function _() {
    return (
      /*click_handler*/
      l[35](
        /*word*/
        l[51]
      )
    );
  }
  return {
    c() {
      e = z("li"), t = z("button"), n = z("div"), s = pt(i), f = ne(), a = z("div"), a.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="11" height="12" viewBox="0 0 11 12" fill="none" class="svelte-ak29na"><path d="M8.70801 5.51112H5.95801V2.57779C5.95801 2.44813 5.90972 2.32377 5.82376 2.23209C5.73781 2.14041 5.62123 2.0889 5.49967 2.0889C5.37812 2.0889 5.26154 2.14041 5.17558 2.23209C5.08963 2.32377 5.04134 2.44813 5.04134 2.57779V5.51112H2.29134C2.16978 5.51112 2.0532 5.56263 1.96725 5.65431C1.8813 5.746 1.83301 5.87035 1.83301 6.00001C1.83301 6.12967 1.8813 6.25402 1.96725 6.34571C2.0532 6.43739 2.16978 6.4889 2.29134 6.4889H5.04134V9.42223C5.04134 9.55189 5.08963 9.67624 5.17558 9.76793C5.26154 9.85961 5.37812 9.91112 5.49967 9.91112C5.62123 9.91112 5.73781 9.85961 5.82376 9.76793C5.90972 9.67624 5.95801 9.55189 5.95801 9.42223V6.4889H8.70801C8.82956 6.4889 8.94614 6.43739 9.0321 6.34571C9.11805 6.25402 9.16634 6.12967 9.16634 6.00001C9.16634 5.87035 9.11805 5.746 9.0321 5.65431C8.94614 5.56263 8.82956 5.51112 8.70801 5.51112Z" fill="#FF9A57" class="svelte-ak29na"></path></svg>', r = ne(), y(t, "class", "text_extension_button_prompt svelte-ak29na"), y(e, "class", "svelte-ak29na");
    },
    m(c, m) {
      le(c, e, m), F(e, t), F(t, n), F(n, s), F(t, f), F(t, a), F(e, r), o || (u = S(t, "click", _), o = !0);
    },
    p(c, m) {
      l = c, m[0] & /*prompts*/
      256 && i !== (i = /*word*/
      l[51] + "") && kt(s, i);
    },
    d(c) {
      c && te(e), o = !1, u();
    }
  };
}
function It(l) {
  let e, t, n, i, s = We(
    /*suffixes*/
    l[9]
  ), f = [];
  for (let a = 0; a < s.length; a += 1)
    f[a] = jt(Nt(l, s, a));
  return {
    c() {
      e = z("div"), t = z("span"), t.textContent = "Add keywords to guide style", n = ne(), i = z("ul");
      for (let a = 0; a < f.length; a += 1)
        f[a].c();
      y(i, "class", "svelte-ak29na"), y(e, "class", "menu_section_style svelte-ak29na");
    },
    m(a, r) {
      le(a, e, r), F(e, t), F(e, n), F(e, i);
      for (let o = 0; o < f.length; o += 1)
        f[o] && f[o].m(i, null);
    },
    p(a, r) {
      if (r[0] & /*addSuffix, suffixes*/
      262656) {
        s = We(
          /*suffixes*/
          a[9]
        );
        let o;
        for (o = 0; o < s.length; o += 1) {
          const u = Nt(a, s, o);
          f[o] ? f[o].p(u, r) : (f[o] = jt(u), f[o].c(), f[o].m(i, null));
        }
        for (; o < f.length; o += 1)
          f[o].d(1);
        f.length = s.length;
      }
    },
    d(a) {
      a && te(e), wl(f, a);
    }
  };
}
function jt(l) {
  let e, t, n, i = (
    /*word*/
    l[51] + ""
  ), s, f, a, r, o, u;
  function _() {
    return (
      /*click_handler_1*/
      l[36](
        /*word*/
        l[51]
      )
    );
  }
  return {
    c() {
      e = z("li"), t = z("button"), n = z("div"), s = pt(i), f = ne(), a = z("div"), a.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="11" height="12" viewBox="0 0 11 12" fill="none" class="svelte-ak29na"><path d="M8.70801 5.51112H5.95801V2.57779C5.95801 2.44813 5.90972 2.32377 5.82376 2.23209C5.73781 2.14041 5.62123 2.0889 5.49967 2.0889C5.37812 2.0889 5.26154 2.14041 5.17558 2.23209C5.08963 2.32377 5.04134 2.44813 5.04134 2.57779V5.51112H2.29134C2.16978 5.51112 2.0532 5.56263 1.96725 5.65431C1.8813 5.746 1.83301 5.87035 1.83301 6.00001C1.83301 6.12967 1.8813 6.25402 1.96725 6.34571C2.0532 6.43739 2.16978 6.4889 2.29134 6.4889H5.04134V9.42223C5.04134 9.55189 5.08963 9.67624 5.17558 9.76793C5.26154 9.85961 5.37812 9.91112 5.49967 9.91112C5.62123 9.91112 5.73781 9.85961 5.82376 9.76793C5.90972 9.67624 5.95801 9.55189 5.95801 9.42223V6.4889H8.70801C8.82956 6.4889 8.94614 6.43739 9.0321 6.34571C9.11805 6.25402 9.16634 6.12967 9.16634 6.00001C9.16634 5.87035 9.11805 5.746 9.0321 5.65431C8.94614 5.56263 8.82956 5.51112 8.70801 5.51112Z" fill="#FF9A57" class="svelte-ak29na"></path></svg>', r = ne(), y(t, "class", "text_extension_button svelte-ak29na"), y(e, "class", "svelte-ak29na");
    },
    m(c, m) {
      le(c, e, m), F(e, t), F(t, n), F(n, s), F(t, f), F(t, a), F(e, r), o || (u = S(t, "click", _), o = !0);
    },
    p(c, m) {
      l = c, m[0] & /*suffixes*/
      512 && i !== (i = /*word*/
      l[51] + "") && kt(s, i);
    },
    d(c) {
      c && te(e), o = !1, u();
    }
  };
}
function pi(l) {
  let e, t, n, i, s;
  t = new Fn({
    props: {
      show_label: (
        /*show_label*/
        l[6]
      ),
      info: (
        /*info*/
        l[4]
      ),
      $$slots: { default: [gi] },
      $$scope: { ctx: l }
    }
  });
  function f(o, u) {
    if (!/*ongoing_animation*/
    o[15] && /*show_menu*/
    o[14] && /*show_magic*/
    o[16])
      return ki;
    if (!/*ongoing_animation*/
    o[15] && !/*show_menu*/
    o[14] && /*show_magic*/
    o[16])
      return vi;
    if (!/*ongoing_animation*/
    o[15])
      return wi;
  }
  let a = f(l), r = a && a(l);
  return {
    c() {
      e = z("label"), oi(t.$$.fragment), n = ne(), i = z("div"), r && r.c(), y(i, "class", "input-container"), y(e, "class", "svelte-ak29na"), Et(
        e,
        "container",
        /*container*/
        l[7]
      );
    },
    m(o, u) {
      le(o, e, u), _i(t, e, null), F(e, n), F(e, i), r && r.m(i, null), s = !0;
    },
    p(o, u) {
      const _ = {};
      u[0] & /*show_label*/
      64 && (_.show_label = /*show_label*/
      o[6]), u[0] & /*info*/
      16 && (_.info = /*info*/
      o[4]), u[0] & /*label*/
      8 | u[1] & /*$$scope*/
      33554432 && (_.$$scope = { dirty: u, ctx: o }), t.$set(_), a === (a = f(o)) && r ? r.p(o, u) : (r && r.d(1), r = a && a(o), r && (r.c(), rt(r, 1), r.m(i, null))), (!s || u[0] & /*container*/
      128) && Et(
        e,
        "container",
        /*container*/
        o[7]
      );
    },
    i(o) {
      s || (rt(t.$$.fragment, o), rt(r), s = !0);
    },
    o(o) {
      di(t.$$.fragment, o), s = !1;
    },
    d(o) {
      o && te(e), ri(t), r && r.d();
    }
  };
}
function Ci(l, e, t) {
  var n = this && this.__awaiter || function(d, A, O, D) {
    function me(Ae) {
      return Ae instanceof O ? Ae : new O(function(Pe) {
        Pe(Ae);
      });
    }
    return new (O || (O = Promise))(function(Ae, Pe) {
      function ql(he) {
        try {
          it(D.next(he));
        } catch (st) {
          Pe(st);
        }
      }
      function Fl(he) {
        try {
          it(D.throw(he));
        } catch (st) {
          Pe(st);
        }
      }
      function it(he) {
        he.done ? Ae(he.value) : me(he.value).then(ql, Fl);
      }
      it((D = D.apply(d, A || [])).next());
    });
  };
  let { value: i = "" } = e, { value_is_output: s = !1 } = e, { lines: f = 1 } = e, { placeholder: a = "Type here..." } = e, { label: r } = e, { info: o = void 0 } = e, { disabled: u = !1 } = e, { show_label: _ = !0 } = e, { container: c = !0 } = e, { max_lines: m } = e, { prompts: v = [] } = e, { suffixes: L = [] } = e, { rtl: w = !1 } = e, { autofocus: H = !1 } = e, { text_align: b = void 0 } = e, { autoscroll: h = !0 } = e, p, T = !1, k, N = 0, B = !1, P = !1, Y = !P && (v.length > 0 || L.length > 0);
  const I = bi();
  mi(() => {
    k = p && p.offsetHeight + p.scrollTop > p.scrollHeight - 100;
  });
  const ie = () => {
    k && h && !B && p.scrollTo(0, p.scrollHeight);
  };
  function ge() {
    I("change", i), s || I("input");
  }
  hi(() => {
    H && p.focus(), k && h && ie(), t(24, s = !1), t(16, Y = !P && (v.length > 0 || L.length > 0));
  });
  function W() {
    return n(this, void 0, void 0, function* () {
      t(14, T = !T);
    });
  }
  function se(d) {
    i.trim() && t(0, i += ", "), t(0, i += `${d}`);
  }
  function K(d) {
    t(0, i += `${d}`);
  }
  function we(d) {
    const A = d.target, O = A.value, D = [A.selectionStart, A.selectionEnd];
    I("select", { value: O.substring(...D), index: D });
  }
  function Te(d) {
    return n(this, void 0, void 0, function* () {
      yield Tt(), (d.key === "Enter" && d.shiftKey && f > 1 || d.key === "Enter" && !d.shiftKey && f === 1 && m >= 1) && (d.preventDefault(), I("submit"));
    });
  }
  function ve(d) {
    const A = d.target, O = A.scrollTop;
    O < N && (B = !0), N = O;
    const D = A.scrollHeight - A.clientHeight;
    O >= D && (B = !1);
  }
  function g(d) {
    return n(this, void 0, void 0, function* () {
      if (yield Tt(), f === m)
        return;
      let A = m === void 0 ? !1 : m === void 0 ? 21 * 11 : 21 * (m + 1), O = 21 * (f + 1);
      const D = d.target;
      D.style.height = "1px";
      let me;
      A && D.scrollHeight > A ? me = A : D.scrollHeight < O ? me = O : me = D.scrollHeight, D.style.height = `${me}px`;
    });
  }
  function ke(d, A) {
    if (f !== m && (d.style.overflowY = "scroll", d.addEventListener("input", g), !!A.trim()))
      return g({ target: d }), {
        destroy: () => d.removeEventListener("input", g)
      };
  }
  function Qe(d) {
    He.call(this, l, d);
  }
  function xe(d) {
    He.call(this, l, d);
  }
  function $e(d) {
    He.call(this, l, d);
  }
  function C(d) {
    He.call(this, l, d);
  }
  function et(d) {
    He.call(this, l, d);
  }
  function pe(d) {
    He.call(this, l, d);
  }
  function Ce() {
    i = this.value, t(0, i);
  }
  function tt(d) {
    at[d ? "unshift" : "push"](() => {
      p = d, t(13, p);
    });
  }
  const de = (d) => K(d), ye = (d) => se(d), lt = () => t(15, P = !0), nt = () => t(15, P = !1);
  function Ne() {
    i = this.value, t(0, i);
  }
  function ue(d) {
    at[d ? "unshift" : "push"](() => {
      p = d, t(13, p);
    });
  }
  function Be() {
    i = this.value, t(0, i);
  }
  function Hl(d) {
    at[d ? "unshift" : "push"](() => {
      p = d, t(13, p);
    });
  }
  return l.$$set = (d) => {
    "value" in d && t(0, i = d.value), "value_is_output" in d && t(24, s = d.value_is_output), "lines" in d && t(1, f = d.lines), "placeholder" in d && t(2, a = d.placeholder), "label" in d && t(3, r = d.label), "info" in d && t(4, o = d.info), "disabled" in d && t(5, u = d.disabled), "show_label" in d && t(6, _ = d.show_label), "container" in d && t(7, c = d.container), "max_lines" in d && t(25, m = d.max_lines), "prompts" in d && t(8, v = d.prompts), "suffixes" in d && t(9, L = d.suffixes), "rtl" in d && t(10, w = d.rtl), "autofocus" in d && t(11, H = d.autofocus), "text_align" in d && t(12, b = d.text_align), "autoscroll" in d && t(26, h = d.autoscroll);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1 && i === null && t(0, i = ""), l.$$.dirty[0] & /*value, el, lines, max_lines*/
    33562627 && p && f !== m && g({ target: p }), l.$$.dirty[0] & /*value*/
    1 && ge();
  }, [
    i,
    f,
    a,
    r,
    o,
    u,
    _,
    c,
    v,
    L,
    w,
    H,
    b,
    p,
    T,
    P,
    Y,
    W,
    se,
    K,
    we,
    Te,
    ve,
    ke,
    s,
    m,
    h,
    Qe,
    xe,
    $e,
    C,
    et,
    pe,
    Ce,
    tt,
    de,
    ye,
    lt,
    nt,
    Ne,
    ue,
    Be,
    Hl
  ];
}
class yi extends si {
  constructor(e) {
    super(), ui(
      this,
      e,
      Ci,
      pi,
      ci,
      {
        value: 0,
        value_is_output: 24,
        lines: 1,
        placeholder: 2,
        label: 3,
        info: 4,
        disabled: 5,
        show_label: 6,
        container: 7,
        max_lines: 25,
        prompts: 8,
        suffixes: 9,
        rtl: 10,
        autofocus: 11,
        text_align: 12,
        autoscroll: 26
      },
      null,
      [-1, -1]
    );
  }
}
function Fe(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
const {
  SvelteComponent: Li,
  append: Q,
  attr: q,
  component_subscribe: Pt,
  detach: Mi,
  element: Vi,
  init: Hi,
  insert: qi,
  noop: Yt,
  safe_not_equal: Fi,
  set_style: Ke,
  svg_element: x,
  toggle_class: Kt
} = window.__gradio__svelte__internal, { onMount: Zi } = window.__gradio__svelte__internal;
function Si(l) {
  let e, t, n, i, s, f, a, r, o, u, _, c;
  return {
    c() {
      e = Vi("div"), t = x("svg"), n = x("g"), i = x("path"), s = x("path"), f = x("path"), a = x("path"), r = x("g"), o = x("path"), u = x("path"), _ = x("path"), c = x("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(s, "fill", "#FF7C00"), q(s, "class", "svelte-43sxxs"), q(f, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(f, "fill", "#FF7C00"), q(f, "fill-opacity", "0.4"), q(f, "class", "svelte-43sxxs"), q(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(a, "fill", "#FF7C00"), q(a, "class", "svelte-43sxxs"), Ke(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), q(o, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(o, "fill", "#FF7C00"), q(o, "fill-opacity", "0.4"), q(o, "class", "svelte-43sxxs"), q(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(u, "fill", "#FF7C00"), q(u, "class", "svelte-43sxxs"), q(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(_, "fill", "#FF7C00"), q(_, "fill-opacity", "0.4"), q(_, "class", "svelte-43sxxs"), q(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(c, "fill", "#FF7C00"), q(c, "class", "svelte-43sxxs"), Ke(r, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), Kt(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(m, v) {
      qi(m, e, v), Q(e, t), Q(t, n), Q(n, i), Q(n, s), Q(n, f), Q(n, a), Q(t, r), Q(r, o), Q(r, u), Q(r, _), Q(r, c);
    },
    p(m, [v]) {
      v & /*$top*/
      2 && Ke(n, "transform", "translate(" + /*$top*/
      m[1][0] + "px, " + /*$top*/
      m[1][1] + "px)"), v & /*$bottom*/
      4 && Ke(r, "transform", "translate(" + /*$bottom*/
      m[2][0] + "px, " + /*$bottom*/
      m[2][1] + "px)"), v & /*margin*/
      1 && Kt(
        e,
        "margin",
        /*margin*/
        m[0]
      );
    },
    i: Yt,
    o: Yt,
    d(m) {
      m && Mi(e);
    }
  };
}
function zi(l, e, t) {
  let n, i;
  var s = this && this.__awaiter || function(m, v, L, w) {
    function H(b) {
      return b instanceof L ? b : new L(function(h) {
        h(b);
      });
    }
    return new (L || (L = Promise))(function(b, h) {
      function p(N) {
        try {
          k(w.next(N));
        } catch (B) {
          h(B);
        }
      }
      function T(N) {
        try {
          k(w.throw(N));
        } catch (B) {
          h(B);
        }
      }
      function k(N) {
        N.done ? b(N.value) : H(N.value).then(p, T);
      }
      k((w = w.apply(m, v || [])).next());
    });
  };
  let { margin: f = !0 } = e;
  const a = zt([0, 0]);
  Pt(l, a, (m) => t(1, n = m));
  const r = zt([0, 0]);
  Pt(l, r, (m) => t(2, i = m));
  let o;
  function u() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 140]), r.set([-125, -140])]), yield Promise.all([a.set([-125, 140]), r.set([125, -140])]), yield Promise.all([a.set([-125, 0]), r.set([125, -0])]), yield Promise.all([a.set([125, 0]), r.set([-125, 0])]);
    });
  }
  function _() {
    return s(this, void 0, void 0, function* () {
      yield u(), o || _();
    });
  }
  function c() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 0]), r.set([-125, 0])]), _();
    });
  }
  return Zi(() => (c(), () => o = !0)), l.$$set = (m) => {
    "margin" in m && t(0, f = m.margin);
  }, [f, n, i, a, r];
}
class Ei extends Li {
  constructor(e) {
    super(), Hi(this, e, zi, Si, Fi, { margin: 0 });
  }
}
const {
  SvelteComponent: Ti,
  append: be,
  attr: ee,
  binding_callbacks: Ot,
  check_outros: mt,
  create_component: vl,
  create_slot: kl,
  destroy_component: pl,
  destroy_each: Cl,
  detach: M,
  element: ae,
  empty: Ee,
  ensure_array_like: Je,
  get_all_dirty_from_scope: yl,
  get_slot_changes: Ll,
  group_outros: ht,
  init: Ni,
  insert: V,
  mount_component: Ml,
  noop: bt,
  safe_not_equal: Bi,
  set_data: R,
  set_style: ce,
  space: G,
  text: E,
  toggle_class: X,
  transition_in: $,
  transition_out: re,
  update_slot_base: Vl
} = window.__gradio__svelte__internal, { tick: Ai } = window.__gradio__svelte__internal, { onDestroy: Di } = window.__gradio__svelte__internal, { createEventDispatcher: Ii } = window.__gradio__svelte__internal, ji = (l) => ({}), Ut = (l) => ({}), Pi = (l) => ({}), Xt = (l) => ({});
function Gt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function Rt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Yi(l) {
  let e, t, n, i, s = (
    /*i18n*/
    l[1]("common.error") + ""
  ), f, a, r;
  t = new Un({
    props: {
      Icon: xn,
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
  const o = (
    /*#slots*/
    l[30].error
  ), u = kl(
    o,
    l,
    /*$$scope*/
    l[29],
    Ut
  );
  return {
    c() {
      e = ae("div"), vl(t.$$.fragment), n = G(), i = ae("span"), f = E(s), a = G(), u && u.c(), ee(e, "class", "clear-status svelte-vopvsi"), ee(i, "class", "error svelte-vopvsi");
    },
    m(_, c) {
      V(_, e, c), Ml(t, e, null), V(_, n, c), V(_, i, c), be(i, f), V(_, a, c), u && u.m(_, c), r = !0;
    },
    p(_, c) {
      const m = {};
      c[0] & /*i18n*/
      2 && (m.label = /*i18n*/
      _[1]("common.clear")), t.$set(m), (!r || c[0] & /*i18n*/
      2) && s !== (s = /*i18n*/
      _[1]("common.error") + "") && R(f, s), u && u.p && (!r || c[0] & /*$$scope*/
      536870912) && Vl(
        u,
        o,
        _,
        /*$$scope*/
        _[29],
        r ? Ll(
          o,
          /*$$scope*/
          _[29],
          c,
          ji
        ) : yl(
          /*$$scope*/
          _[29]
        ),
        Ut
      );
    },
    i(_) {
      r || ($(t.$$.fragment, _), $(u, _), r = !0);
    },
    o(_) {
      re(t.$$.fragment, _), re(u, _), r = !1;
    },
    d(_) {
      _ && (M(e), M(n), M(i), M(a)), pl(t), u && u.d(_);
    }
  };
}
function Ki(l) {
  let e, t, n, i, s, f, a, r, o, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Wt(l)
  );
  function _(h, p) {
    if (
      /*progress*/
      h[7]
    )
      return Xi;
    if (
      /*queue_position*/
      h[2] !== null && /*queue_size*/
      h[3] !== void 0 && /*queue_position*/
      h[2] >= 0
    )
      return Ui;
    if (
      /*queue_position*/
      h[2] === 0
    )
      return Oi;
  }
  let c = _(l), m = c && c(l), v = (
    /*timer*/
    l[5] && xt(l)
  );
  const L = [Ji, Wi], w = [];
  function H(h, p) {
    return (
      /*last_progress_level*/
      h[15] != null ? 0 : (
        /*show_progress*/
        h[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = H(l)) && (f = w[s] = L[s](l));
  let b = !/*timer*/
  l[5] && sl(l);
  return {
    c() {
      u && u.c(), e = G(), t = ae("div"), m && m.c(), n = G(), v && v.c(), i = G(), f && f.c(), a = G(), b && b.c(), r = Ee(), ee(t, "class", "progress-text svelte-vopvsi"), X(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), X(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(h, p) {
      u && u.m(h, p), V(h, e, p), V(h, t, p), m && m.m(t, null), be(t, n), v && v.m(t, null), V(h, i, p), ~s && w[s].m(h, p), V(h, a, p), b && b.m(h, p), V(h, r, p), o = !0;
    },
    p(h, p) {
      /*variant*/
      h[8] === "default" && /*show_eta_bar*/
      h[18] && /*show_progress*/
      h[6] === "full" ? u ? u.p(h, p) : (u = Wt(h), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), c === (c = _(h)) && m ? m.p(h, p) : (m && m.d(1), m = c && c(h), m && (m.c(), m.m(t, n))), /*timer*/
      h[5] ? v ? v.p(h, p) : (v = xt(h), v.c(), v.m(t, null)) : v && (v.d(1), v = null), (!o || p[0] & /*variant*/
      256) && X(
        t,
        "meta-text-center",
        /*variant*/
        h[8] === "center"
      ), (!o || p[0] & /*variant*/
      256) && X(
        t,
        "meta-text",
        /*variant*/
        h[8] === "default"
      );
      let T = s;
      s = H(h), s === T ? ~s && w[s].p(h, p) : (f && (ht(), re(w[T], 1, 1, () => {
        w[T] = null;
      }), mt()), ~s ? (f = w[s], f ? f.p(h, p) : (f = w[s] = L[s](h), f.c()), $(f, 1), f.m(a.parentNode, a)) : f = null), /*timer*/
      h[5] ? b && (ht(), re(b, 1, 1, () => {
        b = null;
      }), mt()) : b ? (b.p(h, p), p[0] & /*timer*/
      32 && $(b, 1)) : (b = sl(h), b.c(), $(b, 1), b.m(r.parentNode, r));
    },
    i(h) {
      o || ($(f), $(b), o = !0);
    },
    o(h) {
      re(f), re(b), o = !1;
    },
    d(h) {
      h && (M(e), M(t), M(i), M(a), M(r)), u && u.d(h), m && m.d(), v && v.d(), ~s && w[s].d(h), b && b.d(h);
    }
  };
}
function Wt(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ae("div"), ee(e, "class", "eta-bar svelte-vopvsi"), ce(e, "transform", t);
    },
    m(n, i) {
      V(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ce(e, "transform", t);
    },
    d(n) {
      n && M(e);
    }
  };
}
function Oi(l) {
  let e;
  return {
    c() {
      e = E("processing |");
    },
    m(t, n) {
      V(t, e, n);
    },
    p: bt,
    d(t) {
      t && M(e);
    }
  };
}
function Ui(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, s, f;
  return {
    c() {
      e = E("queue: "), n = E(t), i = E("/"), s = E(
        /*queue_size*/
        l[3]
      ), f = E(" |");
    },
    m(a, r) {
      V(a, e, r), V(a, n, r), V(a, i, r), V(a, s, r), V(a, f, r);
    },
    p(a, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      a[2] + 1 + "") && R(n, t), r[0] & /*queue_size*/
      8 && R(
        s,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (M(e), M(n), M(i), M(s), M(f));
    }
  };
}
function Xi(l) {
  let e, t = Je(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Qt(Rt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ee();
    },
    m(i, s) {
      for (let f = 0; f < n.length; f += 1)
        n[f] && n[f].m(i, s);
      V(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = Je(
          /*progress*/
          i[7]
        );
        let f;
        for (f = 0; f < t.length; f += 1) {
          const a = Rt(i, t, f);
          n[f] ? n[f].p(a, s) : (n[f] = Qt(a), n[f].c(), n[f].m(e.parentNode, e));
        }
        for (; f < n.length; f += 1)
          n[f].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && M(e), Cl(n, i);
    }
  };
}
function Jt(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, s = " ", f;
  function a(u, _) {
    return (
      /*p*/
      u[41].length != null ? Ri : Gi
    );
  }
  let r = a(l), o = r(l);
  return {
    c() {
      o.c(), e = G(), n = E(t), i = E(" | "), f = E(s);
    },
    m(u, _) {
      o.m(u, _), V(u, e, _), V(u, n, _), V(u, i, _), V(u, f, _);
    },
    p(u, _) {
      r === (r = a(u)) && o ? o.p(u, _) : (o.d(1), o = r(u), o && (o.c(), o.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && R(n, t);
    },
    d(u) {
      u && (M(e), M(n), M(i), M(f)), o.d(u);
    }
  };
}
function Gi(l) {
  let e = Fe(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = E(e);
    },
    m(n, i) {
      V(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Fe(
        /*p*/
        n[41].index || 0
      ) + "") && R(t, e);
    },
    d(n) {
      n && M(t);
    }
  };
}
function Ri(l) {
  let e = Fe(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = Fe(
    /*p*/
    l[41].length
  ) + "", s;
  return {
    c() {
      t = E(e), n = E("/"), s = E(i);
    },
    m(f, a) {
      V(f, t, a), V(f, n, a), V(f, s, a);
    },
    p(f, a) {
      a[0] & /*progress*/
      128 && e !== (e = Fe(
        /*p*/
        f[41].index || 0
      ) + "") && R(t, e), a[0] & /*progress*/
      128 && i !== (i = Fe(
        /*p*/
        f[41].length
      ) + "") && R(s, i);
    },
    d(f) {
      f && (M(t), M(n), M(s));
    }
  };
}
function Qt(l) {
  let e, t = (
    /*p*/
    l[41].index != null && Jt(l)
  );
  return {
    c() {
      t && t.c(), e = Ee();
    },
    m(n, i) {
      t && t.m(n, i), V(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = Jt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && M(e), t && t.d(n);
    }
  };
}
function xt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = E(
        /*formatted_timer*/
        l[20]
      ), n = E(t), i = E("s");
    },
    m(s, f) {
      V(s, e, f), V(s, n, f), V(s, i, f);
    },
    p(s, f) {
      f[0] & /*formatted_timer*/
      1048576 && R(
        e,
        /*formatted_timer*/
        s[20]
      ), f[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && R(n, t);
    },
    d(s) {
      s && (M(e), M(n), M(i));
    }
  };
}
function Wi(l) {
  let e, t;
  return e = new Ei({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      vl(e.$$.fragment);
    },
    m(n, i) {
      Ml(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      t || ($(e.$$.fragment, n), t = !0);
    },
    o(n) {
      re(e.$$.fragment, n), t = !1;
    },
    d(n) {
      pl(e, n);
    }
  };
}
function Ji(l) {
  let e, t, n, i, s, f = `${/*last_progress_level*/
  l[15] * 100}%`, a = (
    /*progress*/
    l[7] != null && $t(l)
  );
  return {
    c() {
      e = ae("div"), t = ae("div"), a && a.c(), n = G(), i = ae("div"), s = ae("div"), ee(t, "class", "progress-level-inner svelte-vopvsi"), ee(s, "class", "progress-bar svelte-vopvsi"), ce(s, "width", f), ee(i, "class", "progress-bar-wrap svelte-vopvsi"), ee(e, "class", "progress-level svelte-vopvsi");
    },
    m(r, o) {
      V(r, e, o), be(e, t), a && a.m(t, null), be(e, n), be(e, i), be(i, s), l[31](s);
    },
    p(r, o) {
      /*progress*/
      r[7] != null ? a ? a.p(r, o) : (a = $t(r), a.c(), a.m(t, null)) : a && (a.d(1), a = null), o[0] & /*last_progress_level*/
      32768 && f !== (f = `${/*last_progress_level*/
      r[15] * 100}%`) && ce(s, "width", f);
    },
    i: bt,
    o: bt,
    d(r) {
      r && M(e), a && a.d(), l[31](null);
    }
  };
}
function $t(l) {
  let e, t = Je(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = il(Gt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Ee();
    },
    m(i, s) {
      for (let f = 0; f < n.length; f += 1)
        n[f] && n[f].m(i, s);
      V(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = Je(
          /*progress*/
          i[7]
        );
        let f;
        for (f = 0; f < t.length; f += 1) {
          const a = Gt(i, t, f);
          n[f] ? n[f].p(a, s) : (n[f] = il(a), n[f].c(), n[f].m(e.parentNode, e));
        }
        for (; f < n.length; f += 1)
          n[f].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && M(e), Cl(n, i);
    }
  };
}
function el(l) {
  let e, t, n, i, s = (
    /*i*/
    l[43] !== 0 && Qi()
  ), f = (
    /*p*/
    l[41].desc != null && tl(l)
  ), a = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && ll()
  ), r = (
    /*progress_level*/
    l[14] != null && nl(l)
  );
  return {
    c() {
      s && s.c(), e = G(), f && f.c(), t = G(), a && a.c(), n = G(), r && r.c(), i = Ee();
    },
    m(o, u) {
      s && s.m(o, u), V(o, e, u), f && f.m(o, u), V(o, t, u), a && a.m(o, u), V(o, n, u), r && r.m(o, u), V(o, i, u);
    },
    p(o, u) {
      /*p*/
      o[41].desc != null ? f ? f.p(o, u) : (f = tl(o), f.c(), f.m(t.parentNode, t)) : f && (f.d(1), f = null), /*p*/
      o[41].desc != null && /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? a || (a = ll(), a.c(), a.m(n.parentNode, n)) : a && (a.d(1), a = null), /*progress_level*/
      o[14] != null ? r ? r.p(o, u) : (r = nl(o), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(o) {
      o && (M(e), M(t), M(n), M(i)), s && s.d(o), f && f.d(o), a && a.d(o), r && r.d(o);
    }
  };
}
function Qi(l) {
  let e;
  return {
    c() {
      e = E(" /");
    },
    m(t, n) {
      V(t, e, n);
    },
    d(t) {
      t && M(e);
    }
  };
}
function tl(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = E(e);
    },
    m(n, i) {
      V(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && R(t, e);
    },
    d(n) {
      n && M(t);
    }
  };
}
function ll(l) {
  let e;
  return {
    c() {
      e = E("-");
    },
    m(t, n) {
      V(t, e, n);
    },
    d(t) {
      t && M(e);
    }
  };
}
function nl(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = E(e), n = E("%");
    },
    m(i, s) {
      V(i, t, s), V(i, n, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && R(t, e);
    },
    d(i) {
      i && (M(t), M(n));
    }
  };
}
function il(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && el(l)
  );
  return {
    c() {
      t && t.c(), e = Ee();
    },
    m(n, i) {
      t && t.m(n, i), V(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = el(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && M(e), t && t.d(n);
    }
  };
}
function sl(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), f = kl(
    s,
    l,
    /*$$scope*/
    l[29],
    Xt
  );
  return {
    c() {
      e = ae("p"), t = E(
        /*loading_text*/
        l[9]
      ), n = G(), f && f.c(), ee(e, "class", "loading svelte-vopvsi");
    },
    m(a, r) {
      V(a, e, r), be(e, t), V(a, n, r), f && f.m(a, r), i = !0;
    },
    p(a, r) {
      (!i || r[0] & /*loading_text*/
      512) && R(
        t,
        /*loading_text*/
        a[9]
      ), f && f.p && (!i || r[0] & /*$$scope*/
      536870912) && Vl(
        f,
        s,
        a,
        /*$$scope*/
        a[29],
        i ? Ll(
          s,
          /*$$scope*/
          a[29],
          r,
          Pi
        ) : yl(
          /*$$scope*/
          a[29]
        ),
        Xt
      );
    },
    i(a) {
      i || ($(f, a), i = !0);
    },
    o(a) {
      re(f, a), i = !1;
    },
    d(a) {
      a && (M(e), M(n)), f && f.d(a);
    }
  };
}
function xi(l) {
  let e, t, n, i, s;
  const f = [Ki, Yi], a = [];
  function r(o, u) {
    return (
      /*status*/
      o[4] === "pending" ? 0 : (
        /*status*/
        o[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(l)) && (n = a[t] = f[t](l)), {
    c() {
      e = ae("div"), n && n.c(), ee(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-vopvsi"), X(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), X(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), X(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), X(
        e,
        "border",
        /*border*/
        l[12]
      ), ce(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), ce(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(o, u) {
      V(o, e, u), ~t && a[t].m(e, null), l[33](e), s = !0;
    },
    p(o, u) {
      let _ = t;
      t = r(o), t === _ ? ~t && a[t].p(o, u) : (n && (ht(), re(a[_], 1, 1, () => {
        a[_] = null;
      }), mt()), ~t ? (n = a[t], n ? n.p(o, u) : (n = a[t] = f[t](o), n.c()), $(n, 1), n.m(e, null)) : n = null), (!s || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      o[8] + " " + /*show_progress*/
      o[6] + " svelte-vopvsi")) && ee(e, "class", i), (!s || u[0] & /*variant, show_progress, status, show_progress*/
      336) && X(e, "hide", !/*status*/
      o[4] || /*status*/
      o[4] === "complete" || /*show_progress*/
      o[6] === "hidden"), (!s || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && X(
        e,
        "translucent",
        /*variant*/
        o[8] === "center" && /*status*/
        (o[4] === "pending" || /*status*/
        o[4] === "error") || /*translucent*/
        o[11] || /*show_progress*/
        o[6] === "minimal"
      ), (!s || u[0] & /*variant, show_progress, status*/
      336) && X(
        e,
        "generating",
        /*status*/
        o[4] === "generating"
      ), (!s || u[0] & /*variant, show_progress, border*/
      4416) && X(
        e,
        "border",
        /*border*/
        o[12]
      ), u[0] & /*absolute*/
      1024 && ce(
        e,
        "position",
        /*absolute*/
        o[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && ce(
        e,
        "padding",
        /*absolute*/
        o[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(o) {
      s || ($(n), s = !0);
    },
    o(o) {
      re(n), s = !1;
    },
    d(o) {
      o && M(e), ~t && a[t].d(), l[33](null);
    }
  };
}
var $i = function(l, e, t, n) {
  function i(s) {
    return s instanceof t ? s : new t(function(f) {
      f(s);
    });
  }
  return new (t || (t = Promise))(function(s, f) {
    function a(u) {
      try {
        o(n.next(u));
      } catch (_) {
        f(_);
      }
    }
    function r(u) {
      try {
        o(n.throw(u));
      } catch (_) {
        f(_);
      }
    }
    function o(u) {
      u.done ? s(u.value) : i(u.value).then(a, r);
    }
    o((n = n.apply(l, e || [])).next());
  });
};
let Oe = [], ut = !1;
function es(l) {
  return $i(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Oe.push(e), !ut)
        ut = !0;
      else
        return;
      yield Ai(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < Oe.length; i++) {
          const f = Oe[i].getBoundingClientRect();
          (i === 0 || f.top + window.scrollY <= n[0]) && (n[0] = f.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), ut = !1, Oe = [];
      });
    }
  });
}
function ts(l, e, t) {
  let n, { $$slots: i = {}, $$scope: s } = e;
  this && this.__awaiter;
  const f = Ii();
  let { i18n: a } = e, { eta: r = null } = e, { queue_position: o } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: c = !1 } = e, { timer: m = !0 } = e, { show_progress: v = "full" } = e, { message: L = null } = e, { progress: w = null } = e, { variant: H = "default" } = e, { loading_text: b = "Loading..." } = e, { absolute: h = !0 } = e, { translucent: p = !1 } = e, { border: T = !1 } = e, { autoscroll: k } = e, N, B = !1, P = 0, Y = 0, I = null, ie = null, ge = 0, W = null, se, K = null, we = !0;
  const Te = () => {
    t(0, r = t(27, I = t(19, ke = null))), t(25, P = performance.now()), t(26, Y = 0), B = !0, ve();
  };
  function ve() {
    requestAnimationFrame(() => {
      t(26, Y = (performance.now() - P) / 1e3), B && ve();
    });
  }
  function g() {
    t(26, Y = 0), t(0, r = t(27, I = t(19, ke = null))), B && (B = !1);
  }
  Di(() => {
    B && g();
  });
  let ke = null;
  function Qe(C) {
    Ot[C ? "unshift" : "push"](() => {
      K = C, t(16, K), t(7, w), t(14, W), t(15, se);
    });
  }
  const xe = () => {
    f("clear_status");
  };
  function $e(C) {
    Ot[C ? "unshift" : "push"](() => {
      N = C, t(13, N);
    });
  }
  return l.$$set = (C) => {
    "i18n" in C && t(1, a = C.i18n), "eta" in C && t(0, r = C.eta), "queue_position" in C && t(2, o = C.queue_position), "queue_size" in C && t(3, u = C.queue_size), "status" in C && t(4, _ = C.status), "scroll_to_output" in C && t(22, c = C.scroll_to_output), "timer" in C && t(5, m = C.timer), "show_progress" in C && t(6, v = C.show_progress), "message" in C && t(23, L = C.message), "progress" in C && t(7, w = C.progress), "variant" in C && t(8, H = C.variant), "loading_text" in C && t(9, b = C.loading_text), "absolute" in C && t(10, h = C.absolute), "translucent" in C && t(11, p = C.translucent), "border" in C && t(12, T = C.border), "autoscroll" in C && t(24, k = C.autoscroll), "$$scope" in C && t(29, s = C.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (r === null && t(0, r = I), r != null && I !== r && (t(28, ie = (performance.now() - P) / 1e3 + r), t(19, ke = ie.toFixed(1)), t(27, I = r))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ge = ie === null || ie <= 0 || !Y ? null : Math.min(Y / ie, 1)), l.$$.dirty[0] & /*progress*/
    128 && w != null && t(18, we = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (w != null ? t(14, W = w.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : t(14, W = null), W ? (t(15, se = W[W.length - 1]), K && (se === 0 ? t(16, K.style.transition = "0", K) : t(16, K.style.transition = "150ms", K))) : t(15, se = void 0)), l.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? Te() : g()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && N && c && (_ === "pending" || _ === "complete") && es(N, k), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = Y.toFixed(1));
  }, [
    r,
    a,
    o,
    u,
    _,
    m,
    v,
    w,
    H,
    b,
    h,
    p,
    T,
    N,
    W,
    se,
    K,
    ge,
    we,
    ke,
    n,
    f,
    c,
    L,
    k,
    P,
    Y,
    I,
    ie,
    s,
    i,
    Qe,
    xe,
    $e
  ];
}
class ls extends Ti {
  constructor(e) {
    super(), Ni(
      this,
      e,
      ts,
      xi,
      Bi,
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
  SvelteComponent: ns,
  add_iframe_resize_listener: is,
  add_render_callback: ss,
  append: fs,
  attr: os,
  binding_callbacks: as,
  detach: rs,
  element: us,
  init: _s,
  insert: cs,
  noop: fl,
  safe_not_equal: ds,
  set_data: ms,
  text: hs,
  toggle_class: qe
} = window.__gradio__svelte__internal, { onMount: bs } = window.__gradio__svelte__internal;
function gs(l) {
  let e, t = (
    /*value*/
    (l[0] ? (
      /*value*/
      l[0]
    ) : "") + ""
  ), n, i;
  return {
    c() {
      e = us("div"), n = hs(t), os(e, "class", "svelte-84cxb8"), ss(() => (
        /*div_elementresize_handler*/
        l[5].call(e)
      )), qe(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), qe(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), qe(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    m(s, f) {
      cs(s, e, f), fs(e, n), i = is(
        e,
        /*div_elementresize_handler*/
        l[5].bind(e)
      ), l[6](e);
    },
    p(s, [f]) {
      f & /*value*/
      1 && t !== (t = /*value*/
      (s[0] ? (
        /*value*/
        s[0]
      ) : "") + "") && ms(n, t), f & /*type*/
      2 && qe(
        e,
        "table",
        /*type*/
        s[1] === "table"
      ), f & /*type*/
      2 && qe(
        e,
        "gallery",
        /*type*/
        s[1] === "gallery"
      ), f & /*selected*/
      4 && qe(
        e,
        "selected",
        /*selected*/
        s[2]
      );
    },
    i: fl,
    o: fl,
    d(s) {
      s && rs(e), i(), l[6](null);
    }
  };
}
function ws(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: s = !1 } = e, f, a;
  function r(_, c) {
    !_ || !c || (a.style.setProperty("--local-text-width", `${c < 150 ? c : 200}px`), t(4, a.style.whiteSpace = "unset", a));
  }
  bs(() => {
    r(a, f);
  });
  function o() {
    f = this.clientWidth, t(3, f);
  }
  function u(_) {
    as[_ ? "unshift" : "push"](() => {
      a = _, t(4, a);
    });
  }
  return l.$$set = (_) => {
    "value" in _ && t(0, n = _.value), "type" in _ && t(1, i = _.type), "selected" in _ && t(2, s = _.selected);
  }, [n, i, s, f, a, o, u];
}
class Es extends ns {
  constructor(e) {
    super(), _s(this, e, ws, gs, ds, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: vs,
  add_flush_callback: ol,
  assign: ks,
  bind: al,
  binding_callbacks: rl,
  check_outros: ps,
  create_component: Ct,
  destroy_component: yt,
  detach: Cs,
  flush: Z,
  get_spread_object: ys,
  get_spread_update: Ls,
  group_outros: Ms,
  init: Vs,
  insert: Hs,
  mount_component: Lt,
  safe_not_equal: qs,
  space: Fs,
  transition_in: Ze,
  transition_out: Ie
} = window.__gradio__svelte__internal;
function ul(l) {
  let e, t;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[2].i18n
    ) },
    /*loading_status*/
    l[18]
  ];
  let i = {};
  for (let s = 0; s < n.length; s += 1)
    i = ks(i, n[s]);
  return e = new ls({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[24]
  ), {
    c() {
      Ct(e.$$.fragment);
    },
    m(s, f) {
      Lt(e, s, f), t = !0;
    },
    p(s, f) {
      const a = f[0] & /*gradio, loading_status*/
      262148 ? Ls(n, [
        f[0] & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          s[2].autoscroll
        ) },
        f[0] & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          s[2].i18n
        ) },
        f[0] & /*loading_status*/
        262144 && ys(
          /*loading_status*/
          s[18]
        )
      ]) : {};
      e.$set(a);
    },
    i(s) {
      t || (Ze(e.$$.fragment, s), t = !0);
    },
    o(s) {
      Ie(e.$$.fragment, s), t = !1;
    },
    d(s) {
      yt(e, s);
    }
  };
}
function Zs(l) {
  let e, t, n, i, s, f = (
    /*loading_status*/
    l[18] && ul(l)
  );
  function a(u) {
    l[25](u);
  }
  function r(u) {
    l[26](u);
  }
  let o = {
    label: (
      /*label*/
      l[3]
    ),
    info: (
      /*info*/
      l[4]
    ),
    show_label: (
      /*show_label*/
      l[10]
    ),
    lines: (
      /*lines*/
      l[8]
    ),
    type: (
      /*type*/
      l[14]
    ),
    rtl: (
      /*rtl*/
      l[19]
    ),
    text_align: (
      /*text_align*/
      l[20]
    ),
    max_lines: /*max_lines*/ l[11] ? (
      /*max_lines*/
      l[11]
    ) : (
      /*lines*/
      l[8] + 1
    ),
    prompts: (
      /*prompts*/
      l[12]
    ),
    suffixes: (
      /*suffixes*/
      l[13]
    ),
    placeholder: (
      /*placeholder*/
      l[9]
    ),
    autofocus: (
      /*autofocus*/
      l[21]
    ),
    container: (
      /*container*/
      l[15]
    ),
    autoscroll: (
      /*autoscroll*/
      l[22]
    ),
    disabled: !/*interactive*/
    l[23]
  };
  return (
    /*value*/
    l[0] !== void 0 && (o.value = /*value*/
    l[0]), /*value_is_output*/
    l[1] !== void 0 && (o.value_is_output = /*value_is_output*/
    l[1]), t = new yi({ props: o }), rl.push(() => al(t, "value", a)), rl.push(() => al(t, "value_is_output", r)), t.$on(
      "change",
      /*change_handler*/
      l[27]
    ), t.$on(
      "input",
      /*input_handler*/
      l[28]
    ), t.$on(
      "submit",
      /*submit_handler*/
      l[29]
    ), t.$on(
      "blur",
      /*blur_handler*/
      l[30]
    ), t.$on(
      "select",
      /*select_handler*/
      l[31]
    ), t.$on(
      "focus",
      /*focus_handler*/
      l[32]
    ), {
      c() {
        f && f.c(), e = Fs(), Ct(t.$$.fragment);
      },
      m(u, _) {
        f && f.m(u, _), Hs(u, e, _), Lt(t, u, _), s = !0;
      },
      p(u, _) {
        /*loading_status*/
        u[18] ? f ? (f.p(u, _), _[0] & /*loading_status*/
        262144 && Ze(f, 1)) : (f = ul(u), f.c(), Ze(f, 1), f.m(e.parentNode, e)) : f && (Ms(), Ie(f, 1, 1, () => {
          f = null;
        }), ps());
        const c = {};
        _[0] & /*label*/
        8 && (c.label = /*label*/
        u[3]), _[0] & /*info*/
        16 && (c.info = /*info*/
        u[4]), _[0] & /*show_label*/
        1024 && (c.show_label = /*show_label*/
        u[10]), _[0] & /*lines*/
        256 && (c.lines = /*lines*/
        u[8]), _[0] & /*type*/
        16384 && (c.type = /*type*/
        u[14]), _[0] & /*rtl*/
        524288 && (c.rtl = /*rtl*/
        u[19]), _[0] & /*text_align*/
        1048576 && (c.text_align = /*text_align*/
        u[20]), _[0] & /*max_lines, lines*/
        2304 && (c.max_lines = /*max_lines*/
        u[11] ? (
          /*max_lines*/
          u[11]
        ) : (
          /*lines*/
          u[8] + 1
        )), _[0] & /*prompts*/
        4096 && (c.prompts = /*prompts*/
        u[12]), _[0] & /*suffixes*/
        8192 && (c.suffixes = /*suffixes*/
        u[13]), _[0] & /*placeholder*/
        512 && (c.placeholder = /*placeholder*/
        u[9]), _[0] & /*autofocus*/
        2097152 && (c.autofocus = /*autofocus*/
        u[21]), _[0] & /*container*/
        32768 && (c.container = /*container*/
        u[15]), _[0] & /*autoscroll*/
        4194304 && (c.autoscroll = /*autoscroll*/
        u[22]), _[0] & /*interactive*/
        8388608 && (c.disabled = !/*interactive*/
        u[23]), !n && _[0] & /*value*/
        1 && (n = !0, c.value = /*value*/
        u[0], ol(() => n = !1)), !i && _[0] & /*value_is_output*/
        2 && (i = !0, c.value_is_output = /*value_is_output*/
        u[1], ol(() => i = !1)), t.$set(c);
      },
      i(u) {
        s || (Ze(f), Ze(t.$$.fragment, u), s = !0);
      },
      o(u) {
        Ie(f), Ie(t.$$.fragment, u), s = !1;
      },
      d(u) {
        u && Cs(e), f && f.d(u), yt(t, u);
      }
    }
  );
}
function Ss(l) {
  let e, t;
  return e = new Ul({
    props: {
      visible: (
        /*visible*/
        l[7]
      ),
      elem_id: (
        /*elem_id*/
        l[5]
      ),
      elem_classes: (
        /*elem_classes*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[16]
      ),
      min_width: (
        /*min_width*/
        l[17]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        l[15]
      ),
      $$slots: { default: [Zs] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ct(e.$$.fragment);
    },
    m(n, i) {
      Lt(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*visible*/
      128 && (s.visible = /*visible*/
      n[7]), i[0] & /*elem_id*/
      32 && (s.elem_id = /*elem_id*/
      n[5]), i[0] & /*elem_classes*/
      64 && (s.elem_classes = /*elem_classes*/
      n[6]), i[0] & /*scale*/
      65536 && (s.scale = /*scale*/
      n[16]), i[0] & /*min_width*/
      131072 && (s.min_width = /*min_width*/
      n[17]), i[0] & /*container*/
      32768 && (s.padding = /*container*/
      n[15]), i[0] & /*label, info, show_label, lines, type, rtl, text_align, max_lines, prompts, suffixes, placeholder, autofocus, container, autoscroll, interactive, value, value_is_output, gradio, loading_status*/
      16580383 | i[1] & /*$$scope*/
      4 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (Ze(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ie(e.$$.fragment, n), t = !1;
    },
    d(n) {
      yt(e, n);
    }
  };
}
function zs(l, e, t) {
  let { gradio: n } = e, { label: i = "Textbox" } = e, { info: s = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: o = "" } = e, { lines: u } = e, { placeholder: _ = "" } = e, { show_label: c } = e, { max_lines: m } = e, { prompts: v = [] } = e, { suffixes: L = [] } = e, { type: w = "text" } = e, { container: H = !0 } = e, { scale: b = null } = e, { min_width: h = void 0 } = e, { loading_status: p = void 0 } = e, { value_is_output: T = !1 } = e, { rtl: k = !1 } = e, { text_align: N = void 0 } = e, { autofocus: B = !1 } = e, { autoscroll: P = !0 } = e, { interactive: Y = !0 } = e;
  const I = () => n.dispatch("clear_status", p);
  function ie(g) {
    o = g, t(0, o);
  }
  function ge(g) {
    T = g, t(1, T);
  }
  const W = () => n.dispatch("change", o), se = () => n.dispatch("input"), K = () => n.dispatch("submit"), we = () => n.dispatch("blur"), Te = (g) => n.dispatch("select", g.detail), ve = () => n.dispatch("focus");
  return l.$$set = (g) => {
    "gradio" in g && t(2, n = g.gradio), "label" in g && t(3, i = g.label), "info" in g && t(4, s = g.info), "elem_id" in g && t(5, f = g.elem_id), "elem_classes" in g && t(6, a = g.elem_classes), "visible" in g && t(7, r = g.visible), "value" in g && t(0, o = g.value), "lines" in g && t(8, u = g.lines), "placeholder" in g && t(9, _ = g.placeholder), "show_label" in g && t(10, c = g.show_label), "max_lines" in g && t(11, m = g.max_lines), "prompts" in g && t(12, v = g.prompts), "suffixes" in g && t(13, L = g.suffixes), "type" in g && t(14, w = g.type), "container" in g && t(15, H = g.container), "scale" in g && t(16, b = g.scale), "min_width" in g && t(17, h = g.min_width), "loading_status" in g && t(18, p = g.loading_status), "value_is_output" in g && t(1, T = g.value_is_output), "rtl" in g && t(19, k = g.rtl), "text_align" in g && t(20, N = g.text_align), "autofocus" in g && t(21, B = g.autofocus), "autoscroll" in g && t(22, P = g.autoscroll), "interactive" in g && t(23, Y = g.interactive);
  }, [
    o,
    T,
    n,
    i,
    s,
    f,
    a,
    r,
    u,
    _,
    c,
    m,
    v,
    L,
    w,
    H,
    b,
    h,
    p,
    k,
    N,
    B,
    P,
    Y,
    I,
    ie,
    ge,
    W,
    se,
    K,
    we,
    Te,
    ve
  ];
}
class Ts extends vs {
  constructor(e) {
    super(), Vs(
      this,
      e,
      zs,
      Ss,
      qs,
      {
        gradio: 2,
        label: 3,
        info: 4,
        elem_id: 5,
        elem_classes: 6,
        visible: 7,
        value: 0,
        lines: 8,
        placeholder: 9,
        show_label: 10,
        max_lines: 11,
        prompts: 12,
        suffixes: 13,
        type: 14,
        container: 15,
        scale: 16,
        min_width: 17,
        loading_status: 18,
        value_is_output: 1,
        rtl: 19,
        text_align: 20,
        autofocus: 21,
        autoscroll: 22,
        interactive: 23
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[2];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), Z();
  }
  get label() {
    return this.$$.ctx[3];
  }
  set label(e) {
    this.$$set({ label: e }), Z();
  }
  get info() {
    return this.$$.ctx[4];
  }
  set info(e) {
    this.$$set({ info: e }), Z();
  }
  get elem_id() {
    return this.$$.ctx[5];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), Z();
  }
  get elem_classes() {
    return this.$$.ctx[6];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), Z();
  }
  get visible() {
    return this.$$.ctx[7];
  }
  set visible(e) {
    this.$$set({ visible: e }), Z();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), Z();
  }
  get lines() {
    return this.$$.ctx[8];
  }
  set lines(e) {
    this.$$set({ lines: e }), Z();
  }
  get placeholder() {
    return this.$$.ctx[9];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), Z();
  }
  get show_label() {
    return this.$$.ctx[10];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), Z();
  }
  get max_lines() {
    return this.$$.ctx[11];
  }
  set max_lines(e) {
    this.$$set({ max_lines: e }), Z();
  }
  get prompts() {
    return this.$$.ctx[12];
  }
  set prompts(e) {
    this.$$set({ prompts: e }), Z();
  }
  get suffixes() {
    return this.$$.ctx[13];
  }
  set suffixes(e) {
    this.$$set({ suffixes: e }), Z();
  }
  get type() {
    return this.$$.ctx[14];
  }
  set type(e) {
    this.$$set({ type: e }), Z();
  }
  get container() {
    return this.$$.ctx[15];
  }
  set container(e) {
    this.$$set({ container: e }), Z();
  }
  get scale() {
    return this.$$.ctx[16];
  }
  set scale(e) {
    this.$$set({ scale: e }), Z();
  }
  get min_width() {
    return this.$$.ctx[17];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), Z();
  }
  get loading_status() {
    return this.$$.ctx[18];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), Z();
  }
  get value_is_output() {
    return this.$$.ctx[1];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), Z();
  }
  get rtl() {
    return this.$$.ctx[19];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), Z();
  }
  get text_align() {
    return this.$$.ctx[20];
  }
  set text_align(e) {
    this.$$set({ text_align: e }), Z();
  }
  get autofocus() {
    return this.$$.ctx[21];
  }
  set autofocus(e) {
    this.$$set({ autofocus: e }), Z();
  }
  get autoscroll() {
    return this.$$.ctx[22];
  }
  set autoscroll(e) {
    this.$$set({ autoscroll: e }), Z();
  }
  get interactive() {
    return this.$$.ctx[23];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), Z();
  }
}
export {
  Es as BaseExample,
  yi as BaseTextbox,
  Ts as default
};
