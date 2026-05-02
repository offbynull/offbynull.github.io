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
const inputSplit = /(.*)/g.exec(input);
const output = `<sub>[\\[src\\]](${inputSplit[1].trim()})</sub>`;
fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });