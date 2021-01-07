import { Anki } from './anki';

document.addEventListener('DOMContentLoaded', async () => {
    const anki = await Anki.create();  // this'll set up the database and start manipulating the DOM
    anki.showNextQuestion();
});