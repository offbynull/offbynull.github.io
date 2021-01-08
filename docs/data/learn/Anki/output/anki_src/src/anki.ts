import { AnkiDb, Grade, Question } from './ankidb';
import { AnkiDom } from './ankidom';

export class Anki {
    private activeQuestion: Question | undefined; // active id

    private constructor(
        private readonly dom: AnkiDom,
        private readonly db: AnkiDb
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

        dom.setQuestionCount(aliveCnt);
        return new Anki(dom, db);
    }

    public async showNextQuestion() {
        if (this.activeQuestion !== undefined) {
            this.dom.hideQuestion(this.activeQuestion.id);
        }
        this.activeQuestion = await this.db.getNextScheduledQuestion();
        if (this.activeQuestion !== undefined) {
            this.dom.showQuestion(this.activeQuestion.id, (grade) => this.questionComplete(grade));
            this.dom.setOutOfQuestionsFlag(false);
        } else {
            this.dom.setOutOfQuestionsFlag(true);
        }
    }

    private async questionComplete(grade: Grade): Promise<void> {
        if (this.activeQuestion === undefined) {
            throw new Error('Should never happen');
        }
        await this.db.answerQuestion(this.activeQuestion.id, grade);
        await this.showNextQuestion();
    }
}