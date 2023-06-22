import * as sass from 'sass';
import { promisify } from 'util';
import { writeFile } from 'fs';

const sassRenderPromise = promisify(sass.render);
const writeFilePromise = promisify(writeFile);
const buildPath = `${process.cwd()}/app/static/dist`;
const srcPath = `${process.cwd()}/app/static/src`;

async function main() {
  const styleResult = await sassRenderPromise({
    file: `${srcPath}/scss/main.scss`,
    outFile: `${buildPath}/css/styles.css`,
    sourceMap: true,
    sourceMapContents: true,
    outputStyle: 'compressed'
  });

  console.log(styleResult.css.toString());

  await writeFilePromise("styles.css", styleResult.css, "utf-8");
  await writeFilePromise("styles.css.map", styleResult.map, "utf-8");
}

main();
