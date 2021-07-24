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

// https://developer.mozilla.org/en-US/docs/Web/CSS/color_value#color_keywords
const nameToRgb = new Map();
nameToRgb.set('black', '#000000');
nameToRgb.set('silver', '#c0c0c0');
nameToRgb.set('gray', '#808080');
nameToRgb.set('white', '#ffffff');
nameToRgb.set('maroon', '#800000');
nameToRgb.set('red', '#ff0000');
nameToRgb.set('purple', '#800080');
nameToRgb.set('fuchsia', '#ff00ff');
nameToRgb.set('green', '#008000');
nameToRgb.set('lime', '#00ff00');
nameToRgb.set('olive', '#808000');
nameToRgb.set('yellow', '#ffff00');
nameToRgb.set('navy', '#000080');
nameToRgb.set('blue', '#0000ff');
nameToRgb.set('teal', '#008080');
nameToRgb.set('aqua', '#00ffff');
nameToRgb.set('orange', '#ffa500');
nameToRgb.set('aliceblue', '#f0f8ff');
nameToRgb.set('antiquewhite', '#faebd7');
nameToRgb.set('aquamarine', '#7fffd4');
nameToRgb.set('azure', '#f0ffff');
nameToRgb.set('beige', '#f5f5dc');
nameToRgb.set('bisque', '#ffe4c4');
nameToRgb.set('blanchedalmond', '#ffebcd');
nameToRgb.set('blueviolet', '#8a2be2');
nameToRgb.set('brown', '#a52a2a');
nameToRgb.set('burlywood', '#deb887');
nameToRgb.set('cadetblue', '#5f9ea0');
nameToRgb.set('chartreuse', '#7fff00');
nameToRgb.set('chocolate', '#d2691e');
nameToRgb.set('coral', '#ff7f50');
nameToRgb.set('cornflowerblue', '#6495ed');
nameToRgb.set('cornsilk', '#fff8dc');
nameToRgb.set('crimson', '#dc143c');
nameToRgb.set('cyan', '#00ffff');
nameToRgb.set('aqua', '#00ffff');
nameToRgb.set('darkblue', '#00008b');
nameToRgb.set('darkcyan', '#008b8b');
nameToRgb.set('darkgoldenrod', '#b8860b');
nameToRgb.set('darkgray', '#a9a9a9');
nameToRgb.set('darkgreen', '#006400');
nameToRgb.set('darkgrey', '#a9a9a9');
nameToRgb.set('darkkhaki', '#bdb76b');
nameToRgb.set('darkmagenta', '#8b008b');
nameToRgb.set('darkolivegreen', '#556b2f');
nameToRgb.set('darkorange', '#ff8c00');
nameToRgb.set('darkorchid', '#9932cc');
nameToRgb.set('darkred', '#8b0000');
nameToRgb.set('darksalmon', '#e9967a');
nameToRgb.set('darkseagreen', '#8fbc8f');
nameToRgb.set('darkslateblue', '#483d8b');
nameToRgb.set('darkslategray', '#2f4f4f');
nameToRgb.set('darkslategrey', '#2f4f4f');
nameToRgb.set('darkturquoise', '#00ced1');
nameToRgb.set('darkviolet', '#9400d3');
nameToRgb.set('deeppink', '#ff1493');
nameToRgb.set('deepskyblue', '#00bfff');
nameToRgb.set('dimgray', '#696969');
nameToRgb.set('dimgrey', '#696969');
nameToRgb.set('dodgerblue', '#1e90ff');
nameToRgb.set('firebrick', '#b22222');
nameToRgb.set('floralwhite', '#fffaf0');
nameToRgb.set('forestgreen', '#228b22');
nameToRgb.set('gainsboro', '#dcdcdc');
nameToRgb.set('ghostwhite', '#f8f8ff');
nameToRgb.set('gold', '#ffd700');
nameToRgb.set('goldenrod', '#daa520');
nameToRgb.set('greenyellow', '#adff2f');
nameToRgb.set('grey', '#808080');
nameToRgb.set('honeydew', '#f0fff0');
nameToRgb.set('hotpink', '#ff69b4');
nameToRgb.set('indianred', '#cd5c5c');
nameToRgb.set('indigo', '#4b0082');
nameToRgb.set('ivory', '#fffff0');
nameToRgb.set('khaki', '#f0e68c');
nameToRgb.set('lavender', '#e6e6fa');
nameToRgb.set('lavenderblush', '#fff0f5');
nameToRgb.set('lawngreen', '#7cfc00');
nameToRgb.set('lemonchiffon', '#fffacd');
nameToRgb.set('lightblue', '#add8e6');
nameToRgb.set('lightcoral', '#f08080');
nameToRgb.set('lightcyan', '#e0ffff');
nameToRgb.set('lightgoldenrodyellow', '#fafad2');
nameToRgb.set('lightgray', '#d3d3d3');
nameToRgb.set('lightgreen', '#90ee90');
nameToRgb.set('lightgrey', '#d3d3d3');
nameToRgb.set('lightpink', '#ffb6c1');
nameToRgb.set('lightsalmon', '#ffa07a');
nameToRgb.set('lightseagreen', '#20b2aa');
nameToRgb.set('lightskyblue', '#87cefa');
nameToRgb.set('lightslategray', '#778899');
nameToRgb.set('lightslategrey', '#778899');
nameToRgb.set('lightsteelblue', '#b0c4de');
nameToRgb.set('lightyellow', '#ffffe0');
nameToRgb.set('limegreen', '#32cd32');
nameToRgb.set('linen', '#faf0e6');
nameToRgb.set('magenta', '#ff00ff');
nameToRgb.set('fuchsia', '#ff00ff');
nameToRgb.set('mediumaquamarine', '#66cdaa');
nameToRgb.set('mediumblue', '#0000cd');
nameToRgb.set('mediumorchid', '#ba55d3');
nameToRgb.set('mediumpurple', '#9370db');
nameToRgb.set('mediumseagreen', '#3cb371');
nameToRgb.set('mediumslateblue', '#7b68ee');
nameToRgb.set('mediumspringgreen', '#00fa9a');
nameToRgb.set('mediumturquoise', '#48d1cc');
nameToRgb.set('mediumvioletred', '#c71585');
nameToRgb.set('midnightblue', '#191970');
nameToRgb.set('mintcream', '#f5fffa');
nameToRgb.set('mistyrose', '#ffe4e1');
nameToRgb.set('moccasin', '#ffe4b5');
nameToRgb.set('navajowhite', '#ffdead');
nameToRgb.set('oldlace', '#fdf5e6');
nameToRgb.set('olivedrab', '#6b8e23');
nameToRgb.set('orangered', '#ff4500');
nameToRgb.set('orchid', '#da70d6');
nameToRgb.set('palegoldenrod', '#eee8aa');
nameToRgb.set('palegreen', '#98fb98');
nameToRgb.set('paleturquoise', '#afeeee');
nameToRgb.set('palevioletred', '#db7093');
nameToRgb.set('papayawhip', '#ffefd5');
nameToRgb.set('peachpuff', '#ffdab9');
nameToRgb.set('peru', '#cd853f');
nameToRgb.set('pink', '#ffc0cb');
nameToRgb.set('plum', '#dda0dd');
nameToRgb.set('powderblue', '#b0e0e6');
nameToRgb.set('rosybrown', '#bc8f8f');
nameToRgb.set('royalblue', '#4169e1');
nameToRgb.set('saddlebrown', '#8b4513');
nameToRgb.set('salmon', '#fa8072');
nameToRgb.set('sandybrown', '#f4a460');
nameToRgb.set('seagreen', '#2e8b57');
nameToRgb.set('seashell', '#fff5ee');
nameToRgb.set('sienna', '#a0522d');
nameToRgb.set('skyblue', '#87ceeb');
nameToRgb.set('slateblue', '#6a5acd');
nameToRgb.set('slategray', '#708090');
nameToRgb.set('slategrey', '#708090');
nameToRgb.set('snow', '#fffafa');
nameToRgb.set('springgreen', '#00ff7f');
nameToRgb.set('steelblue', '#4682b4');
nameToRgb.set('tan', '#d2b48c');
nameToRgb.set('thistle', '#d8bfd8');
nameToRgb.set('tomato', '#ff6347');
nameToRgb.set('turquoise', '#40e0d0');
nameToRgb.set('violet', '#ee82ee');
nameToRgb.set('wheat', '#f5deb3');
nameToRgb.set('whitesmoke', '#f5f5f5');
nameToRgb.set('yellowgreen', '#9acd32');
nameToRgb.set('rebeccapurple', '#663399');
const toRgb = (c) => {
    if (c.length == 7 && c.startsWith('#')) {
        return c;
    }
    const ret = nameToRgb.get(c);
    if (ret === undefined) {
        throw `Unable to handle ${c}`;
    }
    return ret;
}

// https://stackoverflow.com/a/36888120
const contrastColor = (c) => {
    const hex = toRgb(c);
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    const luma = ((0.299 * r) + (0.587 * g) + (0.114 * b)) / 255;  // Calculate the perceptive luminance (aka luma) - human eye favors green color... 
    return luma > 0.5 ? 'black' : 'white';                         // Return black for bright colors, white for dark colors
};

const input = fs.readFileSync('/input/input.data', { encoding: 'utf8' }).trim();
const outputColor = input.substring(0, input.indexOf(' ')).trim()
const outputText = input.substring(input.indexOf(' ')).trim()
const output = `<span style="background-color: ${outputColor}; color: ${contrastColor(outputColor)}; padding: 3px">${outputText}</span>`
fs.writeFileSync('/output/output.md', output, { encoding: 'utf8' });