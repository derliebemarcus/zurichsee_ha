import { readFile, writeFile } from "node:fs/promises";

const packageData = JSON.parse(await readFile("package.json", "utf8"));
const version = String(packageData.version).trim();
const manifestPath = "custom_components/zurichsee_ha/manifest.json";
const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
manifest.version = version;

await writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");
await writeFile("version.txt", version + "\n", "utf8");
console.log("Synchronized integration release metadata to " + version);
