const fs = require('fs');
const cp = require('child_process');

const packageJson = JSON.parse(fs.readFileSync('package.json', { encoding: 'utf8' }));
try {
    for (const requiredModule of Object.keys(packageJson.dependencies)) {
        require(requiredModule)
    }
} catch (e) {
    cp.execSync('npm install', { stdio: [0, 1, 2] });
}


const input = fs.readFileSync('/input/input.data', { encoding: 'utf8' }).trim();
const refs = JSON.parse(fs.readFileSync('/input/refs.json', { encoding: 'utf8' }).trim());
const inputSplit = /([^:]+):([^:]+)(?::(.+))?/g.exec(input);
// throw inputSplit.length
const refKey = inputSplit[1].trim();
const srcText = inputSplit[2].trim();
const srcOther = inputSplit[3] !== undefined ? inputSplit[3].trim() : null;
const srcName = refs[refKey]["name"].trim();
const srcLink = refs[refKey]["link"].trim();
if (srcName === undefined || srcLink === undefined) {
    throw Error(`Unrecognized type: ${inputSplit}`)
}
const output = `<sub>\\[`
        + `[${srcName}` + (srcText === '' ? '' : `:${srcText}`) + `](${srcLink})`
        + (srcOther === null ? '' : `:${srcOther}`) + `\\]</sub>`;
fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });