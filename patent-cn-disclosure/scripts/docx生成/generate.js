/* generate.js — 技术交底书 md → docx 生成器 v5.1（patent-cn-disclosure skill 底层模板，通用版）
 * 运行：node generate.js <输入.md> [-o 输出.docx] [-i 附图目录] [--header "页眉文本"]
 * 依赖：本目录 node_modules（docx@9，复制自已验证安装，勿重复安装）。
 * 格式规格唯一依据：../../references/docx-format.md §2（常量勿随意改动）；
 * v1–v5.1 演化记录见 ../../NOTICE.md《版本沿革》。
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, PageNumber, AlignmentType, HeadingLevel, WidthType,
  BorderStyle, ShadingType, LevelFormat, TabStopType, TabStopPosition,
  Math: OoxmlMath, MathRun, MathSubScript, MathSuperScript,
} = require("docx");
const fs = require("fs");
const path = require("path");

// ---- CLI ----
const args = process.argv.slice(2);
function argOf(flag) {
  const k = args.indexOf(flag);
  return k >= 0 && args[k + 1] ? args[k + 1] : null;
}
const IN = args.find(a => !a.startsWith("-"));
if (!IN) {
  console.error("用法: node generate.js <输入.md> [-o 输出.docx] [-i 附图目录] [--header 页眉]");
  process.exit(2);
}
const MD = path.resolve(IN);
const OUT = path.resolve(argOf("-o") || argOf("--out") || MD.replace(/\.md$/i, ".docx"));
const IMG_DIR = path.resolve(argOf("-i") || argOf("--img") || path.dirname(MD));
const HEADER_OVERRIDE = argOf("--header");
const RED = "C00000"; // 撰写者提示红（过程稿专用，定稿删除）

// ---- 工具 ----
function pngSize(file) { // PNG IHDR: width@16, height@20 (big-endian)
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
function image(file, width, caption) {
  const { w, h } = pngSize(file);
  const height = Math.round(width * h / w);
  const out = [new Paragraph({
    alignment: AlignmentType.CENTER, keepNext: !!caption, spacing: { before: 120, after: caption ? 40 : 120 },
    children: [new ImageRun({ data: fs.readFileSync(file), transformation: { width, height }, type: "png" })],
  })];
  if (caption) out.push(new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text: caption, bold: true, size: 21, color: "404040", font: { ascii: "Calibri", eastAsia: "SimHei" } })],
  }));
  return out;
}

// ---- 内联/显示 LaTeX → docx 原生公式组件 ----
// 符号映射（v5.1 扩充：真实案件曾因 \sum/\times 缺映射直通为英文字面词，人工改Σ×才过审）
const SYM = {
  "\\sum": "Σ", "\\prod": "∏", "\\times": "×", "\\cdot": "·", "\\div": "÷",
  "\\leq": "≤", "\\geq": "≥", "\\neq": "≠", "\\approx": "≈", "\\pm": "±",
  "\\infty": "∞", "\\partial": "∂", "\\forall": "∀", "\\exists": "∃",
  "\\int": "∫", "\\rightarrow": "→", "\\to": "→", "\\leftarrow": "←", "\\Rightarrow": "⇒",
  "\\alpha": "α", "\\beta": "β", "\\gamma": "γ", "\\delta": "δ", "\\epsilon": "ε",
  "\\varepsilon": "ε", "\\zeta": "ζ", "\\eta": "η", "\\theta": "θ", "\\iota": "ι",
  "\\kappa": "κ", "\\lambda": "λ", "\\mu": "μ", "\\nu": "ν", "\\xi": "ξ",
  "\\pi": "π", "\\rho": "ρ", "\\sigma": "σ", "\\tau": "τ", "\\upsilon": "υ",
  "\\phi": "φ", "\\varphi": "φ", "\\chi": "χ", "\\psi": "ψ", "\\omega": "ω",
  "\\Gamma": "Γ", "\\Delta": "Δ", "\\Theta": "Θ", "\\Lambda": "Λ", "\\Xi": "Ξ",
  "\\Pi": "Π", "\\Sigma": "Σ", "\\Phi": "Φ", "\\Psi": "Ψ", "\\Omega": "Ω",
};
function latexToMath(latex) {
  let s = String(latex);
  for (const [k, v] of Object.entries(SYM)) s = s.split(k).join(v); // 先替换长命令（含\argmin等已含于通用链）
  s = s
    .replace(/\\mathrm\{([^}]*)\}/g, "$1")
    .replace(/\\left\(/g, "(").replace(/\\right\)/g, ")")
    .replace(/\\ell/g, "ℓ").replace(/\\in\b/g, "∈")
    .replace(/\\argmin|\\arg\\min/g, "argmin").replace(/\\argmax|\\arg\\max/g, "argmax")
    .replace(/\\min\b/g, "min").replace(/\\max\b/g, "max")
    .replace(/\\,|\\ /g, " ").replace(/\\/g, "")
    .replace(/-/g, "−");
  const out = [];
  let buf = "";
  const flush = () => { if (buf) { out.push(new MathRun(buf)); buf = ""; } };
  let i = 0;
  while (i < s.length) {
    const ch = s[i];
    if (ch === "_" || ch === "^") {
      const m = buf.match(/([A-Za-z0-9Ωℓ()]+)$/);
      let base = "";
      if (m) { base = m[1]; buf = buf.slice(0, buf.length - base.length); }
      flush();
      i += 1;
      let script = "";
      if (s[i] === "{") {
        let depth = 0, j = i;
        for (; j < s.length; j++) {
          if (s[j] === "{") depth += 1;
          else if (s[j] === "}") { depth -= 1; if (depth === 0) break; }
        }
        script = s.slice(i + 1, j); i = j + 1;
      } else { script = s[i]; i += 1; }
      const parts = latexToMath(script);
      const baseRun = [new MathRun(base || " ")];
      out.push(ch === "_"
        ? new MathSubScript({ children: baseRun, subScript: parts })
        : new MathSuperScript({ children: baseRun, superScript: parts }));
      continue;
    }
    buf += ch; i += 1;
  }
  flush();
  return out;
}

// ---- 文本 → 混排 run（【待确认】红、**加粗**、$内联公式$） ----
function texClean(s) { return s.replace(/[{}]/g, ""); }
function redBase(b) {
  return Object.assign({}, b, { color: RED, font: { ascii: "Calibri", eastAsia: "SimHei" } });
}
function runs(text, base) {
  const out = [];
  // 先按【待确认…】/【提示…】（书写者标记）切红段，再逐段处理加粗与内联公式
  const segs = String(text).split(/(【(?:待确认|提示)[^】]*】)/).filter(x => x !== "");
  for (const seg of segs) {
    const isRed = /^【(待确认|提示)/.test(seg);
    const b = isRed ? redBase(base) : base;
    const boldParts = seg.split("**");
    for (let k = 0; k < boldParts.length; k++) {
      if (boldParts[k] === "") continue;
      const bold = k % 2 === 1 ? true : b.bold;
      const parts = isRed ? [boldParts[k]] : boldParts[k].split("$");
      for (let j = 0; j < parts.length; j++) {
        if (parts[j] === "") continue;
        if (j % 2 === 1 && !isRed) out.push(new OoxmlMath({ children: latexToMath(parts[j]) }));
        else out.push(new TextRun(Object.assign({}, b, { text: texClean(parts[j]), bold })));
      }
    }
  }
  return out;
}
function para(text, opts = {}) {
  const isRed = opts.red === true;
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    indent: opts.noIndent ? undefined : { firstLine: 420 },
    spacing: { line: 312, before: opts.before || 0, after: opts.after || 80 },
    keepNext: opts.keepNext,
    children: runs(text, { size: 24, color: isRed ? RED : "000000",
      font: { ascii: "Calibri", eastAsia: isRed ? "SimHei" : "SimSun" } }),
  });
}

let listSeq = 0;
const numberingConfig = [];
function listRuns(item, redTail) {
  const base = { size: 24, color: "000000", font: { ascii: "Calibri", eastAsia: "SimSun" } };
  if (!redTail) return runs(item, base);
  const sp = splitTrailingParen(item);
  if (!sp) return runs(item, base);
  const out = runs(sp.main, base);
  out.push(new TextRun({ text: sp.red, size: 24, color: RED, font: { ascii: "Calibri", eastAsia: "SimHei" } }));
  if (sp.tail) out.push(new TextRun(Object.assign({}, base, { text: sp.tail })));
  return out;
}
function numberedList(items, red = false, redTail = false) {
  listSeq += 1;
  const ref = "num-list-" + listSeq;
  numberingConfig.push({
    reference: ref,
    levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 620, hanging: 360 } } } }],
  });
  return items.map(t => new Paragraph({
    numbering: { reference: ref, level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 80 },
    children: listRuns(t, redTail),
  }));
}
function bulletList(items, redTail = false) {
  return items.map(t => new Paragraph({
    bullet: { level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { line: 312, after: 80 },
    children: listRuns(t, redTail),
  }));
}

// 末尾说明性括号拆分：返回 {main, red, tail} 或 null（附图说明/参考文献条目用）
function splitTrailingParen(s) {
  const m = String(s).match(/^(.*)（([^（）]*)）(。?)$/);
  if (!m || !m[1]) return null;
  return { main: m[1], red: "（" + m[2] + "）", tail: m[3] };
}

// 表格（列宽：常见 2/3/4 列用已验证比例，其余均分）
const WIDTH_HINTS = { 2: [28, 72], 3: [16, 42, 42], 4: [24, 14, 31, 31] };
function mdTable(rows) {
  const nCol = rows[0].length;
  const widths = WIDTH_HINTS[nCol] || Array(nCol).fill(Math.floor(100 / nCol));
  const cellRuns = (text, isHead) => {
    const base = { size: 21, bold: isHead, color: isHead ? "0B1220" : "000000",
      font: { ascii: "Calibri", eastAsia: isHead ? "SimHei" : "SimSun" } };
    return runs(text, base); // 【待确认】红由 runs() 统一处理
  };
  const mkCell = (text, isHead, w) => new TableCell({
    children: [new Paragraph({
      alignment: AlignmentType.LEFT, spacing: { line: 312 },
      children: cellRuns(text, isHead),
    })],
    shading: isHead ? { type: ShadingType.CLEAR, fill: "F1F5F9" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    width: { size: w, type: WidthType.PERCENTAGE },
  });
  return [new Paragraph({ keepNext: true, spacing: { before: 120 }, children: [] }), new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: "7F8C97" },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: "7F8C97" },
      left: { style: BorderStyle.SINGLE, size: 2, color: "B8C2CB" },
      right: { style: BorderStyle.SINGLE, size: 2, color: "B8C2CB" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "C9D2DA" },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: "C9D2DA" },
    },
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0, cantSplit: true,
      children: r.map((c, j) => mkCell(c, i === 0, widths[j])),
    })),
  })];
}

// ---- 解析 markdown ----
const lines = fs.readFileSync(MD, "utf-8").split(/\r?\n/);
const children = [];
let i = 0, inFence = false, fenceKind = null, formulaCount = 0;
let tableBuf = null, numBuf = null, numBufRed = false, bulBuf = null, currentSection = "";
let inRedSection = false;
let headerText = HEADER_OVERRIDE || "";

const RED_TAIL_SECTIONS = new Set(["附图说明", "参考文献"]);
// 页眉案件名预扫描：兼容加粗行（**案件名称**：X）与头部表格行（| 案件名称 | X | / | 交底书名称 | X |）
if (!headerText) {
  for (const ln of lines) {
    const m = ln.match(/^\|\s*(?:案件名称|交底书名称)\s*\|\s*([^|]+?)\s*\|/)
      || ln.match(/^ ?\*\*(?:案件名称|交底书名称)\*\*[：:]?\s*(.+)$/);
    if (m && m[1].trim()) {
      headerText = "技术交底书——" + m[1].trim().replace(/【[^】]*】/g, "").trim();
      break;
    }
  }
}
function flushLists() {
  const redTail = RED_TAIL_SECTIONS.has(currentSection);
  if (numBuf) { children.push(...numberedList(numBuf, numBufRed, redTail)); numBuf = null; numBufRed = false; }
  if (bulBuf) { children.push(...bulletList(bulBuf, redTail)); bulBuf = null; }
}
function flushTable() {
  if (tableBuf) { children.push(...mdTable(tableBuf)); tableBuf = null; }
}

while (i < lines.length) {
  const line = lines[i];
  if (line.trim().startsWith("```")) {
    flushLists(); flushTable();
    inFence = !inFence;
    if (inFence) fenceKind = line.trim().replace(/`/g, "").trim();
    // 围栏内容（含 mermaid 源码）不落 docx；插图由围栏后的图片行驱动
    i += 1; continue;
  }
  if (inFence) { i += 1; continue; }

  if (/^\s*\|/.test(line)) {
    flushLists();
    const cells = line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(s => s.trim());
    if (/^[-\s:|]+$/.test(line.trim())) { i += 1; continue; } // 分隔行
    if (!tableBuf) tableBuf = [];
    tableBuf.push(cells);
    i += 1; continue;
  } else flushTable();

  const t = line.trim();
  if (t === "" || t === "---") { flushLists(); i += 1; continue; }

  if (t.startsWith("$$") && t.endsWith("$$")) { // 显示公式：原生OMML居中＋编号右对齐
    flushLists();
    formulaCount += 1;
    // 兼容手写编号：剥离尾部 \qquad (n) / \quad (n) / \; (n)，由生成器统一自动编号
    let body = t.slice(2, -2).replace(/\\q?quad\s*\\?[;:]?\s*\(\s*\d+\s*\)\s*$/, "").trim();
    children.push(new Paragraph({
      spacing: { before: 80, after: 120, line: 312 },
      tabStops: [
        { type: TabStopType.CENTER, position: 4394 },
        { type: TabStopType.RIGHT, position: TabStopPosition.MAX },
      ],
      children: [
        new TextRun({ text: "	", size: 24 }),
        new OoxmlMath({ children: latexToMath(body) }),
        new TextRun({ text: "	（" + formulaCount + "）", size: 24, color: "000000" }),
      ],
    }));
    i += 1; continue;
  }

  // 图片行：![图题](文件.png|宽=560) 或 pandoc 风格 ![图题](文件.png){width=6.2in}
  let m;
  if ((m = t.match(/^!\[([^\]]*)\]\(([^)]+)\)\s*(\{[^}]*\})?$/))) {
    flushLists();
    let target = m[2], width = 0;
    const bar = target.indexOf("|");
    if (bar >= 0) {
      const w = parseInt(target.slice(bar + 1).replace(/[^0-9]/g, ""), 10);
      if (w > 0) width = w;
      target = target.slice(0, bar).trim();
    }
    if (m[3]) { // {width=6.2in} 属性（in×96 / cm×37.8）
      const wm = m[3].match(/width\s*=\s*([0-9.]+)\s*(in|cm|px)/);
      if (wm) width = Math.round(parseFloat(wm[1]) * (wm[2] === "in" ? 96 : wm[2] === "cm" ? 37.8 : 1));
    }
    if (!width) width = 540;
    const file = path.isAbsolute(target) ? target : path.join(IMG_DIR, target);
    if (!fs.existsSync(file)) {
      console.error("缺附图文件，中止（先渲染附图 PNG）: " + file);
      process.exit(3);
    }
    children.push(...image(file, width, m[1] || ""));
    i += 1; continue;
  }

  if ((m = t.match(/^#\s+(.*)$/))) { // 文档标题
    inRedSection = false;
    if (!headerText) headerText = m[1].trim();
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 120, after: 200 },
      children: [new TextRun({ text: m[1], bold: true, size: 44, color: "0B1220", font: { ascii: "Calibri", eastAsia: "SimHei" } })],
    }));
    i += 1; continue;
  }
  if ((m = t.match(/^##\s+(.*)$/))) {
    flushLists();
    const red = m[1].trim() === "注意事项";
    inRedSection = red;
    currentSection = m[1].trim();
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, spacing: { before: 360, after: 160, line: 312 },
      children: [new TextRun({ text: m[1], bold: true, size: 32, color: red ? RED : "0B1220", font: { ascii: "Calibri", eastAsia: "SimHei" } })] }));
    i += 1; continue;
  }
  if ((m = t.match(/^###\s+(.*)$/))) {
    flushLists();
    currentSection = m[1].trim();
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 240, after: 120, line: 312 },
      children: [new TextRun({ text: m[1], bold: true, size: 28, color: inRedSection ? RED : "0B1220", font: { ascii: "Calibri", eastAsia: "SimHei" } })] }));
    i += 1; continue;
  }
  if ((m = t.match(/^####\s+(.*)$/))) {
    flushLists();
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, spacing: { before: 200, after: 100, line: 312 },
      children: [new TextRun({ text: m[1], bold: true, size: 24, color: "0B1220", font: { ascii: "Calibri", eastAsia: "SimHei" } })] }));
    i += 1; continue;
  }
  if ((m = t.match(/^>\s?(.*)$/))) {
    flushLists();
    children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { left: 420 },
      spacing: { line: 312, after: 80 },
      children: runs(m[1], { size: 22, color: "595959", font: { ascii: "Calibri", eastAsia: "KaiTi" } }) }));
    i += 1; continue;
  }
  if ((m = t.match(/^(\d+)\.\s+(.*)$/))) {
    if (bulBuf) { children.push(...bulletList(bulBuf)); bulBuf = null; }
    if (!numBuf) { numBuf = []; numBufRed = inRedSection; }
    numBuf.push(m[2]);
    i += 1; continue;
  }
  if ((m = t.match(/^[-*]\s+(.*)$/))) {
    if (numBuf) { children.push(...numberedList(numBuf, numBufRed)); numBuf = null; numBufRed = false; }
    if (!bulBuf) bulBuf = [];
    bulBuf.push(m[1]);
    i += 1; continue;
  }

  // 普通段落；文档头部元信息行（加粗标签行）不缩进
  const isMeta = /^\*\*(案件名称|技术联系人|申请人\/发明人|发明人|联系人|代理机构|专利类型)\*\*/.test(t);
  flushLists();
  const red = inRedSection;
  children.push(para(t, { noIndent: isMeta, align: isMeta ? AlignmentType.LEFT : undefined, red }));

  // 页眉候选：案件名称行
  if (!HEADER_OVERRIDE && /^\*\*案件名称\*\*/.test(t)) {
    headerText = "技术交底书——" + t.replace(/^\*\*案件名称\*\*[:：]\s*/, "").replace(/【[^】]*】/g, "").trim();
  }
  i += 1;
}
flushLists(); flushTable();

const doc = new Document({
  numbering: { config: numberingConfig },
  styles: { default: { document: {
    run: { font: { ascii: "Calibri", eastAsia: "SimSun" }, size: 24, color: "000000" },
    paragraph: { spacing: { line: 312 } },
  }}},
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 },
      margin: { top: 1417, bottom: 1417, left: 1701, right: 1417 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: headerText || "技术交底书", size: 18, color: "888888" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  const back = fs.readFileSync(OUT); // 写入回读核验（防间歇性写失败）
  if (back.length !== buf.length) {
    console.error("回读长度不符，写入可疑，请重跑: " + OUT);
    process.exit(4);
  }
  console.log("written: " + OUT + " " + buf.length + " bytes");
});
