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
if (input === 'self') {
    const output = `<sub>[\\[self src\\]](data:text/html,%3C!doctype%20html%3E%0A%3Chtml%3E%0A%3Cbody%3E%0AThis%20was%20derived%20using%20self%20experimentation%20-%20there%20is%20no%20source%20other%20than%20myself.%0A%3C/body%3E%0A%3C/html%3E)</sub>`
    fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });
} else {
    const inputSplit = /(.*)/g.exec(input);
    const output = `<sub>[\\[src\\]](${inputSplit[1].trim()})</sub>`;
    fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });
}