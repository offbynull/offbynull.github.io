import { Anki } from './anki';

// export {AnkiDom} from './ankidom';
// export {AnkiDb} from './ankidb';

document.addEventListener("DOMContentLoaded", function(){
    const anki = new Anki();  // this'll set up the database and start manipulating the DOM
});