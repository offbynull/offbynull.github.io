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
const inputSplit = /(.*):(.*):?(.*)/g.exec(input);
if (inputSplit[1].trim().toLowerCase() === 'gt') {
    const output = `<sub>[\\[GT2018:${inputSplit[2].trim()}\\]](http://faculty.econ.ucdavis.edu/faculty/bonanno/GT_Book.html)</sub>`;
    fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });
} else {
    throw Error(`Unrecognized type: ${inputSplit}`)
}