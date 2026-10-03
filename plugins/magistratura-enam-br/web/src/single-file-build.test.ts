// @vitest-environment node
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { build } from "vite";
import { JSDOM } from "jsdom";
import { singleFileBuild } from "./single-file-build";

test("Vite gera um HTML autocontido com JS CSS e asset incorporados", async () => {
  const root = mkdtempSync(join(tmpdir(), "magistratura-single-file-"));
  try {
    writeFileSync(join(root, "index.html"), '<html><body><div id="root"></div><script type="module" src="/main.js"></script></body></html>');
    writeFileSync(join(root, "main.js"), 'import "./style.css"; import icon from "./icon.svg"; window.fixture = [icon, "</script>", "<!--"];');
    writeFileSync(join(root, "style.css"), 'body {color:red} .fixture::after {content:"</style>"}');
    writeFileSync(join(root, "icon.svg"), '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg>');
    const result = await build({ configFile: false, root, logLevel: "silent", plugins: [singleFileBuild()], build: { write: false } });
    const output = Array.isArray(result) ? result[0].output : "output" in result ? result.output : [];
    expect(output.map(asset => asset.fileName)).toEqual(["index.html"]);
    const html = output.find(asset => asset.fileName === "index.html");
    if (!html || html.type !== "asset") throw new Error("HTML ausente");
    const document = new JSDOM(String(html.source)).window.document;
    expect(document.querySelector("script[src]")).toBeNull();
    expect(document.querySelector('link[rel="stylesheet"]')).toBeNull();
    const script = document.querySelector("script")!.textContent!;
    expect(script).toContain("data:image/svg+xml");
    // Compile the synthetic output: closing-tag escaping must preserve JS syntax.
    expect(() => new Function(script)).not.toThrow();
    expect(document.querySelector("style")!.textContent).toContain("color:red");
    expect(document.querySelector("style")!.textContent).toContain("/style>");
  } finally {
    if (dirname(resolve(root)) !== resolve(tmpdir())) throw new Error("Diretório temporário inesperado");
    rmSync(root, { recursive: true, force: true });
  }
});
