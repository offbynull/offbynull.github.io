import { AnkiDb } from "./ankidb";
import { AnkiDom } from "./ankidom";

export class Anki {
    private readonly dom: AnkiDom;
    private readonly db: AnkiDb;

    public constructor(databaseName: string = 'internal') {
        this.dom = new AnkiDom();
        this.db = AnkiDb.create(databaseName);
        const cnt = this.dom.getQuestionCount();
        for (let id = 0; id < cnt; id++) {
            this.db.trackQuestion(id);
        }
    }

    public async showNextQuestion() {
        const question = await this.db.getNextScheduledQuestion();
        if (question === undefined) {
            throw 'No questions';
        }
        this.dom.showQuestion(question.id, (passed, showTime) => {
            console.log(passed, showTime);
            this.showNextQuestion();
        });
    }
}