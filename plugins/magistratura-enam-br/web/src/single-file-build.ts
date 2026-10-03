import type { Plugin } from "vite";

export function singleFileBuild(): Plugin {
  return {
    name: "single-file-build",
    enforce: "post",
    config: () => ({
      base: "./",
      build: {
        assetsInlineLimit: () => true,
        cssCodeSplit: false,
        assetsDir: "",
        chunkSizeWarningLimit: 1000,
        rollupOptions: { output: { inlineDynamicImports: true } },
      },
    }),
    generateBundle(_options, bundle) {
      const entry = bundle["index.html"];
      if (!entry || entry.type !== "asset") this.error("O widget exige um único index.html");
      let html = typeof entry.source === "string" ? entry.source : new TextDecoder().decode(entry.source);
      const incorporated = new Set<string>();
      html = html.replace(/<script\b[^>]*\bsrc="([^"]+)"[^>]*><\/script>/g, (_tag, href: string) => {
        const chunk = bundle[href.replace(/^\.\//, "")];
        if (!chunk || chunk.type !== "chunk") this.error(`Script não incorporável: ${href}`);
        incorporated.add(chunk.fileName);
        // Escape HTML delimiters without changing the JavaScript string value.
        const code = chunk.code.replace(/<\/script|<!--/gi, match => "\\x3C" + match.slice(1));
        return `<script type="module">${code}</script>`;
      });
      html = html.replace(/<link\b[^>]*\bhref="([^"]+)"[^>]*>/g, (tag, href: string) => {
        if (!/\brel="stylesheet"/.test(tag)) return tag;
        const asset = bundle[href.replace(/^\.\//, "")];
        if (!asset || asset.type !== "asset" || !asset.fileName.endsWith(".css")) this.error(`CSS não incorporável: ${href}`);
        incorporated.add(asset.fileName);
        const css = typeof asset.source === "string" ? asset.source : new TextDecoder().decode(asset.source);
        return `<style>${css.replace(/<\/style/gi, match => "\\3C " + match.slice(1))}</style>`;
      });
      entry.source = html;
      for (const name of incorporated) delete bundle[name];
      if (Object.keys(bundle).some(name => name !== "index.html")) this.error("O widget deve gerar somente index.html");
    },
  };
}
