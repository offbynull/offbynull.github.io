import { AnkiDb, Grade, Question } from './ankidb';
import { AnkiDom } from './ankidom';

export class Anki {
    private activeQuestion: Question | undefined; // active id

    private constructor(
        private readonly dom: AnkiDom,
        private readonly db: AnkiDb,
        private readonly questionCount: number
    ) {
        this.activeQuestion = undefined;
    }

    public static async create(databaseName: string = 'internal'): Promise<Anki> {
        const dom = new AnkiDom();
        const db = AnkiDb.create(databaseName);
        
        const cnt = dom.getQuestionCount();
        let aliveCnt = 0;
        for (let id = 0; id < cnt; id++) {
            const dead = dom.isDeadQuestion(id);
            db.trackQuestion(id, dead);
            if (dead === false) {
                aliveCnt++;
            }
        }

        dom.findAndUpdateInfoTag('NONE', aliveCnt);
        return new Anki(dom, db, aliveCnt);
    }

    public async showNextQuestion() {
        if (this.activeQuestion !== undefined) {
            this.dom.hideQuestion(this.activeQuestion.id);
            console.log('hiding' + this.activeQuestion.id)
        }
        this.activeQuestion = await this.db.getNextScheduledQuestion();
        if (this.activeQuestion !== undefined) {
            this.dom.showQuestion(this.activeQuestion.id, (passed, showTime) => this.questionComplete(passed, showTime));
        }
    }

    private async questionComplete(passed: boolean, showTime: Date): Promise<void> {
        if (this.activeQuestion === undefined) {
            throw new Error('Should never happen');
        }
        this.dom.findAndUpdateInfoTag(passed ? 'PASS' : 'FAIL', this.questionCount);
        await this.db.answerQuestion(this.activeQuestion.id, passed ? Grade.CORRECT_PERFECT : Grade.INCORRECT_BLACKOUT);
        await this.showNextQuestion();
    }
}