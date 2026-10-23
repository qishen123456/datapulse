// Uses the bundled artifact-tool runtime. Supply NODE_PATH via the documented symlink.
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';
const root = fileURLToPath(new URL('../', import.meta.url));
const tables = JSON.parse(await fs.readFile(`${root}generated/model.json`, 'utf8'));
await fs.mkdir(`${root}data`, { recursive: true });
const quote = value => {
  const text = value == null ? '' : String(value);
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
for (const [name, rows] of Object.entries(tables)) {
  const headers = Object.keys(rows[0]);
  const matrix = [headers, ...rows.map(row => headers.map(key => row[key] ?? ''))];
  const wb = Workbook.create();
  const sheet = wb.worksheets.add(name);
  const range = sheet.getRangeByIndexes(0, 0, matrix.length, headers.length);
  range.values = matrix;
  wb.recalculate();
  const values = range.values;
  if (values.length !== matrix.length) throw new Error(`${name}: row count changed`);
  for (let r = 0; r < matrix.length; r++) {
    for (let c = 0; c < headers.length; c++) {
      if ((values[r][c] ?? '') !== matrix[r][c]) throw new Error(`${name}: value changed at ${r},${c}`);
    }
  }
  const csv = '\uFEFF' + values.map(row => row.map(quote).join(',')).join('\r\n') + '\r\n';
  await fs.writeFile(`${root}data/${name}.csv`, csv, 'utf8');
  console.log(`${name}: ${rows.length} rows × ${headers.length} columns`);
}
